Title: Gate One supervisor script
Date: 2012-08-02 07:10
Author: John Hogenmiller (john@hogenmiller.net)

Yesterday, I [setup gateone] to run as a non-root user. I also spent
some time looking at potential init scripts for starting and stopping
this. The gateone project does not currently provide any init scripts,
but this is planned for the future ([Issue \#47]). I tried to use one
of the scripts in that thread, but I wasn't really pleased with them.
The big issue is that gateone.py doesn't fork. However, I believe there
is a better solution.

[supervisord] is a python script designed to control and monitor
non-daemonizing python scripts. As Gate One is a foreground only
process, it seems particularly suited to this task - more so than
writing my own script in python or daemontools.

Installation can be done with python-pip or easy\_install. On newer
systems, pip is recommended.

    sudo pip install supervisor

On Ubuntu, pip installs supervisord to /usr/local/bin. By default,
/usr/local/bin is not in root's path, so it makes sense (to me at least)
to create symlinks to /usr/sbin.

    johnh@puppet2:~$ ls /usr/local/bin
    echo_supervisord_conf  pidproxy  supervisorctl  
    supervisordjohnh@puppet2:~$ sudo ln -s /usr/local/bin/supervisord /usr/sbin
    johnh@puppet2:~$ sudo ln -s /usr/local/bin/supervisorctl /usr/sbin

Now, we need to create a configuration file. Supervisord has a utility
to generate a sample one.

    echo_supervisord_conf  > supervisord.conf

To get started, we can use the sample configuration and just add a
couple lines to the bottom for gateone.

     [program:gateone]
     command=/opt/gateone/gateone.py
     directory=/opt/gateone;user=johnh   ; Default is root. Add a user= to setuid

Now, copy supervisord.conf to /etc/supervisord.conf and start
supervisord. Make sure gateone.py is not currently running. Then we'll
run supervisorctl to test things out.

    johnh@puppet2:~$ sudo cp supervisord.conf /etc
    johnh@puppet2:~$ sudo supervisord
    johnh@puppet2:~$ sudo supervisorctl statusgateone
                              RUNNING    pid 9549, uptime 0:00:05
    johnh@puppet2:~$ ps ax | grep
     gateone 9549 ?        Sl     0:00 python /opt/gateone/gateone.py
    johnh@puppet2:~$ sudo supervisorctl stop gateone
    gateone: stopped
    johnh@puppet2:~$ ps ax | grep gateone
     9605 ?        Ss     0:00 dtach -c /opt/gateone/tmp/gateone/../dtach_3 -E -z -r none /opt/gateone/plugins/ssh/scripts/ssh_connect.py -S /tmp/gateone/.../%SHORT_SOCKET% --sshfp -a -oUserKnownHostsFile=/opt/gateone/users/user1@puppet2/ssh/known_hosts 
    9606 pts/3    Ss+    0:00 python /opt/gateone/plugins/ssh/scripts/ssh_connect.py -S /tmp/gateone/.../%SHORT_SOCKET% --sshfp -a -oUserKnownHostsFile=/opt/gateone/users/user1@puppet2/ssh/known_hosts

In this example, we see that gateone.py is started and stopped by
supervisorctl, but because we have dtach enabled, our sessions are still
in place. If we restart gateone.py, we can connect to it again and have
our sessions resumed. While we could probably configure supervisord to
kill these terminals, I believe we'd normally want to keep them running.
The few times I would want to stop those terminals would be a) manually
reconfiguring/troubleshooting opengate, b) updating software, or c)
rebooting the server. For a&b, running the command "gateone.py -kill"
will kill those terminals. For a server shutdown or reboot, the act of
shutting down the OS will kill these terminals.

Finally, we need a way to start and stop supervisord itself.
Fortunately, the supervisord project has provided a number of [init
scripts]. I was able to use the [Debian script] in Ubuntu with only
a few minor changes.

1.  I had symlinked supervisord and supervisorctl to /usr/sbin. The
    script expects them in /usr/bin (but even says that /usr/sbin is a
    better location). I had to change /usr/bin to /usr/sbin.
    Alternatively, you can symlink the files into /usr/bin
2.  I added a status option that runs \$SUPERVISORCTL status
3.  If you started supervisord manually, you must shut it down and start
    it with the script. The script won't be able to stop supervisord
    unless /var/run/supervisord.pid is current.

Here is my complete init script for Ubuntu:

