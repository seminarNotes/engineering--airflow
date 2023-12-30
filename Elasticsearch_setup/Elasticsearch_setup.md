# ElasticSearch Setup 
최초 작성일 : 2023-12-27  
마지막 수정일 : 2023-12-29
  
## 0. Overview
Windows 환경에서 ElasticSearch를 설치하고, 세팅하는 과정을 기록한다.

## Table of Contents
1. [Download setup file](#1.-Download-setup-file)
2. [Install with setup file](#2.-Install-with-setup-file)
3. [Execute_ElasticSearch](#3.-Execute-ElasticSearch)




## 1. Download setup file

ElasticSearch를 실행하기 위해서 ElasticSearch와 함께 Kibana를 설치해야 한다. Kibana는 ElasticSearch를 사용할 때, 대시보드를 사용할 수 있도록 GUI를 제공하는 소프트웨어다. 각 소프트웨어의 설치 파일은 아래에서 다운로드 할 수 있다.
```console
https://www.elastic.co/kr/downloads/elasticsearch
```

```console
https://www.elastic.co/kr/downloads/kibana
```

다운로드 이후, 작업 디렉토리에서 압축 파일을 푼다. 예를 들어, C드라이브 아래 작업 디렉토리(ELK, Elasticsearch, Logstash, Kibana의 줄임말)를 생성하고, zip 파일을 옮긴 후, 압축 파일을 푼다.

C:\ELK

참고로, 개발 및 환경을 세팅할 때, 경로에는 "한글"과 version을 나타내는 "x.x.x"과 같은 폴더/파일 이름은 생략하는 것을 강력히 권장한다. 필자는 elasticsearch와 kibana가 설치된 폴더의 경로를 아래와 같도록, 폴더 명을 각각 변경하였다.

C:\ELK\elasticsearch

C:\ELK\kibana


## 2. Install with setup file
Visual Studio Code를 이용해서 설치를 완료한다. 명령 프롬포트를 실행해서 작업 디렉토리를 열고(최상위 폴더를 ELK로 하고), Visual Stuido Code를 실행한다.
```console
C:\Users\seminarNotes>CD C:\ELK

C:\ELK>code .
```
Visual Studio Code와 함께 왼쪽 Explorer를 이용해서 elasticsearch.yml파일를 연다.
C:\ELK\elasticsearch\config\elasticsearch.yml

그리고 아래와 같은 문구를 추가한다.
```yaml
#config/elasticsearch.yml
cluster.name: cluster-test
node.name: cluster-test-node01

path:
  data: C:\ELK\elasticsearch\data
  logs: C:\ELK\elasticsearch\logs  

network.host: 127.0.0.1

discovery.type: "single-node"
xpack.security.enabled: false
```

다음으로 C:\ITStudy\ELK\elasticsearch\config\jvm.options 파일에 접속해서, -Xms5g/-Xmx5g의 부분의 주석을 해제하고, -Xms1g/-Xmx1g로 변경한다. 


```
## -Xms5g
## -Xmx5g
```

```
-Xms1g
-Xmx1g
```

해당 수정 부분은 elasticsearch를 사용할 때, 할당하는 메모리에 대한 세팅으로, 메모리에 대한 여유가 있는 유저는 -Xms5g/-Xmx5g 그대로 사용해도 무방하다.

또, C:\ITStudy\ELK\kibana\config\kibana.yml 파일에 접속하여, 맨 아래 아래와 같은 세팅값을 추가한다.

```yaml
#config/kibana.yml
server.port: 5601
server.host: localhost
server.publicBaseUrl: "http://localhost:5601"
elasticsearch.hosts: ["http://localhost:9200"]
```


## 3. Execute ElasticSearch
설치된 elasticsearch와 kibana는 아래 batch파일을 터미널을 통해 실행한다.
```console
c:\ELK\elasticsearch\bin\elasticsearch.bat

c:\ELK\kibana\bin\kibana.bat
```
설치와 실행을 점검하기 위해, elaticsearch는 http://localhost:9200 kibana는 http://localhost:5601 에 접속해서 확인한다.

