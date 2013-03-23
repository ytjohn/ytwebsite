Title: Using puppet to install djbdns
Date: 2012-06-22 12:30
Author: John Hogenmiller 

This is a basic walkthrough of getting a slightly complex "step by step
to install" program like djbdns to install under puppet (in this case,
under Ubuntu 12.04). It shows building the manifest, testing it, and
some possible gotchas.  
  
I am generally following the guide put together by Higher Logic[1], with
a few changes of my own.  
  
Step 1: Installation  
I use the dbndns fork of djbdns, which has a few patches installed that
djbdns lacks. In fact, the djbdns package in Debian/Ubuntu is a virtual
package that really install dbndns. To install it normally, you would
type "sudo apt-get install dbndns". This would also install daemontools
and daemontools-run. However, we'll also need make and ucspi-tcp.  
  
We're going to do this the puppet way. I'm assuming my puppet
configuration in in /etc/puppet, node manifests are in
/etc/puppet/nodes, and modules are in /etc/puppet/modules.  
  
a. Create the dbndns module with a package definition to install   
  
    sudo mkdir -p /etc/puppet/modules/dbndns/manifests  
    sudo vi /etc/puppet/modules/dbndns/manifests/init.pp  
     
        class dbndns {  
            package {  
                    dbndns:  
                    ensure =\> present;  
  
                    ucspi-tcp:  
                    ensure =\> present;  
  
                    make:  
                    ensure =\> present;  
            }  
  
        }  
  
         
b. Create a file for your node (ie: puppet2.example.net)  
  
    sudo vi /etc/puppet/nodes/puppet2.example.net.pp  
     
        node    'puppet2.lab.example.net' {  
            include dbndns  
        }  
         
  
c. Test  
Ok, to test on your puppet client, run "sudo puppet agent --test"  
  
    johnh@puppet2:\~\# sudo puppet agent --test  
    info: Retrieving plugin  
    info: Loading facts in /var/lib/puppet/lib/facter/facter\_dot\_d.rb  
    info: Loading facts in /var/lib/puppet/lib/facter/root\_home.rb  
    info: Loading facts in /var/lib/puppet/lib/facter/puppet\_vardir.rb  
    info: Caching catalog for puppet2.lab.example.net  
    info: Applying configuration version '1340213237'  
    notice: /Stage[main]/Dbndns/Package[dbndns]/ensure: created  
    notice: Finished catalog run in 3.39 seconds  
  
Here we can see our dbndns package installed. But is it running? Well,
djbdns uses daemontools, which runs svscan, and some searching online
shows that in Ubuntu 12.04/Precise, this is now an upstart job. svscan
is not running. So let's make it run. Add the following to your init.pp
(within the module definition):  
  
        \# define the service to restart  
        service { "svscan":  
                ensure  =\> "running",  
                provider =\> "upstart",  
                require =\> Package["dbndns"],  
        }  
  
Now back on puppet2, let's test it.  
  
    johnh@puppet2:\~\# sudo puppet agent --test  
    info: Retrieving plugin  
    info: Loading facts in /var/lib/puppet/lib/facter/facter\_dot\_d.rb  
    info: Loading facts in /var/lib/puppet/lib/facter/root\_home.rb  
    info: Loading facts in /var/lib/puppet/lib/facter/puppet\_vardir.rb  
    info: Caching catalog for puppet2.lab.example.net  
    info: Applying configuration version '1340213237'  
    notice: /Stage[main]/Dbndns/Service[svscan]/ensure: ensure changed
'stopped' to 'running'  
    notice: Finished catalog run in 0.47 seconds  
  
  
We now told puppet to ensure that svscan is running. The "provider"
option tells it to use upstart instead of /etc/init.d/ scripts or the
service command. Also, we make sure that it doesn't attempt to start
svscan unless dbndns is already installed.  
  
Now we have daemontools running, but we haven't got it start our tinydns
service yet. To do that, we need to create some users and configure the
service.  
     
Step 2: Create users  
  
Going back to our guide, our next step is to create users. We can do
that in puppet as well.  
    \# Users for the chroot jail  
    adduser --no-create-home --disabled-login --shell /bin/false dnslog  
    adduser --no-create-home --disabled-login --shell /bin/false
tinydns  
    adduser --no-create-home --disabled-login --shell /bin/false
dnscache  
  
So in our init.pp module file, we need to define our users:  
  
    user { "dnslog":  
            shell =\> "/bin/false",  
            managehome =\> "no",  
            ensure =\> "present",  
        }  
         
    user { "tinydns":  
            shell =\> "/bin/false",  
            managehome =\> "no",  
            ensure =\> "present",  
        }  
         
    user { "dnscache":  
            shell =\> "/bin/false",  
            managehome =\> "no",  
            ensure =\> "present",  
        }  
  
