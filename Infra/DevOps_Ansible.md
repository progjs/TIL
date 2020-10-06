## Vagrantfile로 인프라를 구성

### 장점

- 환경 구축 작업이 간소화
- 환경 공유 용이
- 환경 파악 용이
- 팀 차원의 유지보수 가능



### Infra를 보다 효율적으로  관리하기 위해 개선해야 할 점

- 구축절차를 기술하는 사람에 따라 다양하게
- 구축된 환경에 대한 추가 설정이 불가함
- 다양한 환경에 적용하기 어려움



### 인프라 구성 관리 도구

- 선언적
- 추상화
- 수렴화
- 멱등성 : 항상 동일한 환경...?
- 간소화



> 1. vagrant로 서버를 구축
>
> 2. ansible로 shell script가 아닌 role별로 옵션을 줘서 **효율적으로 환경을 구축**
>
> 3. serverspec으로 구축된 환경을 자동적으로 test하는 테스트케이스를 생성
>
>    [ansible-playbook][https://github.com/devops-book/ansible-playbook-sample.git] 소스코드 활용
>
> 4. 테스트 결과를 HTML로 볼 수 있도록 설정

## Ansible 사용법

#### Ansible (앤서블)

: Python으로 만들어진 **인프라 구성 관리 도구**



### Ansible을 사용하는 이유

- 환경설정, 구축절차를 통일된 형식으로 기술

- 매개변수 등 환경의 차이를 관리

- 실행 전에 변경되는 부분을 파악



### 설치

1. nginx 설치 확인

   ``` 
   C:\HashiCorp\WorkDir> vagrant ssh
   
   [vagrant@demo ~]$ systemctl status nginx
   ● nginx.service - The nginx HTTP and reverse proxy server
      Loaded: loaded 
      	:
   ```

   

2. ansible 설치 & 버전 확인

   ```
   [vagrant@demo ~]$ sudo systemctl stop nginx.service
   [vagrant@demo ~]$ sudo yum install -y epel-release
   [vagrant@demo ~]$ sudo yum install -y ansible
   [vagrant@demo ~]$ ansible --version
   ansible 2.9.10
   	:
   ```

   

3. ansible 명령으로 nginx 기동

   ```
   [vagrant@demo ~]$ sudo sh -c "echo \"localhost\" >> /etc/ansible/hosts"		⇐ 서버 인번터리에 localhost를 추가
   [vagrant@demo ~]$ cat /etc/ansible/hosts
   # This is the default ansible 'hosts' file.
   	:
   localhost
   ```

   - 명령어 해석 - 이스케이프

     의미 문자에서 의미를 제거하고, 문자 그대로만으로 인식하도록 변형해주는 문자

     >  의미 문자(= 메타 문자) : 어떤 기능에서 특별한 의미를 가지는 문자(ex 특수 기호)

     "를 사용하기 위해 앞에 \를 추가

     ```
      \"localhost\"
     ```

   ```
   [vagrant@demo ~]$ ansible localhost -b -c local -m service -a "name=nginx state=started"
   localhost | CHANGED => {
       "ansible_facts": {
           "discovered_interpreter_python": "/usr/bin/python"
       },
       "changed": true,
       "name": "nginx",
       "state": "started",
       "status": {
          :
       }
   }
   ```

   - ` "changed": true.`  중지 상태 => 실행 상태로 변경

   - 명령어 해석

     ```
     $ ansible localhost -b -c local -m service -a "name=nginx state=started"
     ```

     ` localhost ` inventory file에 기재되어있는 서버 중 명령어를 수행할 대상

     `-b` 원격 실행되는 대상 서버의 사용자 (-b = root)

     `-c local `  대상 서버가 자기 자신(localhost)이므로 SSH를 사용하지 않고 local로 연결

     `-m service` service 모듈 이용

     `-a "name=nginx state=started"` 모듈의 추가 인자

     

4. nginx 상태 확인

   ```
   [vagrant@demo ~]$ systemctl status nginx.service
   ● nginx.service - The nginx HTTP and reverse proxy server
      Loaded: loaded (/usr/lib/systemd/system/nginx.service; disabled; vendor preset: disabled)
      Active: active (running) since Thu 2020-09-10 01:59:59 UTC; 7min ago
     Process: 3473 ExecStart=/usr/sbin/nginx (code=exited, status=0/SUCCESS)
     Process: 3469 ExecStartPre=/usr/sbin/nginx -t (code=exited, status=0/SUCCESS)
     Process: 3467 ExecStartPre=/usr/bin/rm -f /run/nginx.pid (code=exited, status=0/SUCCESS)
    Main PID: 3474 (nginx)
      CGroup: /system.slice/nginx.service
              ├─3474 nginx: master process /usr/sbin/nginx
              ├─3475 nginx: worker process
              └─3476 nginx: worker process
   ```

   - Active: active (running)

     

5. nginx가 실행 상태일 때 ansible 명령을 실행

   ```
   [vagrant@demo ~]$ ansible localhost -b -c local -m service -a "name=nginx state=started"
   localhost | SUCCESS => {
       "ansible_facts": {
           "discovered_interpreter_python": "/usr/bin/python"
       },
       "changed": false,
       "name": "nginx",
       "state": "started",
       "status": {
       	:
       }
   }
   ```

   - `"changed": false,` 이미 실행 상태였기 때문에, 변화 없음





## Ansible-playbook 



inventory file은 `/etc/ansible/hosts`를 사용하지만 `-i`옵션으로 직접 지정도 가능

```
[vagrant@demo ansible-playbook-sample]$ cat development
[development-webservers]
localhost

[webservers:children]
development-webservers

[vagrant@demo ansible-playbook-sample]$ cat production
[production-webservers]
localhost

[webservers:children]
production-webservers
```

사용하는 server를 다르게 지정할 수 있다.

(현재는 둘다 webservers 사용)



- role 별로 실행될 내용을 담고 있는 `dir` 목록

  ```
  [vagrant@demo ansible-playbook-sample]$ ls ./roles/
  common  jenkins  nginx  serverspec  serverspec_sample
  ```

  

- common role이 수행해야 할 내용 정의

  ```
  [vagrant@demo ansible-playbook-sample]$ ls ./roles/common/tasks/
  main.yml
  
  [vagrant@demo ansible-playbook-sample]$ cat ./roles/common/tasks/main.yml
  ---
  # tasks file for common
  - name: install epel
    yum: name=epel-release state=installed
  ```

  

- nginx role이 수행해야 할 내용을 `main.yml` 파일에 정의

  ```
  [vagrant@demo ansible-playbook-sample]$ cat ./roles/nginx/tasks/main.yml
  
  ---
  # tasks file for nginx
  - name: install nginx
    yum: name=nginx state=installed
  
  - name: replace index.html
    template: src=index.html.j2 dest=/usr/share/nginx/html/index.html
  
  - name: nginx start
    service: name=nginx state=started enabled=yes
  ```

  - `install nginx` 라는 task가 하는 일

    `nginx`라는 모듈을 `installed` 상태로 만든다.



- dry-run 모드 : 실행한 것처럼 결과 미리보기 `--check`

  - `./roles/nginx/templates/index.html.j2` 파일 내용 변경

    ```
    HELLO, {{ env }} ansible !!!	
    ```

  ```
  [vagrant@demo ansible-playbook-sample]$ ansible-playbook -i development
  site.yml --check --diff
  [WARNING]: Invalid characters were found in group names but not replaced, use
  -vvvv to see details
  
  PLAY [webservers] **************************************************************
  
  TASK [Gathering Facts] *********************************************************
  ok: [localhost]
  
  TASK [common : install epel] ***************************************************
  ok: [localhost]
  
  TASK [install nginx] ***********************************************************
  ok: [localhost]
  
  TASK [nginx : replace index.html] **********************************************
  --- before: /usr/share/nginx/html/index.html
  +++ after: /home/vagrant/.ansible/tmp/ansible-local-27336TVc0hn/tmpoFkyXB/index.html.j2
  @@ -1 +1 @@
  -hello, production ansible
  +HELLO, development ansible !!!
  
  changed: [localhost]
  
  TASK [nginx start] *************************************************************
  ok: [localhost]
  
  PLAY RECAP *********************************************************************
  localhost                  : ok=5    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
  ```

  

## Serverspec으로 인프라 구축 테스트 자동화

1. ruby 2.7 설치 (최신버전으로 update하기 위해)

2. default를 ruby 2.0 => ruby 2.7로 변경 

   - rvm 사용
   - root의 ruby 버전도 변경 (link를 2.7 버전으로 연결)

3. serverspec 설치

4. `serverspec-init`

5. sample_spec.rb 파일 확인

   테스트하기 위한 코드

   ```ruby
   [vagrant@demo ansible-playbook-sample]$ cat spec/localhost/sample_spec.rb
   require 'spec_helper'
   
   describe package('httpd'), :if => os[:family] == 'redhat' do
     it { should be_installed }
   end
   
   describe package('apache2'), :if => os[:family] == 'ubuntu' do
     it { should be_installed }
   end
   
   describe service('httpd'), :if => os[:family] == 'redhat' do
     it { should be_enabled }
     it { should be_running }
   end
   
   describe service('apache2'), :if => os[:family] == 'ubuntu' do
     it { should be_enabled }
     it { should be_running }
   end
   
   describe service('org.apache.httpd'), :if => os[:family] == 'darwin' do
     it { should be_enabled }
     it { should be_running }
   end
   ```

   

6. serverspec으로 테스트 실행

   ```
   [vagrant@demo ansible-playbook-sample]$ rake spec
   /usr/local/rvm/rubies/ruby-2.7.0/bin/ruby -I/usr/local/rvm/rubies/ruby-2.7.0/lib/ruby/gems/2.7.0/gems/rspec-support-3.9.3/lib:/usr/local/rvm/rubies/ruby-2.7.0/lib/ruby/gems/2.7.0/gems/rspec-core-3.9.2/lib /usr/local/rvm/rubies/ruby-2.7.0/lib/ruby/gems/2.7.0/gems/rspec-core-3.9.2/exe/rspec --pattern spec/localhost/\*_spec.rb
   
   Package "httpd"
     is expected to be installed (FAILED - 1)
   
   Service "httpd"
     is expected to be enabled (FAILED - 2)
     is expected to be running (FAILED - 3)
   
   Port "80"
     is expected to be listening
   
   Failures:
   
     1) Package "httpd" is expected to be installed
        On host `localhost'
        Failure/Error: it { should be_installed }
          expected Package "httpd" to be installed
          /bin/sh -c rpm\ -q\ httpd
          package httpd is not installed
   
        # ./spec/localhost/sample_spec.rb:4:in `block (2 levels) in <top (required)>'
   
     2) Service "httpd" is expected to be enabled
        On host `localhost'
        Failure/Error: it { should be_enabled }
          expected Service "httpd" to be enabled
          /bin/sh -c systemctl\ --quiet\ is-enabled\ httpd
   
        # ./spec/localhost/sample_spec.rb:12:in `block (2 levels) in <top (required)>'
   
     3) Service "httpd" is expected to be running
        On host `localhost'
        Failure/Error: it { should be_running }
          expected Service "httpd" to be running
          /bin/sh -c systemctl\ is-active\ httpd
          unknown
   
        # ./spec/localhost/sample_spec.rb:13:in `block (2 levels) in <top (required)>'
   
   Finished in 0.18234 seconds (files took 1.32 seconds to load)
   4 examples, 3 failures
   
   Failed examples:
   
   rspec ./spec/localhost/sample_spec.rb:4 # Package "httpd" is expected to be installed
   rspec ./spec/localhost/sample_spec.rb:12 # Service "httpd" is expected to be enabled
   rspec ./spec/localhost/sample_spec.rb:13 # Service "httpd" is expected to be running
   
   /usr/local/rvm/rubies/ruby-2.7.0/bin/ruby -I/usr/local/rvm/rubies/ruby-2.7.0/lib/ruby/gems/2.7.0/gems/rspec-support-3.9.3/lib:/usr/local/rvm/rubies/ruby-2.7.0/lib/ruby/gems/2.7.0/gems/rspec-core-3.9.2/lib /usr/local/rvm/rubies/ruby-2.7.0/lib/ruby/gems/2.7.0/gems/rspec-core-3.9.2/exe/rspec --pattern spec/localhost/\*_spec.rb failed
   ```



## Ansible로 Serverspec에서 사용하는 테스트케이스(_spec.rb)를 자동으로 생성

1. site.yml 에서 `serverspec_sample` 주석 해제

   ```
   ---
   - hosts: webservers
     become: yes
     connection: local
     roles:
       - common
       - nginx
       - serverspec
       - serverspec_sample
   #    - jenkins
   ```

2. severspec_sample role 정의 파일 확인

   - task 정의

   ```
   [vagrant@demo ansible-playbook-sample]$ cat ./roles/serverspec_sample/tasks/main.yml
   ---
   # tasks file for serverspec_sample
   - name: distribute serverspec suite
     copy: src=serverspec_sample dest={{ serverspec_base_path }}
   
   - name: distribute spec file
     template: src=web_spec.rb.j2 dest={{ serverspec_path }}/spec/localhost/web_spec.rb
   ```

   -  task에서 사용하는 변수 정의 

   ```
   [vagrant@demo ansible-playbook-sample]$ cat ./roles/serverspec_sample/vars/main.yml
   serverspec_base_path: "/tmp"
   serverspec_path: "{{ serverspec_base_path }}/serverspec_sample"
   ```

   - template 정의

   ```
   [vagrant@demo ansible-playbook-sample]$ cat ./roles/serverspec_sample/templates/web_spec.rb.j2
   require 'spec_helper'
   
   describe package('nginx') do
     it { should be_installed }
   end
   
   describe service('nginx') do
     it { should be_enabled }
     it { should be_running }
   end
   
   describe port(80) do
     it { should be_listening }
   end
   
   describe file('/usr/share/nginx/html/index.html') do
     it { should be_file }
     it { should exist }
     its(:content) { should match /^Hello, {{ env }} ansible!!$/ }
   end
   ```

3. ansible-playbook으로 spec 파일(테스트 케이스 정의 파일)을 배포

   ```
   [vagrant@demo ansible-playbook-sample]$ ansible-playbook -i development site.yml
   [WARNING]: Invalid characters were found in group names but not replaced, use
   -vvvv to see details
   
   PLAY [webservers] ***************************************************************
   
   TASK [Gathering Facts] **********************************************************
   ok: [localhost]
   
   	:
   
   TASK [serverspec_sample : distribute serverspec suite] **************************
   changed: [localhost]
   
   TASK [serverspec_sample : distribute spec file] *********************************
   changed: [localhost]
   
   PLAY RECAP **********************************************************************
   localhost                  : ok=9    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
   ```

4. spec 파일(테스트케이스 정의) 생성 확인

   ```
   [vagrant@demo ansible-playbook-sample]$ cat /tmp/serverspec_sample/spec/localhost/web_spec.rb
   require 'spec_helper'
   
   describe package('nginx') do
     it { should be_installed }
   end
   
   describe service('nginx') do
     it { should be_enabled }
     it { should be_running }
   end
   
   describe port(80) do
     it { should be_listening }
   end
   
   describe file('/usr/share/nginx/html/index.html') do
     it { should be_file }
     it { should exist }
     its(:content) { should match /^Hello, development ansible!!$/ }
   end
   ```

5. (ansible을 이용해서 자동으로 생성한) spec 파일로 테스트 실행

   - 앞에서 수정했던 `index.html.j2` 파일을 동일하게 수정

   ```
   [vagrant@demo ansible-playbook-sample]$ cat ~/ansible-playbook-sample/roles/nginx/templates/index.html.j2
   HELLO, {{ env }} ansible !!!				
   
   [vagrant@demo ansible-playbook-sample]$ vi ~/ansible-playbook-sample/roles/nginx/templates/index.html.j2
   Hello, {{ env }} ansible!!
   ```

   - 수정한 템플릿에 맞춰 새로 index.html 생성

   ```
   [vagrant@demo ansible-playbook-sample]$ ansible-playbook -i development site.yml
   [WARNING]: Invalid characters were found in group names but not replaced, use -vvvv to see details
   
   PLAY [webservers] *********************************************************************************
   
   TASK [Gathering Facts] ****************************************************************************
   ok: [localhost]
   
   	:
   
   TASK [nginx : replace index.html] *****************************************************************
   changed: [localhost]
   
   	:
   
   PLAY RECAP ****************************************************************************************
   localhost                  : ok=9    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
   ```

   - 테스트 실행 : `rake spec`

   ```
   [vagrant@demo ansible-playbook-sample]$ cd /tmp/serverspec_sample/
   
   [vagrant@demo serverspec_sample]$ rake spec
   /usr/local/rvm/rubies/ruby-2.7.0/bin/ruby -I/usr/local/rvm/rubies/ruby-2.7.0/lib/ruby/gems/2.7.0/gems/rspec-support-3.9.3/lib:/usr/local/rvm/rubies/ruby-2.7.0/lib/ruby/gems/2.7.0/gems/rspec-core-3.9.2/lib /usr/local/rvm/rubies/ruby-2.7.0/lib/ruby/gems/2.7.0/gems/rspec-core-3.9.2/exe/rspec --pattern spec/localhost/\*_spec.rb
   
   Package "nginx"
     is expected to be installed
   
   Service "nginx"
     is expected to be enabled
     is expected to be running
   
   Port "80"
     is expected to be listening
   
   File "/usr/share/nginx/html/index.html"
     is expected to be file
     is expected to exist
     content
       is expected to match /^Hello, development ansible!!$/
   
   Finished in 0.10557 seconds (files took 0.41014 seconds to load)
   7 examples, 0 failures		
   ```

6. nginx를 중지하고 테스트를 실행해보기 - 테스트 fail 예상

   ```
   [vagrant@demo serverspec_sample]$ sudo systemctl stop nginx.service
   
   [vagrant@demo serverspec_sample]$ systemctl status nginx.service
   ● nginx.service - The nginx HTTP and reverse proxy server
      Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; vendor preset: disabled)
      Active: inactive (dead) since Thu 2020-09-10 08:12:46 UTC; 21s ago
    Main PID: 25832 (code=exited, status=0/SUCCESS)
   
   [vagrant@demo serverspec_sample]$ rake spec
   /usr/local/rvm/rubies/ruby-2.7.0/bin/ruby -I/usr/local/rvm/rubies/ruby-2.7.0/lib/ruby/gems/2.7.0/gems/rspec-support-3.9.3/lib:/usr/local/rvm/rubies/ruby-2.7.0/lib/ruby/gems/2.7.0/gems/rspec-core-3.9.2/lib /usr/local/rvm/rubies/ruby-2.7.0/lib/ruby/gems/2.7.0/gems/rspec-core-3.9.2/exe/rspec --pattern spec/localhost/\*_spec.rb
   
   Package "nginx"
     is expected to be installed
   
   Service "nginx"
     is expected to be enabled
     is expected to be running (FAILED - 1)
   
   Port "80"
     is expected to be listening (FAILED - 2)
   
   File "/usr/share/nginx/html/index.html"
     is expected to be file
     is expected to exist
     content
       is expected to match /^Hello, development ansible!!$/
   
   Failures:
   
     1) Service "nginx" is expected to be running
        On host `localhost'
        Failure/Error: it { should be_running }
          expected Service "nginx" to be running
          /bin/sh -c systemctl\ is-active\ nginx
          inactive
   
        # ./spec/localhost/web_spec.rb:9:in `block (2 levels) in <top (required)>'
   
     2) Port "80" is expected to be listening
        On host `localhost'
        Failure/Error: it { should be_listening }
          expected Port "80" to be listening
          /bin/sh -c ss\ -tunl\ \|\ grep\ -E\ --\ :80\\\
   
        # ./spec/localhost/web_spec.rb:13:in `block (2 levels) in <top (required)>'
   
   Finished in 0.11722 seconds (files took 0.41031 seconds to load)
   7 examples, 2 failures
   
   Failed examples:
   
   rspec ./spec/localhost/web_spec.rb:9 # Service "nginx" is expected to be running
   rspec ./spec/localhost/web_spec.rb:13 # Port "80" is expected to be listening
   
   /usr/local/rvm/rubies/ruby-2.7.0/bin/ruby -I/usr/local/rvm/rubies/ruby-2.7.0/lib/ruby/gems/2.7.0/gems/rspec-support-3.9.3/lib:/usr/local/rvm/rubies/ruby-2.7.0/lib/ruby/gems/2.7.0/gems/rspec-core-3.9.2/lib /usr/local/rvm/rubies/ruby-2.7.0/lib/ruby/gems/2.7.0/gems/rspec-core-3.9.2/exe/rspec --pattern spec/localhost/\*_spec.rb failed
   ```

7. 테스트 결과를 HTML 로 출력

   ```
   [vagrant@demo serverspec_sample]$ sudo gem install coderay
   
   [vagrant@demo serverspec_sample]$ rake spec SPEC_OPTS="--format html" > ~/result.html
   /usr/local/rvm/rubies/ruby-2.7.0/bin/ruby -I/usr/local/rvm/rubies/ruby-2.7.0/lib/ruby/gems/2.7.0/gems/rspec-support-3.9.3/lib:/usr/local/rvm/rubies/ruby-2.7.0/lib/ruby/gems/2.7.0/gems/rspec-core-3.9.2/lib /usr/local/rvm/rubies/ruby-2.7.0/lib/ruby/gems/2.7.0/gems/rspec-core-3.9.2/exe/rspec --pattern spec/localhost/\*_spec.rb failed
   
   [vagrant@demo serverspec_sample]$ sudo mv ~/result.html /usr/share/nginx/html/
   [vagrant@demo serverspec_sample]$ sudo setenforce 0
   [vagrant@demo serverspec_sample]$ sudo systemctl start nginx.service
   ```

   - host PC에서 http://192.168.33.10/result.html 로 접속

   





