Docker, CoreOS, and ShipYard

Just wanted to write up my first impressions using [CoreOS] and [Shipyard].

Why am I so interested in [Docker]? Docker is based off of Linux containers and is a super lightweight "virtualization" method. Calling it virtualization isn't entirely correct, it's more of a glorified chroot, or a true evolution of the FreeBSD jails. You start with an OS image (Ubuntu, Centos, etc) as your base. Multiple docker instances can share the same image. A reference container is layered over top of that image, containing your application. 

[Docker]: https://www.docker.io/ 
[CoreOS]: https://coreos.com/
[Shipyard]: http://shipyard-project.com/

For example, if I wanted to install a complicated applicaton like [gitlab] with a ton of ruby gem dependencies, I could start with a Ubuntu 12.04 LTS image, start an interactive container, walk through the gitlab install process, and then commit my container (version control). Now this container only has the file system differences between the Ubuntu base image and what I installed. I can now upload this container somewhere and others can use it.
If I use this container, it becomes a read-only reference point and any configuration changes I make (such as my own user accounts) become part of a running instance and these changes are not made to the container. I could even commit my configuration changes to a new container and distribute that. Basically, a docker instance is comprised of layers - the base image, 1 or more containers, then finally the current instance.

I've been experimenting with Docker for a while, but recently a coworker informed me of a management interface called [Shipyard] that lets you create and manage your Docker containers across multiple hosts.

First off, I did what turned out to be a mistake. I tried to install this on one of my development hosts that already had docker setup. It also had a few other things running such as reddis and a project running on port 8000. Shipyard installs a set of docker containers including redis and it's management interface is django based and runs on port 8000. It also attempts to bind another container to port 80. When I attempted to install, these containers failed to get setup. I then tried shutting down other processes, disabling iptables, deleting the docker containers and re-running the install, but I ended up with a system that wouldn't see any existing containers or images, and wouldn't import any images so I could build a container. It was a very frustrating first start.

At this point I decided to go ahead and spin up a new virtual machine to run Shipyard. Normally, I could do this with Ubuntu, but I've been watching another related project called [CoreOS] which is designed to run as a minimal footprint Linux distribution (runs in 161MB of ram), where all applications are built os docker containers. Technically, you don't even have to install it, it could just netboot into CoreOS and load your containers off a local storage array.

