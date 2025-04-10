# 3. 컨테이너 레지스트리 만들기

컨테이너 레지스트리(Azure Container Registry; ACR)은 컨테이너 이미지를 위한 프라이빗 레지스트리입니다. 프라이빗 컨테이너 레지스트리를 사용하면 애플리케이션과 사용자 지정 코드를 안전하게 빌드하고 배포할 수 있습니다.

## 컨테이너 레지스트리 만들기

### 리소스 그룹 만들기

Azure의 모든 리소스는 생성할 때 과금이 청구될 구독과 리소스들의 논리 컨테이너인 리소스 그룹을 지정해줘야 합니다.

먼저 [Azure 포털](https://portal.azure.com/)로 이동합니다.

1. 서비스 검색 상자에서 `리소스 그룹`을 입력합니다.
2. 왼쪽 상단의 `만들기` 버튼을 클릭합니다.
3. 아래와 같이 구성하고 하단의 `검토 + 만들기` 버튼을 클릭하고 `만들기` 버튼을 클릭하여 리소스를 생성합니다.
    - 구독 : 사용할 구독 선택
    - 리소스 그룹 이름 : AKSWorkshopResourceGroup
    - 지역 : (Asia Pacific) Korea Central

### 컨테이너 레지스트리 만들기

1. 서비스 검색 상자에서 `컨테이너 레지스트리`를 입력합니다.
2. 왼쪽 상단의 `만들기` 버튼을 클릭합니다.
3. 앞서 선택한 구독과 생성한 `AKSWorkshopResourceGroup` 리소스 그룹을 선택하고 아래와 같이 구성합니다.
    - 레지스트리 이름 : <alias>samplerepo
    - 위치 : Korea Central
    - 가격 책정 플랜 : 표준
4. 나머지 구성은 그대로 두고 `검토 + 만들기` 버튼을 클릭하고 `만들기` 버튼을 클릭하여 리소스를 생성합니다.

### 컨테이너 이미지를 레지스트리에 푸시

1. 로컬에서 터미널을 열어 docker images 명령어를 입력하여 로컬에 빌드된 이미지를 확인합니다.
    
    ![image.png](./images/image.png)
    
2. 이미지가 정상적으로 빌드되어 있다면, rabbitmq를 제외하고 `aks-store-demo` 세 개의 이미지를 푸시할 것입니다. 이미지가 빌드되어 있지 않다면 아래 명령어를 로컬 터미널(샘플 애플리케이션 경로)에서 실행하여 이미지를 빌드합니다.
    
    ```bash
    docker compose -f docker-compose-quickstart.yml build
    ```
    
3. 레지스트리 이름을 환경 변수로 등록합니다. **(이 실습에서는 cmd 기준으로 진행됩니다. 각 OS에 맞게 명령어를 수정하여 실행해야 합니다.)**
    - Windows (cmd)
        
        ```bash
        set ACRNAME=<alias>samplerepo
        
        # 사용시 %ACRNAME%
        ```
        
    - Linux
        
        ```bash
        export ACRNAME=<alias>samplerepo
        
        # 사용시 $ACRNAME
        ```
        
4. 레지스트리에 로그인하기 위해 로컬 터미널에서 아래 명령어를 실행합니다.
    
    ```bash
    az login
    # 여러 개의 테넌트를 사용줄일 때 테넌트를 지정하여 로그인
    # az login --tenant <디렉터리 ID>
    az acr login --name %ACRNAME%
    ```
    
5. ACR에 이미지를 업로드하기 위해서는 레지스트리의 로그인 서버 주소를 사용하여 이미지에 태그를 지정해야 합니다. 아래 명령어를 사용하여 각 이미지에 태그를 지정해 줍니다.
    
    ```bash
    # docker tag <기존 이미지 레지스트리>:<기존 이미지 태그> <로그인 서버 주소>/<이미지 레지스트리>:<이미지 태그>
    docker tag aks-store-demo-order-service %ACRNAME%.azurecr.io/aks-store-demo/order-service
    docker tag aks-store-demo-store-front %ACRNAME%.azurecr.io/aks-store-demo/store-front
    docker tag aks-store-demo-product-service %ACRNAME%.azurecr.io/aks-store-demo/product-service
    ```
    
6. 레지스트리에 이미지를 푸시합니다.
    
    ```bash
    docker push %ACRNAME%.azurecr.io/aks-store-demo/order-service
    docker push %ACRNAME%.azurecr.io/aks-store-demo/store-front
    docker push %ACRNAME%.azurecr.io/aks-store-demo/product-service
    ```
    
7. Azure 포털로 이동하여 컨테이너 레지스트리 화면으로 이동합니다.
8. 레지스트리 목록에서 생성한 `<alias>samplerepo` 를 클릭합니다.
9. 왼쪽의 블레이드에서 `서비스`를 클릭하고 `리포지토리`를 클릭하여 업로드된 이미지를 확인합니다.
    
    ![image.png](./images/image%201.png)