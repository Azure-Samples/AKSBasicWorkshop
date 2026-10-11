---
title: 01. 준비 사항
duration_minutes: 20
last_updated: 2026-10-11
---

# 01. 준비 사항

## 개요와 학습 목표

로컬에서 컨테이너를 빌드하고 AKS에 연결할 도구를 준비합니다.

## 사전 요구사항

Docker Desktop을 실행할 수 있는 Windows 또는 macOS 환경과 도구 설치 권한이 필요합니다. Azure 포털에 로그인할 수 있는 구독과 실습 리소스 생성 권한도 준비합니다.

## 예상 소요 시간

약 20분을 예상합니다. 도구 설치와 버전 확인을 포함한 계획값이며 실측값은 아닙니다. Docker Desktop 최초 설치·WSL 구성·재부팅이 필요하면 추가 시간을 확보합니다.

## 실습 단계

### Git 준비

샘플 애플리케이션 복제에 Git을 사용합니다. 설치되어 있지 않다면 [Git 설치 안내](https://git-scm.com/downloads)를 따릅니다.

### Docker Desktop 설치

이 실습에서는 로컬 환경에서 Docker 이미지를 빌드할 수 있어야 합니다. 아래 안내에 따라 Docker Desktop을 구성합니다.

아래 가이드를 참고하여 각 OS에 맞는 Docker Desktop을 구성합니다.

- [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/)
- [Docker Desktop for Mac](https://docs.docker.com/desktop/setup/install/mac-install/)

> WSL(Windows Subsystem for Linux)은 Windows 10, 11에서 Linux 환경을 실행할 수 있도록 해주는 기능입니다. Docker Desktop은 WSL 2 버전과  Hyper-V 버전을 제공하고 있습니다. WSL 2 버전의 Docker Desktop 설치 시 Windows에서 WSL 2 기능을 활성화 해야 합니다.
>

### Azure CLI 설치

아래 공식 설치 안내에서 OS에 맞는 Azure CLI를 설치합니다.

[https://learn.microsoft.com/ko-kr/cli/azure/install-azure-cli](https://learn.microsoft.com/ko-kr/cli/azure/install-azure-cli)

### Kubernetes CLI 설치

Kubernetes CLI, [`kubectl`](https://kubernetes.io/docs/reference/kubectl/)을 사용하여 Kubernetes 클러스터에 연결합니다. 명령을 로컬로 실행하는 경우 Azure CLI 또는 Azure PowerShell을 사용하여 `kubectl`을 설치할 수 있습니다.

Azure CLI가 설치된 터미널에서 아래 명령어를 사용하여 `kubectl`을 로컬로 설치합니다.

```console
az aks install-cli
```

### 터미널 선택

명령은 로컬 터미널에서 실행합니다. Windows CMD 예시는 `cmd`, Bash 예시는 `bash`로 표시합니다. `console`은 CMD와 Bash에서 같은 형태로 실행하는 명령입니다. PowerShell에서는 CMD의 `%ACRNAME%` 문법이 동작하지 않으므로 CMD를 열거나 Bash 예시를 사용할 수 있는 환경을 선택합니다.

## 검증

Docker Desktop을 실행한 뒤 로컬 터미널에서 다음 명령을 실행합니다.

```console
git --version
docker version
docker compose version
az version
kubectl version --client
```

각 도구의 버전이 출력되고 `docker version`에 Client와 Server 정보가 모두 표시되면 다음 랩으로 진행합니다.

## 정리

도구는 다음 랩에서도 사용하므로 유지합니다. 클라우드 리소스 정리는 [마지막 랩](../07-cleanup/README.md)에서 진행합니다.

## 트러블슈팅

| 증상 | 확인과 조치 |
|---|---|
| 명령을 찾을 수 없음 | 해당 도구를 설치했는지 확인하고 새 터미널을 엽니다. 설치 경로가 PATH에 포함되어야 합니다. |
| Docker Server 연결 오류 | Docker Desktop을 실행하고 Engine이 준비될 때까지 기다린 뒤 `docker version`을 다시 실행합니다. |
| Windows에서 Docker Desktop이 시작되지 않음 | Docker 설치 안내의 WSL 2·가상화 요구사항을 확인합니다. |
| PowerShell에서 `%ACRNAME%`이 그대로 출력됨 | Windows CMD를 열고 CMD 예시를 사용하거나 Bash 환경에서 Bash 예시를 사용합니다. |

## 이전·다음

[워크샵 홈](../README.md) · [다음: 샘플 애플리케이션 구성](../02-sample-application/README.md)