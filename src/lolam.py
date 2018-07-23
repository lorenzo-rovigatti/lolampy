#!/usr/bin/env python3

from time import sleep
from daemon.pidfile import TimeoutPIDLockFile
import daemon
import os

from Servo import Servo
from Mail import GmailWrapper

CWD = os.getcwd()

PID_FILE = os.path.join(CWD, "lolampy.pid")
LOG_FILE = os.path.join(CWD, "lolampy.log")

if __name__ == '__main__':
    pid_file = TimeoutPIDLockFile(PID_FILE)
    with open(LOG_FILE, "w+") as log_file:
        daemon_context = daemon.DaemonContext(
            stdout=log_file,
            stderr=log_file,
            pidfile=pid_file,
            working_directory = CWD
        )

        with daemon_context:
            with open("user") as f:
                username = f.readline().strip()

            with open("pwd") as f:
                pwd = f.readline().strip()

            while True:
                wrapper = GmailWrapper(username, pwd)
                ids = wrapper.get_unread_ids_by_subject("gira")
                if len(ids) > 0:
                    wrapper.mark_as_read(ids)

                    servo = Servo(18)
                    servo.start()

                    base_duty = 7.5
                    base_delta_duty = 5
                    servo.do_cycle(base_duty - base_delta_duty)
                    servo.do_cycle(base_duty + 2. * base_delta_duty)
                    servo.do_cycle(base_duty - base_delta_duty)

                    servo.clean()

                sleep(10)
