import argparse
import datetime
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

import yaml
from markdown_it import MarkdownIt


EXCLUDED = {".git", "node_modules", ".venv", "venv", "__pycache__"}
TEXT_SUFFIXES = {
    ".md", ".txt", ".py", ".ipynb", ".sh", ".ps1", ".bicep", ".bicepparam",
    ".json", ".jsonc", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf",
    ".env", ".js", ".jsx", ".ts", ".tsx", ".cs", ".java", ".go", ".html",
    ".xml", ".sql", ".tf", ".tfvars", ".properties", ".csv", ".log",
}
ENDPOINT = re.compile(
    r"https?://[a-z0-9-]+\.(?:openai\.azure\.com|cognitiveservices\.azure\.com|"
    r"services\.ai\.azure\.com|azure-api\.net|azurecr\.io|servicebus\.windows\.net)"
    r"(?=[:/\s\"'<>\\)]|$)", re.I
)
UUID = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
IDENTIFIER = re.compile(
    rf"(?<![a-z0-9_<-])(?:subscription[_ -]?id|tenant[_ -]?id|/subscriptions/|/tenants/)"
    rf"[^a-z0-9\r\n]{{0,20}}(?P<id>{UUID})", re.I
)
LAB = re.compile(r"^\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN = MarkdownIt("commonmark", {"html": True})


def git(*args):
    return subprocess.run(
        ["git", *args], check=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    ).stdout


def tree_entries():
    def walk(directory):
        for entry in sorted(directory.iterdir()):
            if entry.name in EXCLUDED:
                continue
            if entry.is_symlink():
                raise ValueError(f"Unsupported symlink: {entry}")
            yield entry
            if entry.is_dir():
                yield from walk(entry)
    yield from walk(Path("."))


def tree_files():
    return (entry for entry in tree_entries() if entry.is_file())


def history():
    if git("rev-parse", "--is-shallow-repository").strip() != b"false":
        raise ValueError("History scan requires a full clone, not a shallow repository")
    commits = git("rev-list", "--all").decode("ascii").splitlines()
    if not commits:
        raise ValueError("History scan not run: no commits")
    seen = set()
    for commit in commits:
        for entry in git("ls-tree", "-rz", "--full-tree", commit).split(b"\0"):
            if not entry:
                continue
            header, name = entry.split(b"\t", 1)
            mode, kind, oid = header.split()
            if kind != b"blob":
                continue
            name = name.decode("utf-8")
            if mode == b"120000":
                raise ValueError(f"Unsupported historical symlink: {commit[:12]}:{name}")
            if (name, oid) in seen:
                continue
            seen.add((name, oid))
            yield name, git("cat-file", "blob", oid.decode("ascii")), commit[:12]


def text(data):
    if b"\0" in data:
        raise ValueError("Text scan requires UTF-8, not binary or UTF-16 content")
    return data.decode("utf-8")


def allowance():
    file = Path(".workshop-scan-allowlist.json")
    if not file.exists():
        return set()
    entries = json.loads(file.read_text(encoding="utf-8"))["entries"]
    if not isinstance(entries, list):
        raise ValueError("Allowlist entries must be a list")
    result = set()
    for entry in entries:
        if (not isinstance(entry, dict) or
            not all(isinstance(entry.get(k), str) and entry[k].strip()
                    for k in ("kind", "path", "sha256", "reason")) or
            entry["kind"] not in {"endpoint", "identifier", "historical-output"} or
            not re.fullmatch(r"[0-9a-f]{64}", entry["sha256"])):
            raise ValueError("Invalid allowlist entry")
        result.add((entry["kind"], entry["path"], entry["sha256"]))
    return result


def fingerprint(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def finding(kind, name, value, location, allowed):
    digest = fingerprint(value)
    if (kind, name, digest) in allowed:
        return None
    return f"{name} [{location}]: {kind}; sha256={digest}"


def documents(scope):
    for file in tree_files():
        yield file.as_posix(), file.read_bytes(), "working tree"
    if scope == "all":
        yield from history()


def secrets(scope):
    if scope == "all":
        # Check the history prerequisites before reporting any scan as complete.
        if git("rev-parse", "--is-shallow-repository").strip() != b"false":
            raise ValueError("History scan requires a full clone")
        if not git("rev-list", "--all").strip():
            raise ValueError("History scan not run: no commits")
    commands = [["gitleaks", "dir", ".", "--redact", "--no-banner"]]
    if scope == "all":
        commands.append(["gitleaks", "git", ".", "--log-opts=--all", "--redact", "--no-banner"])
    for command in commands:
        result = subprocess.run(command, check=False)
        if result.returncode:
            return result.returncode
    return 0


def identifiers(scope):
    allowed = allowance()
    bad = []
    for name, data, location in documents(scope):
        file = Path(name)
        if not (file.suffix.lower() in TEXT_SUFFIXES or
                file.name.startswith(".env") or file.name in {"Dockerfile", "Makefile"}):
            continue
        source = text(data)
        # Decode notebook strings so JSON escapes cannot conceal identifiers.
        if name.endswith(".ipynb"):
            source = json.dumps(json.loads(source), ensure_ascii=False)
        for pattern, kind in ((ENDPOINT, "endpoint"), (IDENTIFIER, "identifier")):
            for match in pattern.finditer(source):
                value = match.group("id") if kind == "identifier" else match.group()
                error = finding(kind, name, value, location, allowed)
                if error:
                    bad.append(error)
    return bad


def notebooks(scope):
    allowed = allowance()
    bad = []
    for name, data, location in documents(scope):
        if not name.endswith(".ipynb"):
            continue
        notebook = json.loads(data)
        cells = notebook["cells"]
        if not isinstance(cells, list):
            raise ValueError(f"{name}: cells must be a list")
        for index, cell in enumerate(cells):
            if cell["cell_type"] != "code":
                continue
            if "outputs" not in cell or "execution_count" not in cell:
                bad.append(f"{name} [{location}]: missing code-cell output fields")
                continue
            if cell["outputs"] != [] or cell["execution_count"] is not None:
                if location == "working tree":
                    bad.append(f"{name}: cell {index + 1} has output/execution_count")
                else:
                    value = json.dumps(
                        [cell["outputs"], cell["execution_count"]],
                        sort_keys=True, ensure_ascii=False
                    )
                    error = finding("historical-output", name, value, location, allowed)
                    if error:
                        bad.append(error)
    return bad


def paths():
    bad = []
    for file in tree_entries():
        for part in file.parts:
            if " " in part or not part.isascii():
                bad.append(f"{file}: non-standard path")
                break
    return bad


def frontmatter(file):
    source = file.read_text(encoding="utf-8-sig")
    match = re.match(r"^---\n(.*?)\n---(?:\n|$)", source, re.S)
    if not match:
        raise ValueError(f"{file}: missing frontmatter")
    metadata = yaml.safe_load(match.group(1))
    if not isinstance(metadata, dict):
        raise ValueError(f"{file}: frontmatter must be a mapping")
    return metadata


def date_value(value, empty=False):
    if empty and value is None:
        return True
    if isinstance(value, datetime.datetime):
        return False
    if isinstance(value, datetime.date):
        return True
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return False
    try:
        datetime.date.fromisoformat(value)
        return True
    except ValueError:
        return False


def duration(value):
    return value is None or (type(value) is int and value > 0)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def strings(value):
    return isinstance(value, list) and bool(value) and all(nonempty(v) for v in value)


def metadata():
    fm = frontmatter(Path("README.md"))
    rules = {
        "type": lambda v: v == "workshop",
        "title": nonempty, "description": nonempty,
        "level": lambda v: v in ("beginner", "intermediate", "advanced"),
        "authors": strings, "contacts": strings,
        "duration_minutes": duration,
        "tags": lambda v: strings(v) and all(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", t) for t in v),
        "language": lambda v: isinstance(v, str) and bool(re.fullmatch(r"[a-z]{2}", v)),
        "execution": lambda v: strings(v) and all(t in ("codespaces", "local", "portal") for t in v),
        "status": lambda v: v in ("active", "draft", "archived"),
        "source": lambda v: isinstance(v, str) and (v == "original" or bool(re.fullmatch(r"localized: https?://\S+", v))),
        "last_updated": date_value,
        "validated_on": lambda v: date_value(v, empty=True),
    }
    bad = [f"README.md: missing/invalid {key}" for key, rule in rules.items()
           if key not in fm or not rule(fm[key])]
    if strings(fm.get("authors")) and strings(fm.get("contacts")):
        if len(fm["authors"]) != len(fm["contacts"]):
            bad.append("README.md: authors/contacts counts differ")
    return bad


def lab_owner(file):
    parts = file.parts
    if parts and LAB.fullmatch(parts[0]):
        return Path(parts[0])
    if len(parts) > 1 and parts[0] == "labs" and LAB.fullmatch(parts[1]):
        return Path(*parts[:2])
    return None


def lab_metadata():
    bad = []
    for file in tree_files():
        owner = lab_owner(file)
        legacy = re.match(r"^lab\d", file.parent.name)
        if file.name != "README.md" or (not legacy and (owner is None or file.parent != owner)):
            continue
        fm = frontmatter(file)
        for key, rule in (("title", nonempty), ("duration_minutes", duration), ("last_updated", date_value)):
            if key not in fm or not rule(fm[key]):
                bad.append(f"{file}: missing/invalid {key}")
    return bad


class HtmlReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append(attrs[key])
        if tag == "img":
            self.images.append(attrs.get("alt", ""))


def references(file):
    source = file.read_text(encoding="utf-8-sig")
    source = re.sub(r"^---\n.*?\n---(?:\n|$)", "", source, count=1, flags=re.S)
    links, images = [], []
    for block in MARKDOWN.parse(source):
        for token in block.children or [block]:
            if token.type == "link_open":
                links.append(token.attrGet("href"))
            elif token.type == "image":
                links.append(token.attrGet("src"))
                images.append(token.content)
            elif token.type in ("html_block", "html_inline"):
                parser = HtmlReferences()
                parser.feed(token.content)
                links.extend(parser.links)
                images.extend(parser.images)
    return links, images


def resolve(file, href):
    url = urlsplit(href)
    if url.scheme or url.netloc:
        return None
    target = unquote(url.path)
    if not target:
        return file.resolve()
    root = Path.cwd().resolve()
    result = (root / target.lstrip("/") if target.startswith("/") else file.parent / target).resolve()
    if not result.is_relative_to(root):
        raise ValueError(f"{file}: link leaves repository")
    return result


def content(check):
    bad = []
    for file in tree_files():
        if file.suffix.lower() != ".md":
            continue
        links, images = references(file)
        if check == 8:
            if any(not alt.strip() for alt in images):
                bad.append(f"{file}: empty image alt-text")
            continue
        for href in links:
            target = resolve(file, href)
            if target is None:
                continue
            if check == 6 and not target.exists():
                bad.append(f"{file}: missing link target {href}")
            if check == 9:
                relative = target.relative_to(Path.cwd().resolve())
                owner = lab_owner(relative)
                if owner is not None and relative.is_relative_to(owner / "assets"):
                    if lab_owner(file) != owner:
                        bad.append(f"{file}: cross-lab assets reference {href}")
    return bad


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("check", type=int, choices=range(1, 10))
    parser.add_argument("--scope", choices=("tree", "all"), default="all")
    args = parser.parse_args()
    if args.check == 1:
        status = secrets(args.scope)
        print(f"{'FAIL' if status else 'PASS'}: check 1")
        return status
    checks = {
        2: lambda: identifiers(args.scope), 3: lambda: notebooks(args.scope),
        4: paths, 5: metadata, 6: lambda: content(6), 7: lab_metadata,
        8: lambda: content(8), 9: lambda: content(9),
    }
    bad = checks[args.check]()
    if bad:
        print("\n".join(bad))
    print(f"{'FAIL' if bad else 'PASS'}: check {args.check}")
    return 1 if bad else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError, subprocess.CalledProcessError) as error:
        # Never include source data or subprocess output in a shared diagnostic.
        print(f"ERROR: check not completed ({type(error).__name__}); inspect local input/tool state", file=sys.stderr)
        sys.exit(2)
