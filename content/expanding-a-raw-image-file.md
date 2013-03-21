Title: Expanding a raw image file
Date: 2011-01-13 05:57
Author: John Hogenmiller (john@hogenmiller.net)

 On one of my customer's devices, the backup software requires that the
backups go to a separate partition (or drive).  However, the customer
only has one raid array and the bulk of the space is in /home.   To work
around this limitation, I created a raw image file called backup.img,
which gets mounted as /backup.   After the software performs its local
backup, I use duplicity to backup /backup remotely to a backup server at
my location (with encryption).  
  
Today I got an alert that /backup was running low on space.  It was an
80GB image and 61GB was in use, leaving only 15GB free.  Now, this
amount of free space should last quite a while.  However, the software
(cPanel)  has a known issue for years that the 80% limit is hardcoded
into the program.  I can change this, but every time cPanel updates, it
overwrites that change.  
  
So to be proactive, I decided to go ahead and increase the image size.  
  
In order to increase the size of an image, you simply unmount your raw
image and use the dd command.  
  

> \# Increase by \~20GB  
> dd if=/dev/zero bs=1M count=20480 \>\> backup.img  
> \# 20,480 is 20,480 MB or \~20GB  
>   
> \# check the filesystem  
> /sbin/e2fsck -f backup.img  
> \# resize the filesystem  
> /sbin/resize2fs backup.img  
> \# check the filesystem again  
> e2fsck -f backup.img               

--  
  
Expanding a raw image file By Administrator on January 13, 2011 5:57 AM
