# Contributing to AKS Basic Workshop

Contributions to the workshop documentation and sample code are welcome.

## Contributor License Agreement

<!-- TODO: Maintainer confirmation required: CLA applicability and bot configuration. -->

## Code of Conduct

Read and follow the [Code of Conduct](./.github/CODE_OF_CONDUCT.md).

## Proposals

Discuss substantial changes with the maintainers before implementing them.
Include the affected lab and step, the relevant revision, your execution environment,
reproduction steps, and the expected and actual results.

Remove credentials, subscription and tenant IDs, personal resource identifiers,
customer data, and private information from logs and screenshots.
Report security vulnerabilities using [SECURITY.md](./SECURITY.md).
See [SUPPORT.md](./SUPPORT.md) for help and support information.

## Pull requests

Search the [pull requests](https://github.com/kyungtaak/AKSBasicWorkshop/pulls) for related changes.
Make your changes in a dedicated branch of your fork and keep unrelated local changes intact.
Submit the pull request to the `main` branch.
Use the target repository's pull request template when one exists.

Keep the change focused and describe any changes to lab behavior.
Preserve existing copyright notices, attribution, and third-party licenses.
Do not change licensing or rewrite shared history without maintainer approval.
Use follow-up commits when addressing review feedback.

## Workshop validation

This workshop uses the Azure portal and a local terminal. Follow the declared
Windows CMD or Bash examples and the [prerequisites](./01-prerequisites/README.md).
Do not add a notebook, devcontainer, or Codespaces track without maintainer approval.
Run the complete workshop in the declared portal and local environments when
validating changes to lab behavior. Cloud deployment, deletion, or paid execution
requires separate authorization.

Run the nine checks documented in [AGENTS.md](./AGENTS.md) from the repository root
using Git Bash or a Bash-based devcontainer.
The checks require gitleaks 8.19 or newer, Python 3.10 or newer,
and the dependencies in `scripts/requirements-workshop.txt`.
The equivalent Windows PowerShell commands are documented in [AGENTS.md](./AGENTS.md).
Record each command, its scope, commit SHA, exit status, and actual result.
A final `PASS` does not override an earlier error.
If a new repository has no Git history, report history checks as not run;
do not count a tree-only scan as a full history pass.

Keep validation logs and decision records in a confirmed Git-ignored local directory.
Share only redacted summaries in the pull request.

Automated checks do not replace a complete workshop run in the declared environment
or a review of screenshots for private information.
Leave `validated_on` blank until a person completes the workshop and provides the date.
Do not invent durations, cost estimates, or successful execution results.
List unresolved TODOs and policy decisions in the pull request.
