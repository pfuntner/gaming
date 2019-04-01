#! /usr/bin/env python

import sys
import time
import datetime
import subprocess

pgm = sys.argv[0]

subprocess.Popen(['/usr/sbin/sshd']).wait()

with open('/tmp/waiter.log', 'w') as stream:
  while True:
    now = datetime.datetime.now()
    msg = '{pgm} running at {now}'.format(**locals())
    stream.write('{msg}\n'.format(**locals()))
    stream.flush()
    print msg
    time.sleep(60**2)
