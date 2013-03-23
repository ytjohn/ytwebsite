Title: pysphere - VMWare in Python
Date: 2012-08-23 22:30
Author: John Hogenmiller (john@hogenmiller.net)
Tags: api, python, programming, vmware, pysphere

I do a good bit of work with VMWare vSphere and I've been wanting to
work more with their API. Everything (except console) that you can do in
the vSphere client, you should be able to do through a web-based API.  
Unfortunately, it seems that VMWare does not provide an SDK for Python,
my current language of choice. I could work in Perl or Java, but I want
to develop a web application, which I don't want to do in Perl.
Fortunately, I found [pysphere], which is a fairly active project of
implementing the VI API in python. It might not fully implement the API,
but it looks relatively stable and easy to implement. Plus, if I find
any functionality missing, I can extend the class directly.  
I followed their [Getting Started][pysphere] page to get it installed
and get connected, but I didn't like having my password right there in
my working code. This was easily resolved by installing [PyYaml] and
creating a config.yaml file. Then, it was just a matter of following
along with the examples to make a good test script.  
My config.yaml:  

    server: esxi1.example.com
    user: john
    pass: password


My test.py:  

    #!/usr/bin/python
    
    import yaml
    from pysphere import *
    
    f = open('config.yaml')
    config = yaml.load(f)
    f.close()
    
    server = VIServer()
    server.connect(config["server"], config["user"], config["pass"])
    
    print server.get_server_type(), server.get_api_version()
    vm1 = server.get_vm_by_name("puppet1-centos6")
    print vm1.get_property('name'), vm1.get_property('ip_address')

And does it work?  

    $ ./test.py
    VMware vCenter Server 5.0
    puppet1-centos6 10.100.0.206

I was even able to go so far as cloning a vm (vm2 = vm1.clone('new vm'))
and can already see massive possibilities with this library in its
current state. The API can be queried much like a simple database, and
objects acted upon with simple statements. Operations like my vm clone
can be setup as a task and run asynchrously. I could easily see
integrating this with something like [tornado], [twisted], or even
[cyclone] to make a non-blocking web framework.

  [pysphere]: http://code.google.com/p/pysphere/wiki/GettingStarted
  [PyYaml]: http://pyyaml.org/wiki/PyYAML
  [tornado]: http://www.tornadoweb.org/
  [twisted]: http://twistedmatrix.com/
  [cyclone]: http://cyclone.io/
