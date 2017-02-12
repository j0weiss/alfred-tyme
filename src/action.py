#!/usr/bin/python
# encoding: utf-8

import sys

from lib.applescript import *
from lib.database import *


taskID = sys.argv[1]

# get all active tasks
active_tasks = get_active_tasks()

stop_tracker = '''
    tell application "Tyme2"
        StopTrackerForTaskID "{0}"
    end tell
'''.format(taskID)

start_tracker = '''
    tell application "Tyme2"
        StartTrackerForTaskID "{0}"
    end tell
'''.format(taskID)


# ===== MAIN =====
if taskID in active_tasks:
    asrun(stop_tracker)
else:
    asrun(start_tracker)
