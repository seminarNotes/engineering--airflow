
WSL은 Windows Subsystem for Linux로, Windows 운영체제에서 Linux를 동시에 사용할 수 있다.

## 설치
명령 프롬프트를 관리자 권한으로 실행해서 다음 명령을 입력한다.  
**PowerShell**
```console
wsl --install
```

## 기본적인 문법  
대부분의 Linux 활용 방법은 CLI(Command Line Interface)를 사용하는 것으로, 사용자가 특정 Command를 입력하면, 대응하는 동작을 하거나 값을 출력하는 식의 대화형 인터프리터이다. 따라서, 아이콘과 같은 시각적 정보를 활용하는 windows와 달리, 파일 관리와 프로그램 실행, 나아가 적절한 시스템을 구성하고 운영하기 위해선, Linux 환경에서 사용하는 다양한 명령어에 익숙해질 필요가 있다.


1. 유저 생성하기
만약 생성하고자 하는 유저의 이름이 "user_exam"인 경우, 아래와 같이 입력하여, 새로운 유저를 생성할 수 있다.
```console
sudo useradd -m -s /bin/bash user_exam
```
또, 새로운 유저의 비밀번호를 생성할 수 있다.
```console
sudo passwd user_exam
```

2. 유저 전환하기  
아래는 root에서 생성한 user_exam로 유저를 전환하는 방법으로 **su user_exam**을 입력한다. 이 때, su는 switch user을 의미한다.
전환 하기 전에는 계정이 root(root@DESKTOP_ABCDEFG)로 되어있지만, 전환 후에는 user_exam(user_exam@DESKTOP_ABCDEFG)으로 되어 있는 것을 확인할 수 있다.
```console
root@DESKTOP_ABCDEFG:~# su user_exam
user_exam@DESKTOP_ABCDEFG:/root$
```

3. 현재 디렉토리 확인
**pwd**는 "Print Working Directory"로 현재 작업 중인 디렉터리의 전체 경로를 출력한다. 예를 들어, user_exam으로 접속한 후, pwd를 입력하면, 다음과 같은 결과를 확인할 수 있다.
```console
user_exam@DESKTOP_ABCDEFG:~$ pwd
/home/user_exam
```
현재 home 폴더 내 user_exam 폴더에서 작업 중임을 의미한다.

**ls**는 "List"로 현재 디렉터리에 있는 파일 및 디렉터리 목록을 출력한다. 예를 들어,
```console
user_exam@DESKTOP_ABCDEFG:~$ ls
dir_01  dir_02  fil_01  fil_02
```
현재 user_exam 폴더 내 dir_01, dir_02, fil_01, fil_02가 있다는 것을 의미한다.

ls -al 
ls -l
ls -a

3. 디렉토리 변경하기


cd (change directory)
cd .. 한칸 올라가기 
cd df
최상위 디렉토리 = root
cd
mkdir 디렉토리 생성
touch 파일 생성
rm (-r) 파일 삭제
rm (-f) 강제 삭제
cp file1 file2 : file1을 file2로 파일 복사 
mv 파일 이동 / 파일 변경
mv file1 dir_1 : file1 -> dir_1 위치 이동
mv file1 file2 : file1 -> file3 이름 변경
mv A B B가 존재하면 이동, B가 존재하지 않으면 이름 변경

tar  파일 / 디렉토리를 압축 해제

tar cvf : 파일  압축 할 때
tar xvf : 압축 해제 할 때
tar cvf dir_1.tar dir_1
tar cvf [만들 압축 파일 명] [대상]
tar xvf dir_1.tar

//// 도커 & 에어플로우 서설치
docker 개념 이해 설치

WSL위에 도커 설치
