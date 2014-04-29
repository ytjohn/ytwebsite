Title: Salt The Earth
Date: 2014-04-29 23:10
Author: John Hogenmiller


## Learning Salt

I am just beginning to read up on [SaltStack](http://docs.saltstack.com/en/latest/topics/tutorials/walkthrough.html), but I am really liking it. It has a number of things I like from Ansible (separation from code and state), the targeting abilities of mcollective, and the centralized control of Puppet/Chef. Salt can be run masterless, but in a master/minion configuration, it uses a message queue (0mq) to control minions and get information back. All messages in this queue are encrypted using keys on both the minion and the master. If you distribute this key, you can consume salt generated data in other programs.

Running commands across all minions could look lik this:

    salt '*' test.ping
    salt '*' disk.percent

In these, test.ping and disk.percent are known as 'execution modules', which are essentially python modules that contain defined functions. For example, disk would be an 'execution module' and "percent" would be a function defined. Here, test.ping runs on all target hosts and returns "True"; disk.percent returns the percentage of disk usage on all minions.

You can also run ad-hoc commands.

    salt '*' cmd.run 'ls -l /etc'

Of course, you can target blocks of systems by hostname (`web*` will match web, web1, web02, webserver,..). Salt also has something called [Grains](http://docs.saltstack.com/en/latest/topics/targeting/grains.html) which everyone else calls facts. You can target based on the grains, or use salt to provide a report based on the grains. The following command will return the number of cpus for every 64-bit cpu.

    salt -G 'cpuarch:x86_64' grains.item num_cpus

I *think* this would work as well:

    salt -G 'cpuarch:x86_64 and num_cpus:4' test.ping

If not, these would work (Compound match):

    salt -C 'G@cpuarch:x86_64 and G@num_cpus:4' test.ping
    salt -c 'G@os:Ubuntu or G@os.Debian' test.ping

## Salt States

In Puppet, your manifests and modules are very closely coupled in puppet code. In Ansible, they separate things into modules and "playbooks". These playbooks are yaml files detailing what modules and values for ansible to use. Salt follows this pattern as well, separating execution modules from states with "Salt States", aka SLS formulas (aka state modules).

A sample SLS formual for installing nginx would look like this:

    nginx:
      pkg:
        - installed
      service:
        - running
        - require:
          - pkg: nginx

Assuming you save that in the right spot (/srv/salt/nginx/init.sls), you can apply this state module to all servers starting with the name 'web'.

    salt 'web*' state.sls nginx


So with one tool, you can query a large amount of data from all your minions, move them to a specific state, run ad-hoc style modules, etc. This can also all be expanded by writing your own python modules. Also, I'm mostly interested in the ability to target modules and groups of hosts in one command, but it's worh noting that salt will do scheduling of jobs just like puppet and chef do.