Back on puppet2, we can give that a test.  
  
    johnh@puppet2:\~\$ sudo puppet agent --test  
    info: Retrieving plugin  
    info: Loading facts in /var/lib/puppet/lib/facter/facter\_dot\_d.rb  
    info: Loading facts in /var/lib/puppet/lib/facter/root\_home.rb  
    info: Loading facts in /var/lib/puppet/lib/facter/puppet\_vardir.rb  
    info: Caching catalog for puppet2.lab.example.net  
    info: Applying configuration version '1340215757'  
    notice: /Stage[main]/Dbndns/User[dnscache]/ensure: created  
    notice: /Stage[main]/Dbndns/User[tinydns]/ensure: created  
    notice: /Stage[main]/Dbndns/User[dnslog]/ensure: created  
    notice: Finished catalog run in 0.86 seconds  
    johnh@puppet2:\~\$ cat /etc/passwd | grep dns  
    dnscache:x:1001:1001::/home/dnscache:/bin/false  
    tinydns:x:1002:1002::/home/tinydns:/bin/false  
    dnslog:x:1003:1003::/home/dnslog:/bin/false  
  
So far, so good. Now we have to do the configuration, which will require
executing some commands.  
  
Step 3 - Configuration  
Our next step are the following commands:  
  
    \# Config  
    tinydns-conf tinydns dnslog /etc/tinydns/ 1.2.3.4  
    dnscache-conf dnscache dnslog /etc/dnscache 127.0.0.1  
    cd /etc/dnscache; touch /etc/dnscache/root/ip/127.0.0  
    mkdir /etc/service ; cd /etc/service ; ln -sf /etc/tinydns/ ; ln -sf
/etc/dnscache  
         
The first two commands create our service directories. Authoratative
tinydns is set to listen on 1.2.3.4 and dnscache is set to listen on
127.0.0.1. The 3rd command creates a file that restricts dnscache to
only respond to requests from IPs starting with 127.0.0. This is isn't
necessary, but the challenge is interesting.  
  
What we want to do first is see if /etc/tinydns and /etc/dnscache exist
and if not, run the -conf program. We also need to know the IP address.
Fortunately, puppet provides this as a variable "\$ipaddress". Try
running the "facter" command.  
  
Puppet has a property call creates that is ideal. If the directory
specified by creates does not exist, it will perform the associated
commands. Here are our new lines:  
  
    exec { "configure-tinydns":  
            command =\> "/usr/bin/tinydns-conf tinydns dnslog
/etc/tinydns \$ipaddress",  
            creates =\> "/etc/tinydns",  
            require =\> Package['dbndns'],  
    }  
  
    exec { "configure-dnscache":  
            command =\> "/usr/bin/dnscache-conf dnscache dnslog
/etc/dnscache 127.0.0.1",  
            creates =\> "/etc/dnscache",  
            require =\> Package['dbndns'],  
    }  
  
  
Thos will configure tinydns and dnscache, and then we can restrict
dnscache  
  
  
    file { "/etc/dnscache/root/ip/127.0.0":  
            ensure =\> "present",  
            owner =\> "dnscache",  
            require =\> Exec["configure-dnscache"],  
    }  
  
Then, we need to create the /etc/service directory and bring tinydns and
dnscache under svscan's control.  
     
    file { "/etc/service":  
            ensure =\> "directory",  
            require =\> Package["dbndns"],  
    }  
  
    file { "/etc/service/tinydns":  
            ensure =\> "link",  
            target =\> "/etc/tinydns",  
            require =\> [ File['/etc/service'],
Exec["configure-tinydns"], ],  
    }  
  
    file { "/etc/service/dnscache":  
            ensure =\> "link",  
            target =\> "/etc/dnscache",  
            require =\> [  File['/etc/service'],
Exec["configure-dnscache"]  ],  
    }  
  
         
And our tests:  
  
    johnh@puppet2:\~\$ sudo puppet agent --test  
    info: Retrieving plugin  
    info: Loading facts in /var/lib/puppet/lib/facter/facter\_dot\_d.rb  
    info: Loading facts in /var/lib/puppet/lib/facter/root\_home.rb  
    info: Loading facts in /var/lib/puppet/lib/facter/puppet\_vardir.rb  
    info: Caching catalog for puppet2.lab.example.net  
    info: Applying configuration version '1340218775'  
    notice: /Stage[main]/Dbndns/Exec[configure-dnscache]/returns:
