Title: C270 Review
Date: 2014-02-01
Author: John Hogenmiller

# Acer C270 Chromebook

Last week I picked up a Chromebook, specifically the Acer C270. One of my coworkers uses one and kind of convinced me that one would be worth checking. I compared what was out there and other than the Pixel, the C270 had the best specs, including battery life (8.5 hours). It's an Intel chipset, 16GB space, 2Gb of RAM, 1.4Ghz.

## The good:

 - You get a lot of functionality for $200.
 - 7 seconds from power off to browser up and running.
 - Both an ssh client and vim are installed by default.
 - The keyboard is fairly responsive.
 - Runs forever without needing a charge.
 - You can install a real OS alongside ChromeOS (using Crouton) and switch between the two without rebooting.
 - It can do web pages and has a built in terminal shell.
 - With Ubuntu installed in a chroot environment, it does everything my regular computer does (and I almost never have to fire up the gui, which would be a battery drain).
 - This does Netflix, Amazon Prime, Hulu and 
 - I haven't done this, but one could replace the drive with a 128GB SSD for $100. 
 
## The bad:

 - Unfortunately the SD card slot isn't very deep. Any SD Card you insert will stick out the side. I was hoping to drop a 64GB sdcard inside here and store videos/music/projects on this card. But since it sticks out so far, I might as well use a USB drive.
 - The trackpad requires an annoying amount of pressure to right click or click and hold (dragging/highlighting). It also makes a loud click when you do this. 

After working on this for the last week, I decided that this Chromebook is exactly what I was hoping my Asus 904 netbook would be. A responsive, long lasting, carry anywhere type computer. It has made me regret purchasing my Nexus 7. I get a lot more daily use out o fthe 11" Chromebook.

So what am I using this for? A lot of things. Anything really. My primary use case for this was actually amateur radio. In my ubuntu chroot environment, I installed [CHIRP](http://chirp.danplanet.com/) to program my radios, [flidgi](http://www.w1hkj.com/Fldigi.html) for operating digital modes, [xlog](http://xlog.nongnu.org/) for QSO logging, and Wine+[APRSISCE](aprsisce.wikidot.com) for APRS action. So far these programs seem to work without issue. I've been able to program radios, send PSK data to PSKDroid on my cell phone using acoustic coupling, and view APRS activity using APRSISCE. When I'm not doing ham radio activity, I leave the X-windows session shut down (and it only takes about 5 seconds to start it up again).

Beyond ham radio, I'm using it to browse the web (duh), ssh into my servers, write python code, and right now... writing this post. Earlier today I fired up a Jenkins server on AWS. I've been meaning to set one up for a long time, and I have a year of AWS's free tier currently. So from this chromebook, I selected a jenkins instance from the AWS market, SSH'd into and add pelican to it. Then I was able to setup a simple jenkins job that would publish my website from github. Then I went over to github and added a commit hook that calls my new jenkins job. Now, anytime I commit into my [website's github repository](https://github.com/ytjohn/ytwebsite/) (including editing it from github directly), jenkins will automatically publish it. Doing this on my tablet, even with the keyboard, would have been frustrating. 

Basically, despite even Google's marketing, their Chromebook is NOT a web browser only type device. It is a full computer. If you're used to Linux desktops and servers, you can do anything on it that you can on your existing setup. Yes, the impressive battery life is obtainable by using ChromeOS and using X-Windows or other cpu heavy applications will bring that battery life down. But even when I left X-windows up for long periods of time (for instance, letting the linux side download updates) it only had a moderate impact on my battery life.

If you're looking for a "carry anywhere, do anything" computing device, the C270 is well worth the price. 
