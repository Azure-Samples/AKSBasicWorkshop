# 1. 준비 사항

### Docker Desktop 설치

이 실습에서는 로컬 환경에서 도커 이미지를 빌드할 수 있어야 합니다. 아래 단계를 통해 Docker Desktop을 구성합니다.

아래 가이드를 참고하여 각 OS에 맞는 Docker Desktop을 구성합니다.

- [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/)
- [Docker Desktop for Mac](https://docs.docker.com/desktop/setup/install/mac-install/)

> WSL(Windows Subsystem for Linux)은 Windows 10, 11에서 Linux 환경을 실행할 수 있도록 해주는 기능입니다. Docker Desktop은 WSL 2 버전과  Hyper-V 버전을 제공하고 있습니다. WSL 2 버전의 Docker Desktop 설치 시 Windows에서 WSL 2 기능을 활성화 해야 합니다.
> 

### Azure CLI 설치

아래 페이지를 참고하여 OS에 맞는 Azure CLI를 설치합니다. 이 실습에서는 Azure CLI 버전 2.0.53 이상이 필요합니다.

[https://learn.microsoft.com/ko-kr/cli/azure/install-azure-cli](https://learn.microsoft.com/ko-kr/cli/azure/install-azure-cli)

### Kubernetes CLI 설치

Kubernetes CLI, [`kubectl`](https://kubernetes.io/docs/reference/kubectl/)을 사용하여 Kubernetes 클러스터에 연결합니다. 명령을 로컬로 실행하는 경우 Azure CLI 또는 Azure PowerShell을 사용하여 `kubectl`을 설치할 수 있습니다.

Azure CLI가 설치된 터미널에서 아래 명령어를 사용하여 `kubectl`을 로컬로 설치합니다.

```bash
az aks install-cli
```