executed successfull  
    notice:
/Stage[main]/Dbndns/File[/etc/dnscache/root/ip/127.0.0]/ensure: created  
    notice: /Stage[main]/Dbndns/File[/etc/service/dnscache]/ensure:
created  
    notice: /Stage[main]/Dbndns/Exec[configure-tinydns]/returns:
executed successfully  
    notice: /Stage[main]/Dbndns/File[/etc/service/tinydns]/ensure:
created  
    notice: Finished catalog run in 0.59 seconds  
    johnh@puppet2:\~\$ ls /etc/service/tinydns/root/  
    add-alias  add-alias6  add-childns  add-host  add-host6  add-mx 
add-ns  data  Makefile  
    johnh@puppet2:\~\$ ps ax | grep supervise  
     7932 ?        S      0:00 supervise dnscache  
     7933 ?        S      0:00 supervise log  
     7934 ?        S      0:00 supervise tinydns  
     7935 ?        S      0:00 supervise log  
  
       
Doing a dig www.example.net @localhost returns 192.0.43.10, so dnscache
works.  
  
Now, let's check tinydns. No domains are configured yet, so let's put
example.com in there. Edit /etc/tinydns/root/data and put these lines in
it, substituting 10.100.0.178 for your own "public" IP address.  
  

> &example.com::ns0.example.com.:3600 
> Zexample.com:ns0.example.com.:hostmaster.example.com.:1188079131:16384:2048:1048576:2560:2560  
>  +ns0.example.com:10.100.0.178:3600

  
Then "make" the data.cdb file:  
  
    cd /etc/tinydns/root ; sudo make  
     
Now test:  
  
    johnh@puppet2:/etc/tinydns/root\$ dig ns0.example.com @10.100.0.178  
  
    ; \<\<\>\> DiG 9.8.1-P1 \<\<\>\> ns0.example.com @10.100.0.178  
    ;; global options: +cmd  
    ;; Got answer:  
    ;; -\>\>HEADER\<\<- opcode: QUERY, status: NOERROR, id: 25433  
    ;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 1, ADDITIONAL:
0  
    ;; WARNING: recursion requested but not available  
  
    ;; QUESTION SECTION:  
    ;ns0.example.com.               IN      A  
  
    ;; ANSWER SECTION:  
    ns0.example.com.        3600    IN      A       10.100.0.178  
  
    ;; AUTHORITY SECTION:  
    example.com.            3600    IN      NS      ns0.example.com.  
  
  
Ok, for a final test, let's remove everything and run it again.  
  
    sudo service svscan stop  
    sudo apt-get purge daemontools daemontools-run ucspi-tcp dbndns  
    sudo rm -rf /etc/service /etc/tinydns /etc/dnscache  
    sudo userdel tinydns   
    sudo userdel dnslog   
    sudo userdel dnscache  
     
Let's do this:  
  
    johnh@puppet2:\~\$ sudo puppet agent --test  
    info: Retrieving plugin  
    info: Loading facts in /var/lib/puppet/lib/facter/facter\_dot\_d.rb  
    info: Loading facts in /var/lib/puppet/lib/facter/root\_home.rb  
    info: Loading facts in /var/lib/puppet/lib/facter/puppet\_vardir.rb  
    info: Caching catalog for puppet2.lab.example.net  
    info: Applying configuration version '1340220032'  
    notice: /Stage[main]/Dbndns/Service[svscan]/ensure: ensure changed
'stopped' to 'running'  
    err: /Stage[main]/Dbndns/Exec[configure-dnscache]/returns: change
from notrun to 0 failed: /usr/bin/dnscache-conf dnscache dnslog
/etc/dnscache 127.0.0.1 returned 111 instead of one of [0] at
/etc/puppet/modules/dbndns/manifests/init.pp:47  
    notice: /Stage[main]/Dbndns/User[dnscache]/ensure: created  
    notice: /Stage[main]/Dbndns/User[tinydns]/ensure: created  
    notice: /Stage[main]/Dbndns/File[/etc/service]/ensure: created  
    notice: /Stage[main]/Dbndns/File[/etc/service/dnscache]: Dependency
Exec[configure-dnscache] has failures: true  
    warning: /Stage[main]/Dbndns/File[/etc/service/dnscache]: Skipping
because of failed dependencies  
    notice: /Stage[main]/Dbndns/User[dnslog]/ensure: created  
    notice: /Stage[main]/Dbndns/File[/etc/dnscache/root/ip/127.0.0]:
