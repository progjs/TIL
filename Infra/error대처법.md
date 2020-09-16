### docker에서 container 삭제가 안될 때

docker를 중지했다가 다시 시작

```
$ sudo service docker stop

컨테이너 파일 확인하고 삭제
$ sudo ls /var/lib/docker/containers
$ sudo ls /var/lib/docker/containers/CONTAINER_ID

$ sudo service docker start

$ docker container ls -a
docker를 재시작해서 남은 garbage들 모두 삭제되었다
```



### 명령어 자체가 먹히지 않을 때

vagrant 재부팅

```
C:\docker>vagrant reload
```

- 가상환경을 다룰 때 cmd창을 사용하는 경우

  cmd창은 언제든지 닫아도 된다

- 그러나, 컴퓨터를 종료할 때에는 반드시 가상머신을 끄고 종료해야한다

  - vagrant 중지(종료) 명령어

  ```
  C:\docker> vagrant halt
  ```

  - VM VirtualBox에서 전원끄기

    머신 > 닫기 > 전원끄기

  ![image-20200915181200056](D:\TIL\img\image-20200915181200056.png)

  - 다시 가상머신 실행 할때 (vagrant) - cmd에서

    `vagrant up` : vagrant 생성 및 실행

    `vagrant ssh` : vagrant 접속

    - vagrant 접속이 VM VirtualBox에서 보이는 미리보기와 같은 것!



