# Note1 : Setting Airflow  
최초 작성일 : 2023-12-21  
마지막 수정일 : 2023-12-27
  
## 0. Overview
Windows 환경에서 Airflow를 설치하고, 세팅하는 과정을 설명한다.

## Table of Contents
1. [Install WSL2 System in Windows](#1.-Install-WSL2-system-in-Windows)
2. [Install Docker Engine on WLS2](#2.-Install-Docker-Engine-on-WLS2)
3. [Install Airflow in Docker](#3.-Install-Airflow-in-Docker) 



## 1. Install WSL2 System in Windows
Windows 환경에서 명령 프롬프트(cmd)를 관리자 권한으로 실행한다. 이 후, **wsl --install**를 입력하고, 계정을 생성한다.

```console
wsl --install
```

## 2. Install Docker Engine on WLS2
wsl를 통해 home/user 디렉토리로 이동한 다음, 에러를 발생시키는 패키지를 먼저 삭제한다.
```console
$ for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

설치 전, 설치된 패키지 목록을 최신 상태로 업데이트 한다.
```console
sudo apt-get update
```
이 후, 필요한 패키지를 차례대로 설치한다.
```console
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```
아래는 파일에 대한 권한을 변경하는 명령어로, 유저에게 docker.gpg 파일에 대한 읽기 권한을 부여한다.
```console
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```
마지막으로, 저장소를 통해 Docker를 설치하고, 업데이트 할 수 있도록, Docker의 공식 APT 패키지 저장소를 시스템에 추가한다.
```console
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
필요한 패키지를 모두 성공적으로 설치하였으면, 최신 상태로 업데이트 한다.
```console
sudo apt-get update
```
아래는 Docker와 관련된 패키지를 설치하는 것으로, docker-ce(Docker Community Edition), docker-ce-cil(Docker Command Line Interface), containerd.io(컨테이너 실행과 관리를 담당하는 런타임), docker-buildx-plugin, docker-compose-plugin(플러그인)을 차례대로 설치한다.
```console
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
Docker 프로그램을 실행하는 것으로 다음 명령어를 입력한다.
```console
sudo service docker start
```
마지막으로, "sudo docker run hello-world"를 입력하여 에러가 발생하지 않으면서, 정상적으로 설치되었음을 확인할 수 있다.
```console
sudo docker run hello-world
```

위 설치 과정은 다음 공식 홈페이지에서 자세한 설명을 확인할 수 있다.  



마지막 수정일 기준,  

https://docs.docker.com/engine/install/ubuntu/
## 3. Install Airflow in Docker

먼저 docker-compose에서 airflow를 세팅하고 실행하는 yaml파일을 다운한다.
```console
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.0/docker-compose.yaml'
```

이후 yaml이 있는 동일한 디렉토리에 airflow 실행에 필요한 추가적인 디렉토리 (dags, logs, plugins, config)과 환경 세팅에 대한 파일 env를 생성한다.
```console
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

데이터 베이스 마이그레이션과 초기 유저 계정을 생성하는 등의 애플리케이션 실행 전, 필요한 초기 설정을 수행하기 위해 다음 명령어를 입력한다.

```console
sudo docker compose up airflow-init
```