Dependency Exec[configure-dnscache] has failures: true  
    warning: /Stage[main]/Dbndns/File[/etc/dnscache/root/ip/127.0.0]:
Skipping because of failed dependencies  
    notice: /Stage[main]/Dbndns/Exec[configure-tinydns]/returns:
executed successfully  
    notice: /Stage[main]/Dbndns/File[/etc/service/tinydns]/ensure:
created  
    notice: Finished catalog run in 0.98 seconds  
  
     
Looks like we had something fail. Oops! configure-dnscache failed. We
see that the user dnscache and tinydns were created after. So we need to
make sure that the users are created before we can configure the
service. This needs to happen to tinydns as well as dnscache. Good thing
we did this test so it doesn't bite us in the future. Let's adjust our
init.pp  
  
        exec { "configure-tinydns":  
                command =\> "/usr/bin/tinydns-conf tinydns dnslog
/etc/tinydns \$ipaddress",  
                creates =\> "/etc/tinydns",  
                require =\> [ Package['dbndns'], User['dnscache'],
User['dnslog'] ],  
        }  
  
        exec { "configure-dnscache":  
                command =\> "/usr/bin/dnscache-conf dnscache dnslog
/etc/dnscache 127.0.0.1",  
                creates =\> "/etc/dnscache",  
                require =\> [ Package['dbndns'],  User['dnscache'],
User['dnslog'] ],  
        }  
  
Also, let's go ahead and run our commands above to get rid of everything
again.  
  
  
    johnh@puppet2:\~\$ sudo puppet agent --test  
    info: Retrieving plugin  
    info: Loading facts in /var/lib/puppet/lib/facter/facter\_dot\_d.rb  
    info: Loading facts in /var/lib/puppet/lib/facter/root\_home.rb  
    info: Loading facts in /var/lib/puppet/lib/facter/puppet\_vardir.rb  
    info: Caching catalog for puppet2.lab.example.net  
    info: Applying configuration version '1340220641'  
    notice: /Stage[main]/Dbndns/Service[svscan]/ensure: ensure changed
'stopped' to 'running'  
    notice: /Stage[main]/Dbndns/User[dnscache]/ensure: created  
    notice: /Stage[main]/Dbndns/User[tinydns]/ensure: created  
    notice: /Stage[main]/Dbndns/File[/etc/service]/ensure: created  
    notice: /Stage[main]/Dbndns/User[dnslog]/ensure: created  
    notice: /Stage[main]/Dbndns/Exec[configure-dnscache]/returns:
executed successfully  
    notice: /Stage[main]/Dbndns/File[/etc/service/dnscache]/ensure:
created  
    notice:
/Stage[main]/Dbndns/File[/etc/dnscache/root/ip/127.0.0]/ensure: created  
    notice: /Stage[main]/Dbndns/Exec[configure-tinydns]/returns:
executed successfully  
    notice: /Stage[main]/Dbndns/File[/etc/service/tinydns]/ensure:
created  
    notice: Finished catalog run in 1.05 seconds  
  
Everything looks good, but when we run "ps ax | grep svscan" we don't
see svscan running. So we check /var/log/syslog and see this   
  
    Jun 20 19:31:35 puppet2 kernel: [ 9646.348251] init: svscan main
process ended, respawning  
    Jun 20 19:31:35 puppet2 kernel: [ 9646.359074] init: svscan
respawning too fast, stopped  
     
If we start it by hand, it works, so what happened? /etc/service didn't
exist yet.  
  
    johnh@puppet2:\~\$ sudo service svscan start  
    svscan start/running, process 9726  
    johnh@puppet2:\~\$ ps ax | grep supervise  
     9730 ?        S      0:00 supervise dnscache  
     9731 ?        S      0:00 supervise log  
     9732 ?        S      0:00 supervise tinydns  
     9733 ?        S      0:00 supervise log  
  
Let's fix that.  
  
        \# define the service to restart  
        service { "svscan":  
                ensure  =\> "running",  
                provider =\> "upstart",  
                require =\> [ Package["dbndns"], File["/etc/service"] ]  
        }  
  
Now, let's give it a go:  
  
  
    johnh@puppet2:\~\$ sudo puppet agent --test  
    info: Retrieving plugin  
    info: Loading facts in /var/lib/puppet/lib/facter/facter\_dot\_d.rb  
    info: Loading facts in /var/lib/puppet/lib/facter/root\_home.rb  
    info: Loading facts in /var/lib/puppet/lib/facter/puppet\_vardir.rb  
    info: Caching catalog for puppet2.lab.example.net  
    info: Applying configuration version '1340220885'  
    notice: /Stage[main]/Dbndns/User[dnscache]/ensure: created  
    notice: /Stage[main]/Dbndns/User[tinydns]/ensure: created  
    notice: /Stage[main]/Dbndns/File[/etc/service]/ensure: created  
    notice: /Stage[main]/Dbndns/Service[svscan]/ensure: ensure changed
