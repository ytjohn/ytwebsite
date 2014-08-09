Ubuntu OpenStack Install
------------------------

This is just a bit of my journey to getting OpenStack going (I'm assuming at this point that I eventually do). It's probably not going to be the best of guides, but just shows what I encounter as I undertake this task.

Other than play with [DevStack](http://www.devstack.org/) I haven't had much chance to work with OpenStack. Recently I decided to purchase some new hardware and set this up in my lab. I found a great deal on a SuperMicro "Twin" server. This is two physical motherboards in a 1U case, each with 32Gb of ram, two 80GB sata drives, IPMI (out of band management), and quad-core 2.5ghz nics. All this was ~ $250. I figured it would be perfect for an OpenStack setup. Once I get it working, I plan to upgrade the drives to the multi-terabyte range.

With OpenStack, I basically understand I need to setup a Controller Node, a Network node, and a Compute node. I can put some or all of these in VMs (though I may have performance issues, especially with the compute nodes). 

* Controller Node: 1 processor, 2 GB memory, and 5 GB storage
* Network Node: 1 processor, 512 MB memory, and 5 GB storage
* Compute Node: 1 processor, 2 GB memory, and 10 GB storage

My goal is to build the controller and network nodes inside virtual machines - running on my own laptop initially. I thoroughly hope to then migrate these virtual machines into the OpenStack cluster when completed. What I really want out of this system when I'm done is

* Two hardware nodes with local storage
* Two networks/vswitches - one on my local private network and one for my public ip space. I may add some additional private "backend" type networks down the road.
* Later, I hope to add iscsi shared storage, for [live migration](http://docs.openstack.org/grizzly/openstack-compute/admin/content/live-migration-usage.html) and failover capabilities.

Finding a clear guide on installing OpenStack has been rather difficult. The [OpenStack Guide](http://docs.openstack.org/trunk/install-guide/install/apt/content/ch_preface.html) has a lot of commands you have to run scattered through individually separated pages. You basically have to keep expanding all the content on the left, find the commands you need to run on various nodes and run them. Some bits seem out of order, like [adding a PPA appears rather far down the stack](http://docs.openstack.org/trunk/install-guide/install/apt/content/basics-packages.html). 

On the other side of things, Ubuntu really wants to show you how [SIMPLE](http://www.ubuntu.com/cloud/ubuntu-openstack/) it is to build a cloud using their [MAAS](http://www.ubuntu.com/cloud/tools/maas) (Metal As A Service) tool, and [Juju](http://www.ubuntu.com/cloud/tools/juju). But as I constantly navigate, I end up going in circles of marketing style pages. I tried working with MAAS, got it to boot up my hardware and get to screen where it showed me the IP address, but seemed to go no further - hours pass. I also realised that even if if did work, it wouldn't setup the two 80gb drives in a raid 1 array. Since all MAAS really seems to do is install a base image of Ubuntu Server, I abandoned it and installed each by hand, with only OpenSSH running.

The next phase of Ubutu's cloud is their orchestration tool "[Juju](http://www.ubuntu.com/cloud/tools/juju).

> Juju is the game-changing service orchestration tool that lets you build entire cloud environments 
> with only a few commands. **Whether you want to deploy OpenStack itself**, a workload on public or private
> clouds, or even directly on bare metal using MAAS, Juju is the fastest and simplest solution.

Yes, that is what I want to do! I want to deploy OpenStack. Another page reads "Juju is the fastest way to deploy OpenStack". Which leads me to start searching the site, including http://juju.ubuntu.com/ looking for a guide on doing just that. It gets very frustrating, once again going in circles. Finally, I find a page on [installing juju](https://juju.ubuntu.com/install/).

In order to keep my hardware machines "virgin", I spun up a virtual machine on my laptop and installed juju here. I also found the add-apt-repository didn't exist on my base install of Ubuntu 14.04.1 LTS, so I had to get that in place first.

	sudo apt-get install python-software-properties
	sudo add-apt-repository ppa:juju/stable
	sudo apt-get update && sudo apt-get install juju-core

On a side note, I did setup ssh key trust between my "jujuvm" and my two physical Ubuntu servers. https://help.ubuntu.com/community/SSH/OpenSSH/Keys

At this point, I don't see a way to deploy OpenStack components. There are some Charms for Identity Items like Keystone and NOVA, but no cohesive deployment pattern. I start to give up on Juju altogether, but then I found someone else has taken this path.  http://marcoceppi.com/2014/06/deploying-openstack-with-just-two-machines/  They are using MAAS, but maybe I can follow them to a point. Looking them over, I think I can combine some steps from Juju's [Manual Provisioning](https://juju.ubuntu.com/docs/config-manual.html).

In my environment, the jujuvm is 10.10.0.182, ostack0 = 10.10.0.25, ostack1 = 10.10.0.26.

Let's setup manual mode:

	juju generate-config
	juju switch manual

Now, the guide I found sets up first node as the Orchestration node, which is fine, but I actually have 3 nodes available to me. I'm going to start referring to my jujuvm as controller0 and it will have both Juju and OpenStack controller setup.

The first thing I need to do is bootstrap my controller0. I have to edit ~/.juju/environments.yaml and change the bootstrap-host under manual to say 10.10.0.182.  Then I can run `juju bootstrap` and see what happens.

	ytjohn@ubuntu:~/.juju$ vi environments.yaml 
	ytjohn@ubuntu:~/.juju$ juju bootstrap
	ytjohn@10.10.0.182's password: 
	[sudo] password for ytjohn: 
	Logging to /var/log/cloud-init-output.log on remote host
	Running apt-get update
	Installing package: git
	Installing package: curl
	Installing package: cpu-checker
	Installing package: bridge-utils
	Installing package: rsyslog-gnutls
	Installing package: juju-mongodb
	Fetching tools: curl -sSfw 'tools from %{url_effective} downloaded: HTTP %{http_code}; time %{time_total}s; size %{size_download} bytes; speed %{speed_download} bytes/s ' -o $bin/tools.tar.gz 'https://streams.canonical.com/juju/tools/releases/juju-1.18.4-trusty-amd64.tgz'
	Starting MongoDB server (juju-db)
	Bootstrapping Juju machine agent
	Starting Juju machine agent (jujud-machine-0)

Looks promising. Now, let's deploy the juju gui to this same machine (0):

	ytjohn@ubuntu:~/.juju$ juju deploy --to 0 juju-gui
	Added charm "cs:trusty/juju-gui-3" to the environment.

At this point, I can access https://10.10.0.182/ - The password is stored in ~/.juju/environments/manual.jenv and under password field. For me, this was the second line. 

I can follow along and start building the actual openstack components using juju deploy onto this same VM. These components will end up in LXC containers (think Docker).

	ytjohn@ubuntu:~/.juju$ juju deploy --to lxc:0 mysql
	Added charm "cs:trusty/mysql-3" to the environment.
	ytjohn@ubuntu:~/.juju$ juju deploy --to lxc:0 keystone
	Added charm "cs:trusty/keystone-5" to the environment.
	ytjohn@ubuntu:~/.juju$ juju deploy --to lxc:0 nova-cloud-controller
	Added charm "cs:trusty/nova-cloud-controller-41" to the environment.
	ytjohn@ubuntu:~/.juju$ juju deploy --to lxc:0 glance
	Added charm "cs:trusty/glance-3" to the environment.
	ytjohn@ubuntu:~/.juju$ juju deploy --to lxc:0 rabbitmq-server
	Added charm "cs:trusty/rabbitmq-server-4" to the environment.
	ytjohn@ubuntu:~/.juju$ juju deploy --to lxc:0 openstack-dashboard
	Added charm "cs:trusty/openstack-dashboard-4" to the environment.
	ytjohn@ubuntu:~/.juju$ juju deploy --to lxc:0 cinder
	Added charm "cs:trusty/cinder-4" to the environment.

Now things are really churning along. According to Marco Ceppi's incredibly awesome work, I've now deployed the minimum for an OpenStack controller within my VM. These will take a little bit too boot up, but we can solder right along to adding a compute node. 

On the web interface, I see all these "charms" show up, and I can click on and interact with them if desired. For instance, I see Keystone started up with an ip of 10.0.3.15. 

Now, I need to jump back to the manual steps because I'm not using MAAS like he is. Here I'll add in my two physical servers.

	ytjohn@ubuntu:~/.juju$ juju add-machine ssh:10.10.0.25
	Logging to /var/log/cloud-init-output.log on remote host
	Running apt-get update
	Installing package: git
	Installing package: curl
	Installing package: cpu-checker
	Installing package: bridge-utils
	Installing package: rsyslog-gnutls
	Fetching tools: curl -sSfw 'tools from %{url_effective} downloaded: HTTP %{http_code}; time %{time_total}s; size %{size_download} bytes; speed %{speed_download} bytes/s ' -o $bin/tools.tar.gz 'https://streams.canonical.com/juju/tools/releases/juju-1.18.4-trusty-amd64.tgz'
	Starting Juju machine agent (jujud-machine-2)
	ytjohn@ubuntu:~/.juju$ juju add-machine ssh:10.10.0.26
	...

Once these complete, I can run `juju status` and see my machines listed.

	  "2":
	    agent-state: started
	    agent-version: 1.18.4
	    dns-name: 10.10.0.25
	    instance-id: manual:10.10.0.25
	    series: trusty
	    hardware: arch=amd64 cpu-cores=8 mem=32175M
	  "3":
	    agent-state: started
	    agent-version: 1.18.4
	    dns-name: 10.10.0.26
	    instance-id: manual:10.10.0.26
	    series: trusty
	    hardware: arch=amd64 cpu-cores=8 mem=20079M

I had an issue the first time I add 10.10.0.25 so I tried to destroy-machine and terminate-machine, but it's still there with a status of "dying". But I should now be able to deploy a compute node -to 2 & 3.

If I run the command without specifying a destination, it put it on the next node (10.10.0.25):

ytjohn@ubuntu:~$ juju deploy nova-compute
Added charm "cs:trusty/nova-compute-3" to the environment.
ytjohn@ubuntu:~$ juju status
# ...
  nova-compute:
    charm: cs:trusty/nova-compute-3
    exposed: false
    relations:
      compute-peer:
      - nova-compute
    units:
      nova-compute/0:
        agent-state: error
        agent-state-info: 'hook failed: "install"'
        agent-version: 1.18.4
        machine: "2"
        public-address: 10.10.0.25

I don't like the look of that 'hook failed: install'. I'll come back to that. I need to setup some relationships.

	ytjohn@ubuntu:~$ juju add-relation nova-cloud-controller rabbitmq-server
	ytjohn@ubuntu:~$ juju add-relation nova-cloud-controller glance
	ytjohn@ubuntu:~$ juju add-relation nova-cloud-controller keystone
	ytjohn@ubuntu:~$ juju add-relation nova-compute nova-cloud-controller
	ytjohn@ubuntu:~$ juju add-relation nova-compute mysql
	ytjohn@ubuntu:~$ juju add-relation nova-compute rabbitmq-server:amqp
	ytjohn@ubuntu:~$ juju add-relation nova-compute glance
	ytjohn@ubuntu:~$ juju add-relation glance mysql
	ytjohn@ubuntu:~$ juju add-relation glance keystone
	ytjohn@ubuntu:~$ juju add-relation glance cinder
	ytjohn@ubuntu:~$ juju add-relation mysql cinder
	ytjohn@ubuntu:~$ juju add-relation cinder rabbitmq-server
	ytjohn@ubuntu:~$ juju add-relation cinder nova-cloud-controller
	ytjohn@ubuntu:~$ juju add-relation cinder keystone
	ytjohn@ubuntu:~$ juju add-relation openstack-dashboard keystone

Going back to nova-computer, I'm going to try removing and redeploying it

	ytjohn@ubuntu:~$ juju remove-service nova-compute
	ytjohn@ubuntu:~$ juju status | grep -A 11 nova-compute:
	  nova-compute:
	    charm: cs:trusty/nova-compute-3
	    exposed: false
	    life: dying
	    units:
	      nova-compute/0:
	        agent-state: error
	        agent-state-info: 'hook failed: "start"'
	        agent-version: 1.18.4
	        life: dying
	        machine: "2"
	        public-address: 10.10.0.25

I went on to .25 and found /var/log/juju/unit-nova-compute-0.log

	2014-07-27 18:28:57 ERROR juju.worker.uniter uniter.go:482 hook failed: exit status 1
	2014-07-27 18:29:32 INFO start Traceback (most recent call last):
	2014-07-27 18:29:32 INFO start   File "/var/lib/juju/agents/unit-nova-compute-0/charm/hooks/start", line 5, in <module>
	2014-07-27 18:29:32 INFO start     from charmhelpers.core.hookenv import (
	2014-07-27 18:29:32 INFO start   File "/var/lib/juju/agents/unit-nova-compute-0/charm/hooks/charmhelpers/core/hookenv.py", line 9, in <module>
	2014-07-27 18:29:32 INFO start     import yaml
	2014-07-27 18:29:32 INFO start ImportError: No module named yaml
	2014-07-27 18:29:32 ERROR juju.worker.uniter uniter.go:482 hook failed: exit status 1

Weird. Python is missing the yaml module. The nova-compute module should have had this as a dependency, but I'll `sudo apt-get install python-yaml` on both .25 and .26. 

At this point, the nova-compute service still "exists" and I need to tell it to retry, or remove it completely. I tried `juju remove-service nova-compute` and `juju terminate-service nova-compute`, but it still sits there. I found a [charms-destroy](https://juju.ubuntu.com/docs/charms-destroy.html) page.

	ytjohn@ubuntu:~$ juju status | grep -A 11 nova-compute:
	  nova-compute:
	    charm: cs:trusty/nova-compute-3
	    exposed: false
	    life: dying
	    units:
	      nova-compute/0:
	        agent-state: error
	        agent-state-info: 'hook failed: "start"'
	        agent-version: 1.18.4
	        life: dying
	        machine: "2"
	        public-address: 10.10.0.25
	ytjohn@ubuntu:~$ juju resolved nova-compute/0
	ytjohn@ubuntu:~$ juju status | grep -A 11 nova-compute:
	  nova-compute:
	    charm: cs:trusty/nova-compute-3
	    exposed: false
	    life: dying
	    units:
	      nova-compute/0:
	        agent-state: started
	        agent-version: 1.18.4
	        life: dying
	        machine: "2"
	        public-address: 10.10.0.25
	ytjohn@ubuntu:~$ juju status | grep -A 11 nova-compute:
	ytjohn@ubuntu:~$ 

Now it's finally gone. Let's add it again.

	ytjohn@ubuntu:~$ juju deploy nova-compute
	Added charm "cs:trusty/nova-compute-3" to the environment.
	ytjohn@ubuntu:~$ juju status | grep -A 11 nova-compute:
	  nova-compute:
	    charm: cs:trusty/nova-compute-3
	    exposed: false
	    relations:
	      compute-peer:
	      - nova-compute
	    units:
	      nova-compute/0:
	        agent-state: pending
	        agent-version: 1.18.4
	        machine: "3"

This time around, it's adding to to machine "3", which is .26. We'll also want it to go to .25.

	ytjohn@ubuntu:~$ juju add-unit --to 2 nova-compute

While that's running, I want to see if I can get into the openstack dashboard. The guide advises me to set the admin-password, and run juju status to see the dashboard's public ip. Upon doing so, I see that it's on an IP of 10.0.3.197, but the "expose:" is False. Even if I set my workstation up to be on the 10.0.3.x/24 network, I won't be able to reach this IP. This is a problem that should have been dealt with in the beginning. But hopefully I can fix this.

I found this page detaling the issue: http://astokes.org/juju-deploy-to-lxc-and-kvm-in-the-local-provider/ - essentially, I need to bridge lxcbr0, which is wha all those containers are using. Interestingly, this page is also setting up a controller node in containers. 

Let's make the bridge. Change /etc/network/interfaces to create a br0 bridged to eth0. Don't worry about making any changes to lxcbr0.

	# The primary network interface
	auto eth0
	iface eth0 inet manual

	auto br0
	iface br0 inet dhcp
	  bridge_ports eth0 

Then, we need to edit /etc/lxc/default.conf and change the lxc.network.link to br0. This will ensure any NEW containers use the br0 interface.

	lxc.network.type = veth
	lxc.network.link = br0

Finally, we need to edit /var/lib/lxc/*/config and change each devices network link from lxcbr0 to br0.

	sudo -s
	for i in `ls /var/lib/lxc/*/config`; do echo $i; cat $i; done

Now let's reboot. That should setup the networking, restart all conatiners using br0, and hopefully the juju relationships will work out the new IPs. 

Sure enough, after the reboot, we see this a public-address of 10.10.0.185.

	ytjohn@ubuntu:~$ juju status openstack-dashboard
	environment: manual
	machines:
	  "0":
	    agent-state: started
	    agent-version: 1.18.4
	    dns-name: 10.10.0.182
	    instance-id: 'manual:'
	    series: trusty
	    containers:
	      0/lxc/5:
	        agent-state: started
	        agent-version: 1.18.4
	        dns-name: 10.10.0.185
	        instance-id: juju-machine-0-lxc-5
	        series: trusty
	        hardware: arch=amd64
	    hardware: arch=amd64 cpu-cores=1 mem=986M
	services:
	  openstack-dashboard:
	    charm: cs:trusty/openstack-dashboard-4
	    exposed: true
	    relations:
	      cluster:
	      - openstack-dashboard
	      identity-service:
	      - keystone
	    units:
	      openstack-dashboard/0:
	        agent-state: started
	        agent-version: 1.18.4
	        machine: 0/lxc/5
	        open-ports:
	        - 80/tcp
	        - 443/tcp
	        public-address: 10.10.0.185


Bringing up https://10.0.0.185/horizon in the web browser does indeed load the OpenStack dashboard. But once it loaded, I tried to login and go a no data error. Even though the CLI shows a series of relationships, the Juju GUI does not. Perhaps I can recreate these relationships. I went ahead and changed all my 'add-relation' commands to 'remove-relation', removed the relationships, and then re-ran the 'add-relation' commands. This still did not fix it.

As I dug in, I started seeing hook errors, especially with keystone:

    units:
      keystone/0:
        agent-state: error
        agent-state-info: 'hook failed: "identity-service-relation-changed"'

 So let's just try destroying keystone and re-adding it.

 	juju resolved keystone/0
 	juju destroy-service keystone
 	# wait....
 	juju status
 	juju deploy --to lxc:0 keystone

But what's this? When keystone comes up, it's on a 10.0.3.52 address. Now I need to work to figure out what I need to do to get these new containers on the right network.

I take a closer look at /etc/default/lxc and see what I missed before. `USE_LXC_BRIDGE="false"  # overridden in lxc-net`.  Well, now I know I need to edit /etc/default/lxc-net and set USE_LXC_BRIDGE="false". Will do, and then I reboot for good measure. 

That did not fix it either. At this point, 

At this point, I've spent a good 8-16 hours on this project spread out over two weeks. I'm going to have to stop for now and re-think things. It has become abundantly clear in all my searching that OpenStack is a rather advanced system with a lot of features like object store and identity management - much more than I was origianlly looking for. All these features make the initial setup rather complex. 

When it comes right down to it, all I really wanted to do at the beginning of this excercise was do an install that gave me the ability to spin up virtual machines with relative ease - point and click or a quick command. I could keep going down this route, but I need to get more experience with OpenStack first. I also have a more pressing need to get some deployments I have off of bare metal hardware and into virtual containers.

There are some other really good guides to doing this, that I would like to share:

 - First off is the Ultimate OpenStack IceHouse Guide, which I like because it gets past that juju abstraction. If I had found this originally and followed it, I might be done by now.  https://gist.github.com/tmartinx/9177697
 - Secondly is the stackgeek scripts. This is a combination guide and combination automation scripts. It's simliar to DevStack, but seems to be more geared towards actually setting up a production environment. I avoided this initially because I felt I was on the right track with this Juju based install and I felt this was going to be too much like DevStack.

Despite finding these two alternate methods, I won't be able to pursue them right now. What I'm going to do is use DevStack, which I know to have worked for me before. It may not be considered production, but I am the only tenant on this system and will have it isolated from the main Internet. This will allow me to start migrating some bare-metal installs I have into virtual machines. That will in turn free up hardware, which I can use to help build a more robust multi-node OpenStack system. I will have to wipe my two hardware nodes and apply the DevStack script. 



 




