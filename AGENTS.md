# 워크샵 에이전트 작업 지침

## 리포 규칙

시크릿과 실제 리소스 식별자를 커밋하지 않는다. 실제 키는 로컬 실행에만 사용하고 문서에는 placeholder를 둔다. 미커밋 변경과 저자의 실습 내용을 보존한다.

랩은 루트의 `NN-kebab-name` 폴더에 단일 README로 둔다. 랩 전용 자산은 해당 랩의 `assets`에, 여러 랩에서 참조하는 것이 확인된 자산만 `shared-assets`에 둔다. 이미지 경로를 바꾸면 참조도 함께 수정한다. 내부 결정 시트와 검사 로그는 Git에서 제외된 `local-only`에 보관한다.

검사 구현의 [원본 MIT 고지](./scripts/LICENSE.md)를 보존한다. 이 고지는 복사한 검사 구현에 적용하며 워크샵 본문·이미지의 라이선스 전환을 승인하는 것은 아니다.

워크샵의 자체 작성 코드·실행 코드 예제에는 [MIT](./LICENSE.md), 문서 설명문에는 [CC BY-SA 4.0](./LICENSE-DOCS)을 적용한다. 이미지·스크린샷·타사 자료와 공식 정책 문안은 문서 라이선스 적용 범위에서 제외하며 기존 조건과 고지를 보존한다. 기여·지원·보안 안내는 승인한 거버넌스 파일을 따르고, 라이선스 적용 범위를 임의로 확대하지 않는다.

## 콘텐츠·노트북 스타일

한국어 안내와 실행 코드를 구분한다. 이 워크샵은 A형 문서 기준을 사용하는 포털·로컬 혼합형이며 `execution: [portal, local]`을 유지한다. 승인 없이 노트북, devcontainer 또는 Codespaces 트랙을 추가하지 않는다.

Windows CMD 코드는 `cmd`, Bash 코드는 `bash`, 두 셸에서 공통으로 쓰는 명령은 `console`로 표시한다. `%ACRNAME%`과 `$ACRNAME`을 혼용하지 않는다. manifest 수정은 줄 번호 대신 `kind`와 `metadata.name`으로 안내한다.

루트 README에는 전체 메타데이터를, 랩 README에는 `title`, `duration_minutes`, `last_updated`를 둔다. 일정은 L200~300, 이론·실습을 포함한 총 4시간이다. 사용자 요청에 따라 예상 시간은 이론 40분, 실습 180분, 휴식·질의응답 20분으로 배분했다. 랩별 예상 시간은 순서대로 20·35·25·30·25·30·15분이며 실측값과 구분한다. 비용과 실행 결과를 추정해서 확정하지 않는다. 노트북이 추가되는 경우 `outputs: []`, `execution_count: null`을 유지한다.

## 검증 하네스

검사 구현과 의존성은 이 저장소의 [검사 스크립트](./scripts/workshop_checks.py)와 [의존성 파일](./scripts/requirements-workshop.txt)을 사용한다. 설치한 skill 폴더를 실행 의존성으로 삼지 않는다. gitleaks 8.19 이상, Python 3.10 이상과 의존성 파일의 패키지가 필요하다. 도구 설치·업데이트는 승인받는다. 아래 명령은 워크샵 표준화 AI 지시문의 검사 9종 원문이며 Git Bash 또는 Bash 기반 devcontainer에서 저장소 루트 기준으로 실행한다.

Windows PowerShell에서는 승인한 로컬 가상 환경의 Python으로 같은 스크립트를 실행할 수 있다. 예를 들어 검사 1은 `& .\.venv\Scripts\python.exe -B -X utf8 .\scripts\workshop_checks.py 1`이며, 검사 번호를 1부터 9까지 순서대로 바꾼다. 매번 `$LASTEXITCODE`를 확인하고 실패하면 후속 검사를 실행하지 않는다. `.venv`와 검사 로그의 `local-only`는 Git 제외 여부를 확인한다.

검사 1~3은 현재 파일과 로컬 전체 refs의 이력을 검사한다. 전체 clone과 이관 대상 refs를 확인하며 shallow clone이나 커밋 없는 저장소를 이력 통과로 표시하지 않는다. 신규 골격과 정리 후 첫 커밋 전 점검에만 `--scope tree`를 사용하고 이력 검사는 미실행으로 보고한다.