I tried to install this using a VirtualBox VM, Ubuntu live CD, and their [bare-metal installation](https://coreos.com/docs/running-coreos/bare-metal/installing-to-disk/) instructions, which involved creating a .ssh/authorized_keys (no copy/paste, had to download the content) and making sure it was owned by uid 1000. Unfortunately, CoreOS would not get an IP address from the DHCP server and you can't login locally as no password is set [issue #7](https://github.com/xdissent/ievms/issues/7).

The most expedient way to get this up and running is to use Vagrant. Make sure you have [Vagrant] and [Virtualbox] installed and do this:

    git clone https://github.com/coreos/coreos-vagrant.git
    cd coreos-vagrant
    vagrant up
    vagrant ssh

[Vagrant]: http://www.vagrantup.com/downloads.html
[VirtualBox]: https://www.virtualbox.org/ 

Once connected, I saw that /dev/sda9 was mounted as /var with 15GB of space. Hopefully that's enough to run my shipyard setup. The programs git and docker are installed, so let's see what it will take to get shipyard going.

First off, I know I need docker to listen on a tcp port. We need to copy the read-only /usr/lib/systemd/system/docker.service to /media/state/units/docker.service and change `ExecStart=/usr/bin/docker -d -r=false -H fd://` to `ExecStart=/usr/bin/docker -d -r=false  -H tcp://127.0.0.1:4243 -H fd://`.

Then I have to grok the instructions on CoreOs' [systemd page](https://coreos.com/docs/launching-containers/launching/getting-started-with-systemd/) to restart docker.

    sudo systemctl link --runtime /media/state/units/docker.service 
    ln -s '/media/state/units/docker.service' '/run/systemd/system/docker.service'
    core@localhost /media/state/units $ sudo systemctl restart docker.service
    core@localhost /media/state/units $ sudo netstat -nlp
    Active Internet connections (only servers)
    Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
    tcp        0      0 127.0.0.1:4243          0.0.0.0:*               LISTEN      3265/docker         

Now, I can run the shipyard deploy command. This will take a while to run.

    docker run -i -t -v /var/run/docker.sock:/docker.sock shipyard/deploy setup


It should end with this status and you should see your docker containers running and listening on ports

Shipyard Stack Deployed

You should be able to login with admin:shipyard at http://<docker-host-ip>:8000
You will also need to setup and register the Shipyard Agent.  See http://github.com/shipyard/shipyard-agent for details.

    core@localhost /lib64 $ docker ps
    CONTAINER ID        IMAGE                      COMMAND                CREATED             STATUS              PORTS                            NAMES
    a8cbfe1d79d1        shipyard/shipyard:latest   /app/.docker/run.sh    5 seconds ago       Up 4 seconds        0.0.0.0:8000->8000/tcp           shipyard                                                                                             
    b55752e625ee        shipyard/db:latest         /bin/bash -e /usr/lo   6 seconds ago       Up 5 seconds        0.0.0.0:49154->5432/tcp          shipyard/db,shipyard_db                                                                              
    d40c735f4d9d        shipyard/lb:latest         /bin/sh -e /usr/loca   7 seconds ago       Up 6 seconds        0.0.0.0:80->80/tcp, 443/tcp      shipyard_lb                                                                                          
    46a3a2520b3f        shipyard/router:latest     /bin/sh -e /usr/loca   7 seconds ago       Up 6 seconds        0.0.0.0:49153->80/tcp, 443/tcp   shipyard_lb/app_router,shipyard_router                                                               
    db97354954b5        shipyard/redis:latest      /usr/local/bin/redis   7 seconds ago       Up 6 seconds        0.0.0.0:6379->6379/tcp           shipyard/redis,shipyard_lb/app_router/redis,shipyard_lb/redis,shipyard_redis,shipyard_router/redis   


    core@localhost /lib64 $ sudo netstat -nlp
    Active Internet connections (only servers)
    Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
    tcp        0      0 127.0.0.1:4243          0.0.0.0:*               LISTEN      3265/docker         
    tcp6       0      0 :::80                   :::*                    LISTEN      3265/docker         
    tcp6       0      0 :::22                   :::*                    LISTEN      1/systemd           
    tcp6       0      0 :::7001                 :::*                    LISTEN      388/etcd            
    tcp6       0      0 :::8000                 :::*                    LISTEN      3265/docker         
    tcp6       0      0 :::49153                :::*                    LISTEN      3265/docker         
    tcp6       0      0 :::4001                 :::*                    LISTEN      388/etcd            
    tcp6       0      0 :::49154                :::*                    LISTEN      3265/docker         
    tcp6       0      0 :::6379                 :::*                    LISTEN      3265/docker         
    raw6       0      0 :::58                   :::*                    7           316/dhcpcd  

We need to download and run an agent to connect to our shipyard host. As of today, the most recent is v0.2.1

    wget https://github.com/shipyard/shipyard-agent/releases/download/v0.2.1/shipyard-agent
    chmod 755 shipyard-agent
    ./shipyard-agent -url http://localhost:8000 -register 
    ./shipyard-agent: error while loading shared libraries: libdevmapper.so.1.02.1: cannot open shared object file: No such file or directory

I have run afoul of a curses [Issue #134](https://github.com/shipyard/shipyard/issues/134). I need to make a symlink and run ldconfig, but /lib64 is on a read-only filesystem.





Now, since I ran this as a vagrant instance, it defaults to a nat'd configuration. This means we go to go back into VirtualBox and route localhost:8000 to 10.0.2.15:8000.

