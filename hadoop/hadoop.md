Hadoop
============= 

> Hadoop = 대규모 비정형 데이터 세트를 분산 저장 및 처리할 수 있는 오픈소스 프레임워크 / 병렬 처리

1. window에서 WSL/ 터미널 먼저 설치 필요
```
wsl --install
```
*username/password = ubunto(오타)

2. git bash를 터미널에서 실행시키기 위한 코드
터미널 설정 > Json 파일열기 > git bash profile 터미널에 추가
```
{
    "name": "Git Bash",
    "commandline": "C:\\Program Files\\Git\\bin\\bash.exe -li",
    "icon": "C:\\Program Files\\Git\\mingw64\\share\\git\\git-for-windows.ico",
    "startingDirectory": "%USERPROFILE%"
}
```
3. 리눅스 설정(LINUx)
** window
- `sudo apt-get update`
- `sudo apt-get install openjdk-8-jdk`
    - java -version 으로 확인
- vi ~/.bashrc
    - `export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64`
- `sudo apt-get install openssh-server`
    - `sudo ufw allow 22`
    - 키생성
        - `ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa`
    - 키등록
        - `cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys`
        - `chmod 600 ~/.ssh/authorized_keys`

4. hadoop 설치
    - `wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz`
    - `tar zxvf hadoop-3.3.6.tar.gz`
    
    ```bash
    # .bashrc
    export HADOOP_HOME=/home/ubuntu/hadoop-3.3.6
    export PATH=$PATH:$HADOOP_HOME/bin
    ```
    
    - source .bashrc
        - hadoop version

5. hadoop 실행을 위해 코드 수정
- core-site.xml
```
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
```

- 터미널(dfs폴더/data, name 파일 생성)
```
mkdir -p dfs/data
mkdir -p dfs/name
```

- hdfs-site.xml
```
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>/home/ubunto(경로확인필요)/hadoop-3.3.6/dfs/name</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>/home/ubunto(경로확인필요)/hadoop-3.3.6/dfs/data</value>
    </property>
</configuration>
```
- mapred-site.xml
```
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
    <property>
        <name>mapreduce.application.classpath</name>
        <value>$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/*:$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/lib/*</value>
    </property>
</configuration>
```
- yarn-site.xml
```
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.nodemanager.env-whitelist</name>
        <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_HOME,PATH,LANG,TZ,HADOOP_MAPRED_HOME</value>
    </property>
</configuration>
```
- hadoop-env.sh
```
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
```
6. 네임노드 포맷
```
hdfs namenode -format
```
dfs/name/ 새로운 파일들 생성됨

7. hfds 실행 **localhost:9870
```
sbin/start-dfs.sh
```

8. yarn 실행 **localhost:8088
```
sbin/start-yarn.sh
```
9. 실행 중지
```
sbin/stop-dfs.sh
sbin/stop-yarn.sh
```
10. 예제 코드
```
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar pi 10 10000
```
-> pi 값 계산하는 코드 실행