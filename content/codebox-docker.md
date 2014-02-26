Title: Codebox in Docker
Date: 2014-02-26
Author: John Hogenmiller

This is a quick note log. I was able to setup a self-hosted web IDE for programming. Today I tested out codebox.io,
but I also want to check out the open source [Cloud9 IDE](https://github.com/dotcloud/hipache).

 - [Codebox.io](https://www.codebox.io) an open-source Web IDE for programming (in your browser)
 - [Docker](http://www.docker.io/) an open source container
 - [Docker-Codebox](https://github.com/forty9ten/docker-codebox/blob/master/Dockerfile). All I really want is this guy's Dockerfile.
 
I already have Docker installed, that's the easy bit.

## Build the box:
~~~~
git clone https://github.com/forty9ten/docker-codebox.git
cd docker-codebox
docker build -t ytjohncodebox .
# much building occurs
~~~~

### Run codebox in docker

This will run the codebox.io environment on port 8000 and you'll be editing files that are stored in a directory
called workspace1. ~/workspace1 on the host gets mounted into /workspace1 in the container.

~~~~
cd ~
mkdir workspace1
docker run -p 8000:8000 -v ./workspace1:/workspace1 -t ytjohncodebox -p 8000 run /workspace1
# many things happen
# I end up seeing this:
# Codebox is running at http://localhost:8000
~~~~

Now, I can access my server on port 8000 (ie, http://192.168.1.32:8000/). This instance is unprotected, it just asks
for an email to get started. But the part I skipped over is that I am actually using nginx to proxy and password
protect this instance. 

I can hit Ctrl+C on the terminal to cancel my instance and all my edited files are safely stored in ~/workspace1.

Interesting bits:
I create a new file in the web browser and save it, I see this bit of json in the console output:

~~~~
[events] watch.change.create : { change: 'create',
  path: '/irule.txt',
  stats: 
   { current: 
      { dev: 64513,
        mode: 33188,
        nlink: 1,
        uid: 0,
        gid: 0,
        rdev: 0,
        blksize: 4096,
        ino: 262847,
        size: 27,
        blocks: 8,
        atime: Wed Feb 26 2014 05:18:44 GMT+0000 (UTC),
        mtime: Wed Feb 26 2014 05:18:42 GMT+0000 (UTC),
        ctime: Wed Feb 26 2014 05:18:42 GMT+0000 (UTC) },
     old: null } }
~~~~

One thing I really need is the ability to open a web terminal. When I do though, the terminal window appears for a
few seconds, and then vanishes. In the console, I see this:

~~~~
[log][shells.stream] new socket connected
[log][shells.stream] open shell  { shellId: 'term2020-44',
  opts: { rows: 80, columns: 24, id: 'term2020-44' } }
[log][events] shell.spawn : { shellId: 'term2020-44' }
[log][events] shell.attach : { shellId: 'term2020-44' }
[log][events] shell.open : { shellId: 'term2020-44' }
[log][events] shell.exit : { shellId: 'term2020-44' }
[log][shells.stream] socket disconnected
[log][shells.stream] socket disconnected
[log][hooks] use hook settings
~~~~

I got this same issue going through my nginx proxy and connecting directly on port 8000. A bit of text flashes 
quickly on the "terminal" in the web browser, but closes too quickly for me to catch it. Perhaps it's attempting to
run something that is not installed in the Docker instance. If I can fix that, then I just need to come up with a cool
way to launch workspaces and tie them into my nginx setup (or switch over to [hipache](https://github.com/dotcloud/hipache)
as my front-end webserver).

Anyways, just wanted to record these steps here and show how easy it could be to get your own self hosted IDE.

