Name: helloworld
Version: 1.0.0
Release: 1
Summary: RPM for Helloworld service
License: MixRadio 2015
Requires: jdk >= 2000:1.7.0_55-fcs
autoprov: no
autoreq: no
BuildRoot: /Users/mdaley/projects/helloworld/helloworld/buildroot

%description

%install
if [ -e $RPM_BUILD_ROOT ];
then
  mv /Users/mdaley/projects/helloworld/helloworld/tmp-buildroot/* $RPM_BUILD_ROOT
else
  mv /Users/mdaley/projects/helloworld/helloworld/tmp-buildroot $RPM_BUILD_ROOT
fi

%files

%attr(444,helloworld,helloworld) /usr/local/helloworld/helloworld.jar
%attr(744,helloworld,helloworld) /usr/local/helloworld/bin
%attr(755,-,-) /etc/rc.d/init.d

%pre
/bin/echo "preinstall script started [$1]"

APP_NAME=helloworld
prefixDir=/usr/local/$APP_NAME
identifier=$APP_NAME.jar

isJettyRunning=`pgrep java -lf | grep $identifier | cut -d" " -f1 | /usr/bin/wc -l`
if [ $isJettyRunning -eq 0 ]
then
  /bin/echo "Helloworld is not running"
else
  sleepCounter=0
  sleepIncrement=2
  waitTimeOut=600

  /bin/echo "Timeout is $waitTimeOut seconds"
  /bin/echo "Helloworld is running, stopping service"
  /sbin/service $APP_NAME stop &
  myPid=$!

  until [ `pgrep java -lf | grep $identifier | cut -d" " -f1 | /usr/bin/wc -l` -eq 0 ]
  do
    if [ $sleepCounter -ge $waitTimeOut ]
    then
      /usr/bin/pkill -KILL -f '$identifier'
      /bin/echo "Killed Helloworld"
      break
    fi
    sleep $sleepIncrement
    sleepCounter=$(($sleepCounter + $sleepIncrement))
  done

  wait $myPid

  /bin/echo "Helloworld down"
fi

rm -rf $prefixDir

if [ "$1" -le 1 ]
then
  mkdir -p $prefixDir
  /usr/sbin/useradd -r -s /sbin/nologin -d $prefixDir -m -c "Helloworld user for the Helloworld service" $APP_NAME 2> /dev/null || :
fi

/usr/bin/getent passwd $APP_NAME

/bin/echo "preinstall script finished"
exit 0

%post
/bin/echo "postinstall script started [$1]"

APP_NAME=helloworld

if [ "$1" -le 1 ]
then
  /sbin/chkconfig --add $APP_NAME
else
  /sbin/chkconfig --list $APP_NAME
fi

ln -s /var/encrypted/logs/$APP_NAME /var/log/$APP_NAME

chown -R $APP_NAME:$APP_NAME /usr/local/$APP_NAME

chmod 755 /usr/local/$APP_NAME/bin

/bin/echo "postinstall script finished"
exit 0

%preun
/bin/echo "preremove script started [$1]"

APP_NAME=helloworld
prefixDir=/usr/local/$APP_NAME
identifier=$APP_NAME.jar

isJettyRunning=`pgrep java -lf | grep $identifier | cut -d" " -f1 | /usr/bin/wc -l`
if [ $isJettyRunning -eq 0 ]
then
  /bin/echo "Helloworld is not running"
else
  sleepCounter=0
  sleepIncrement=2
  waitTimeOut=600
  /bin/echo "Timeout is $waitTimeOut seconds"
  /bin/echo "Helloworld is running, stopping service"
  /sbin/service $APP_NAME stop &
  myPid=$!

  until [ `pgrep java -lf | grep $identifier | cut -d" " -f1 | /usr/bin/wc -l` -eq 0 ]
  do
    if [ $sleepCounter -ge $waitTimeOut ]
    then
      /usr/bin/pkill -KILL -f '$identifier'
      /bin/echo "Killed Helloworld"
      break
    fi
    sleep $sleepIncrement
    sleepCounter=$(($sleepCounter + $sleepIncrement))
  done

  wait $myPid

  /bin/echo "Helloworld down"
fi

if [ "$1" = 0 ]
then
  /sbin/chkconfig --del $APP_NAME
else
  /sbin/chkconfig --list $APP_NAME
fi

/bin/echo "preremove script finished"
exit 0

%postun
/bin/echo "postremove script started [$1]"

if [ "$1" = 0 ]
then
  /usr/sbin/userdel -r helloworld 2> /dev/null || :
  /bin/rm -rf /usr/local/helloworld
fi

/bin/echo "postremove script finished"
exit 0
