`aws-sdk`가 없습니다 error

```
"predeploy": "zip -r Lambda-Deployment.zip * -x *.zip *.log",
```

위에서 *.json 있는지 확인(없어야 함)



`handler`가 없습니다 error

```
export.handler 
```

위에서 handler 오타났는지 확인 (index.js)



### s3 elasticbeanstalk 버킷 삭제 방법

![image-20201027153846440](E:\aws\images\버킷삭제)

버킷 정책에서 `"Effect": "Deny"` 때문에 삭제할수 없는 것이다.

`Allow`로 바꾸거나 상단오른쪽에 삭제를 누르고

버킷목록에서 해당 버킷을 삭제하면 된다.





##### API gateway 생성 (이름 24-Video)

- 리소스 user-token 에 메서드 GET 생성

- 통합요청에서 lambda함수 통합하고 매핑 템플릿에 application/json 추가

  ```
  {
      "authToken" : "$input.params('Authorization')"
  }
  ```

- api CORS 활성화 후 api 배포

- api gateway ARN을 24-video/js/config.js 에 추가

  ```
      apiBaseUrl: 'https://90wtzlq1ij.execute-api.us-east-1.amazonaws.com/dev'
  ```

  

- lambda함수 테스트

  ```
  {
    "authorizationToken": "Bearer eyJhbGciOiJ...id토큰"
  }
  ```

  - error 수정을 위해 auth0-> advanced setting에서 HS256으로 변경

    ![image-20201028015731275](E:\aws\images\hs256)