종료 코드 0은 통과, 1은 검출, 2 이상은 입력·도구 오류다. 마지막 메시지가 PASS여도 앞 단계의 오류·검출을 확인한다. 명령·검사 범위·대상 커밋 SHA·미커밋 변경 여부·종료 코드와 원본 로그를 로컬 전용 기록에 남긴다. 현재 파일이나 검사 대상 SHA가 바뀌면 다시 검사한다.

검사 4~9는 현재 파일을 검사하며 `.git`, `node_modules`, `.venv`, `venv`, `__pycache__`를 제외한다. 검사 2~3도 현재 파일에서 같은 실행 환경 폴더를 제외하되 이력의 blob은 제외하지 않는다. Git에서 제외한 `local-only`의 파일은 자동으로 검사에서 제외되는 것이 아니므로 입력·검출 문제를 숨기기 위해 로그를 삭제하거나 검사 기준을 바꾸지 않는다.

식별자·이력 출력의 오탐은 저자가 확인한 정확한 경로·해시·근거만 `.workshop-scan-allowlist.json`에 기록한다. 시크릿 오탐은 `.gitleaks.toml`의 정확한 allowlist로 처리한다. `example` 문자열만으로 자동 제외하거나 실노출을 예외로 숨기지 않는다. 현재 노트북 출력은 예외로 허용하지 않는다.

자산 검사는 경로를 정규화해 다른 랩의 전용 자산 참조를 찾는다. 루트 `assets`는 다른 랩의 전용 자산으로 판정하지 않는다. 링크 검사는 파일 존재 여부를 확인하며 문서 앵커·외부 URL 응답 검증을 대신하지 않는다. 바이너리·미지원 주소와 스크린샷의 민감 정보는 별도로 검토하며, 자동 검사 통과를 실제 Azure 실행 검증이나 공개 승인으로 표시하지 않는다.

```bash
# 실패한 검사 뒤에는 진행하지 않는다.
set -e
# (1) 시크릿: working tree + 전체 이력
python3 scripts/workshop_checks.py 1
# (2) 개인 엔드포인트·구독/테넌트 ID: working tree + 전체 이력
python3 scripts/workshop_checks.py 2
# (3) 노트북 출력: 현재 제거 + 이력 검출 분류
python3 scripts/workshop_checks.py 3
# (4) 공백·비ASCII 경로
python3 scripts/workshop_checks.py 4
# (5) 루트 frontmatter: 필수 키·자료형·허용값·날짜
python3 scripts/workshop_checks.py 5
# (6) 상대 링크·이미지: Markdown 제목·참조형 링크·HTML 포함
python3 scripts/workshop_checks.py 6
# (7) 랩 frontmatter: 필수 키·자료형·날짜
python3 scripts/workshop_checks.py 7
# (8) 빈 이미지 alt-text
python3 scripts/workshop_checks.py 8
# (9) 다른 랩의 전용 assets 참조
python3 scripts/workshop_checks.py 9
```

## 백로그·DO NOT

- `validated_on`은 사람이 전체 실습을 완료한 날짜만 기록한다. 현재는 `status: draft`와 검증일 공란을 유지한다.
- 실제 진행 시간으로 세션별·랩별 예상 시간을 보정한다.
- 실제 포털·로컬 환경에서 E2E 검증을 수행하고 샘플 commit과 도구 버전을 기록한다.
- 스크린샷의 민감 정보와 최신 UI를 확인한다. 기존 이미지 파일의 내용은 승인 없이 바꾸거나 삭제하지 않는다.
- 원본 이력의 스크린샷 식별자 문제는 텍스트 검사로 해소되지 않는다. Azure-Samples 이관 전에는 원본을 보존한 별도 작업본의 스쿼시 계획을 승인받으며, 현재 이력을 임의로 재작성하거나 공개 준비 완료로 표시하지 않는다.
- CLA 적용·봇 설정과 도움 채널·지원 범위는 미확정이다. CONTRIBUTING과 SUPPORT의 TODO를 확인하고 확정 전에는 지원 보장이나 공개 준비 완료로 표시하지 않는다. 승인한 방침대로 Issues 링크를 추가하지 않으며 원격 Issues 설정도 변경하지 않는다.
- 삭제·분할·병합·이력 변경은 승인 없이 수행하지 않는다. 시크릿·실제 식별자 노출 발견 시 즉시 중단하고 값을 재출력하지 않는다.
- 검사 실패·미실행을 통과로 표시하지 않는다. 노트북이 없는 출력 검사 통과를 노트북 실행 검증으로 표현하지 않는다.
- 클라우드 배포·삭제, 유료 실행, 원격 push와 공개 전환을 자동으로 수행하지 않는다.