~~~~ {.prettyprint .linenums}
#! /bin/sh### BEGIN INIT INFO# Provides:          supervisord# Required-Start:    $local_fs $remote_fs $networking# Required-Stop:     $local_fs $remote_fs $networking# Default-Start:     2 3 4 5# Default-Stop:      0 1 6# Short-Description: Starts supervisord - see http://supervisord.org# Description:       Starts and stops supervisord as needed - see http://supervisord.org### END INIT INFO# Author: Leonard Norrgard # Version 1.0-alpha# Based on the /etc/init.d/skeleton script in Debian.# Please note: This script is not yet well tested. What little testing# that actually was done was only on supervisor 2.2b1.# Do NOT "set -e"# PATH should only include /usr/* if it runs after the mountnfs.sh scriptPATH=/sbin:/usr/sbin:/bin:/usr/binDESC="Run a set of applications as daemons."NAME=supervisordDAEMON=/usr/sbin/$NAME   # Supervisord is installed in /usr/bin by default, but /usr/sbin would make more sense.SUPERVISORCTL=/usr/sbin/supervisorctlPIDFILE=/var/run/$NAME.pidDAEMON_ARGS="--pidfile ${PIDFILE}"SCRIPTNAME=/etc/init.d/$NAME# Exit if the package is not installed[ -x "$DAEMON" ] || exit 0# Read configuration variable file if it is present[ -r /etc/default/$NAME ] && . /etc/default/$NAME# Load the VERBOSE setting and other rcS variables. /lib/init/vars.sh# Define LSB log_* functions.# Depend on lsb-base (>= 3.0-6) to ensure that this file is present.. /lib/lsb/init-functions## Function that starts the daemon/service#do_start(){        # Return        #   0 if daemon has been started        #   1 if daemon was already running        #   2 if daemon could not be started        [ -e $PIDFILE ] && return 1        start-stop-daemon --start --quiet --pidfile $PIDFILE --exec $DAEMON -- \                $DAEMON_ARGS  \                || return 2        # Add code here, if necessary, that waits for the process to be ready        # to handle requests from services started subsequently which depend        # on this one.  As a last resort, sleep for some time.}## Function that stops the daemon/service#do_stop(){        # Return        #   0 if daemon has been stopped        #   1 if daemon was already stopped        #   2 if daemon could not be stopped        #   other if a failure occurred        [ -e $PIDFILE ] || return 1        # Stop all processes under supervisord control.        $SUPERVISORCTL stop all        start-stop-daemon --stop --quiet --retry=TERM/30/KILL/5 --pidfile $PIDFILE --name $NAME        RETVAL="$?"        [ "$RETVAL" = 2 ] && return 2        # Wait for children to finish too if this is a daemon that forks        # and if the daemon is only ever run from this initscript.        # If the above conditions are not satisfied then add some other code        # that waits for the process to drop all resources that could be        # needed by services started subsequently.  A last resort is to        # sleep for some time.        start-stop-daemon --stop --quiet --oknodo --retry=0/30/KILL/5 --exec $DAEMON        [ "$?" = 2 ] && return 2        # Many daemons don't delete their pidfiles when they exit.        rm -f $PIDFILE        return "$RETVAL"}## Function that sends a SIGHUP to the daemon/service#do_reload() {        #        # If the daemon can reload its configuration without        # restarting (for example, when it is sent a SIGHUP),        # then implement that here.        #        start-stop-daemon --stop --signal 1 --quiet --pidfile $PIDFILE --name $NAME        return 0}case "$1" in  start)        [ "$VERBOSE" != no ] && log_daemon_msg "Starting $DESC" "$NAME"        do_start        case "$?" in                0|1) [ "$VERBOSE" != no ] && log_end_msg 0 ;;                2) [ "$VERBOSE" != no ] && log_end_msg 1 ;;        esac        ;;  stop)        [ "$VERBOSE" != no ] && log_daemon_msg "Stopping $DESC" "$NAME"        do_stop        case "$?" in                0|1) [ "$VERBOSE" != no ] && log_end_msg 0 ;;                2) [ "$VERBOSE" != no ] && log_end_msg 1 ;;        esac        ;;  #reload|force-reload)        #        # If do_reload() is not implemented then leave this commented out        # and leave 'force-reload' as an alias for 'restart'.        #        #log_daemon_msg "Reloading $DESC" "$NAME"        #do_reload        #log_end_msg $?        #;;  restart|force-reload)        #        # If the "reload" option is implemented then remove the        # 'force-reload' alias        #        log_daemon_msg "Restarting $DESC" "$NAME"        do_stop        case "$?" in          0|1)                do_start                case "$?" in                        0) log_end_msg 0 ;;                        1) log_end_msg 1 ;; # Old process is still running                        *) log_end_msg 1 ;; # Failed to start                esac                ;;          *)                # Failed to stop                log_end_msg 1                ;;        esac        ;;  status)        $SUPERVISORCTL status        RETVAL=$?        ;;  *)        #echo "Usage: $SCRIPTNAME {start|stop|restart|reload|force-reload}" >&2        echo "Usage: $SCRIPTNAME {start|stop|restart|force-reload|status}" >&2        exit 3        ;;esac
~~~~

And here is a complete copy of my supervisord.conf file:

~~~~ {.prettyprint .linenums}
[unix_http_server]file=/tmp/supervisor.sock   ; (the path to the socket file)[supervisord]logfile=/tmp/supervisord.log ; (main log file;default $CWD/supervisord.log)logfile_maxbytes=50MB        ; (max main logfile bytes b4 rotation;default 50MB)logfile_backups=10           ; (num of main logfile rotation backups;default 10)loglevel=info                ; (log level;default info; others: debug,warn,trace)pidfile=/tmp/supervisord.pid ; (supervisord pidfile;default supervisord.pid)nodaemon=false               ; (start in foreground if true;default false)minfds=1024                  ; (min. avail startup file descriptors;default 1024)minprocs=200                 ; (min. avail process descriptors;default 200)[rpcinterface:supervisor]supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface[supervisorctl]serverurl=unix:///tmp/supervisor.sock ; use a unix:// URL  for a unix socket[program:gateone]command=/opt/gateone/gateone.pydirectory=/opt/gateonestdout_logfile=/opt/gateone/logs/supervisor.loguser=johnh
~~~~

  [setup gateone]: http://blog.yourtech.us/2012/08/exploring-gateone-browser-ssh-terminal.html
  [Issue \#47]: https://github.com/liftoff/GateOne/issues/47
  [supervisord]: http://www.supervisord.org/
  [init scripts]: https://github.com/Supervisor/initscripts
  [Debian script]: https://raw.github.com/Supervisor/initscripts/master/debian-norrgard