'stopped' to 'running'  
    notice: /Stage[main]/Dbndns/User[dnslog]/ensure: created  
    notice: /Stage[main]/Dbndns/Exec[configure-dnscache]/returns:
executed successfully  
    notice: /Stage[main]/Dbndns/File[/etc/service/dnscache]/ensure:
created  
    notice:
/Stage[main]/Dbndns/File[/etc/dnscache/root/ip/127.0.0]/ensure: created  
    notice: /Stage[main]/Dbndns/Exec[configure-tinydns]/returns:
executed successfully  
    notice: /Stage[main]/Dbndns/File[/etc/service/tinydns]/ensure:
created  
    notice: Finished catalog run in 1.24 seconds  
    johnh@puppet2:\~\$ ps ax | grep svscan  
    10613 ?        Ss     0:00 /bin/sh /usr/bin/svscanboot  
    10615 ?        S      0:00 svscan /etc/service  
    10639 pts/0    S+     0:00 grep --color=auto svscan  
    johnh@puppet2:\~\$ ps ax | grep supervise  
    10630 ?        S      0:00 supervise dnscache  
    10631 ?        S      0:00 supervise log  
    10632 ?        S      0:00 supervise tinydns  
    10633 ?        S      0:00 supervise log  
    10641 pts/0    S+     0:00 grep --color=auto supervise  
  
Excellent! We now have a working puppet class that will install puppet,
configure it, and get it up and running. At this point, we don't have
any records being served by tinydns, but it wouldn't be hard to push a
file to /etc/tinydns/root/data and execute a command to perform the
make. In my case, I will be using VegaDNS's update-data.sh[2] to pull
the data remotely.  
  
Here is our completed modules/dbndns/init.pp:  
  
---  
class dbndns {  
  
  
        package {  
                dbndns:  
                ensure =\> present;  
  
                ucspi-tcp:  
                ensure =\> present;  
  
                make:  
                ensure =\> present;  
        }  
  
  
        \# define the service to restart  
        service { "svscan":  
                ensure  =\> "running",  
                provider =\> "upstart",  
                require =\> [ Package["dbndns"], File["/etc/service"] ]  
        }  
  
        user { "dnslog":  
                        shell =\> "/bin/false",  
                        managehome =\> false,  
                        ensure =\> "present",  
                }  
  
        user { "tinydns":  
                        shell =\> "/bin/false",  
                        managehome =\> false,  
                        ensure =\> "present",  
                }  
  
        user { "dnscache":  
                        shell =\> "/bin/false",  
                        managehome =\> false,  
                        ensure =\> "present",  
                }  
  
        exec { "configure-tinydns":  
                command =\> "/usr/bin/tinydns-conf tinydns dnslog
/etc/tinydns \$ipaddress",  
                creates =\> "/etc/tinydns",  
                require =\> [ Package['dbndns'], User['dnscache'],
User['dnslog'] ],  
        }  
  
        exec { "configure-dnscache":  
                command =\> "/usr/bin/dnscache-conf dnscache dnslog
/etc/dnscache 127.0.0.1",  
                creates =\> "/etc/dnscache",  
                require =\> [ Package['dbndns'],  User['dnscache'],
User['dnslog'] ],  
        }  
  
        file { "/etc/dnscache/root/ip/127.0.0":  
                ensure =\> "present",  
                owner =\> "dnscache",  
                require =\> Exec["configure-dnscache"],  
        }  
  
        file { "/etc/service":  
                ensure =\> "directory",  
                require =\> Package["dbndns"],  
        }  
  
        file { "/etc/service/tinydns":  
                ensure =\> "link",  
                target =\> "/etc/tinydns",  
                require =\> [ File['/etc/service'],  
                                        Exec["configure-tinydns"],  
                                ],  
        }  
  
        file { "/etc/service/dnscache":  
                ensure =\> "link",  
                target =\> "/etc/dnscache",  
                require =\> [  File['/etc/service'],  
                                        Exec["configure-dnscache"]  
                                ],  
        }  
  
}  
  
  
  
  
---  
  
[1]
http://higherlogic.com.au/2011/djbdns-on-ubuntu-10-04-server-migration-from-bind-and-zone-transfers-to-secondaries-bind/  
[2] https://github.com/shupp/VegaDNS/blob/master/update-data.sh
