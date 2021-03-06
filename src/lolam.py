#!/usr/bin/env python3

from time import sleep
from daemon.pidfile import TimeoutPIDLockFile
import daemon
import os
import sys
import configparser
from datetime import datetime

from servo import Servo
from mail import GmailWrapper
from scheduler import build_scheduler

CWD = os.getcwd()

PID_FILE = os.path.join(CWD, "lolampy.pid")
LOG_FILE = os.path.join(CWD, "lolampy.log")

def feed(config):
    print("%s: feeding" % datetime.now(), file=sys.stderr)
    servo = Servo(18)
    servo.start()

    base_duty = 7.5
    base_delta_duty = 5
    servo.do_cycle(base_duty - base_delta_duty)
    servo.do_cycle(base_duty + base_delta_duty)
    servo.do_cycle(base_duty - base_delta_duty)

    servo.clean()
    
def get_config(config_file):
    try:
        open(config_file)
    except:
        print("Unreadable configuration file '%s'" % config_file, file=sys.stderr)
        exit(1)
    
    defaults = {
        "use_email" : True,
        "send_confirmation" : False
    }
    
    config = configparser.SafeConfigParser(defaults=defaults)
    config.read(config_file)
    
    return config

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage is %s config_file" % sys.argv[0], file=sys.stderr)
        exit(1)
        
    config = get_config(sys.argv[1])
    pid_file = TimeoutPIDLockFile(PID_FILE)
    
    with open(LOG_FILE, "w+") as log_file:
        # start the daemon
        daemon_context = daemon.DaemonContext(
            stdout=log_file,
            stderr=log_file,
            pidfile=pid_file,
            working_directory = CWD
        )
        
        with daemon_context:
            # initialise the scheduler
            try:
                use_email = config.getboolean("general", "use_email")
                sleeping_time = config.getint("general", "sleeping_time")
                if use_email:
                    username = config.get("email", "username")
                    pwd = config.get("email", "password")
                    send_confirmation = config.getboolean("email", "send_confirmation")
                    if send_confirmation:
                        confirmation_address = config.get("email", "send_confirmation_to")
                scheduler = build_scheduler(config)
            except BaseException as e:
                print("Caught the following exception during the parsing of the configuration file: %s" % str(e), file=sys.stderr)
                exit(1)
                
            while True:
                # check the scheduler
                if scheduler.is_feeding_time():
                    feed(config)
                    scheduler.set_next()
                    if use_email and send_confirmation:
                        try:
                            wrapper = GmailWrapper(username, pwd)
                            wrapper.send_confirmation(confirmation_address)
                        except BaseException as e:
                            print("Caught the following exception while trying to send a confirmation email: %s" % str(e), file=sys.stderr)
                
                # check the email if necessary
                if use_email:
                    try:
                        wrapper = GmailWrapper(username, pwd)
                        ids = wrapper.get_unread_ids_by_subject("cibo")
                        if len(ids) > 0:
                            wrapper.mark_as_read(ids)
                            feed(config)
                        
                        sleep(sleeping_time)
                    except BaseException as e:
                        print("Caught the following exception while trying to access the email: %s" % str(e), file=sys.stderr)

