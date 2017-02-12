#!/usr/bin/python
# encoding: utf-8

import subprocess
from subprocess import Popen, PIPE
import re
import json
import datetime


def get_tasks():
    apiData = subprocess.check_output(['osascript', '-e', r'''
        set taskList to {"\n"}

        tell application "Tyme2"
            set projectList to every project
            repeat with p in projectList
                set pTasks to every task of p
                repeat with t in pTasks
                    set tName to the name of t
                    set tID to the the id of t
                    set pName to the name of p
                    set newTask to {taskName:tName, taskID:tID, projectName:pName}
                    copy newTask to end of taskList
                    copy "\n" to end of taskList
                end repeat
            end repeat
        end tell

        return taskList'''])

    data = []
    for item in re.findall("taskName:.+?, taskID:.+?, projectName:.+", apiData):
        task_name = re.findall("(?<=taskName:)(.+?)(?=,)", item)[0]
        task_id = re.findall("(?<=taskID:)([A-Z0-9-]+)(?=,)", item)[0]
        project_name = re.findall("(?<=projectName:)(.+?)(?=,)", item)[0]

        json_string = '{"task": "' + task_name + '"' + ', "id": "' + task_id + '"' + ', "project": "' + project_name + '"}'

        # print json_string
        data.append(json.loads(json_string))

    return data


def get_active_tasks():
    api_active_tasks = subprocess.check_output(['osascript', '-e', r'''
        tell application "Tyme2"
            set trackedTasks to trackedTaskIDs
        end tell
        '''])

    active_tasks = []
    for taskID in re.findall("[A-Z0-9-]+", api_active_tasks):
        active_tasks.append(taskID)

    return active_tasks


def get_daily_total():
    daily_total = subprocess.check_output(['osascript', '-e', r'''
        tell application "Tyme2"
            set nowInSeconds to the time of the (current date)
            -- start of the working day is currently at 6 o'clock
            set secondsSinceWorkingDayStart to (nowInSeconds - 60 * 60 * 6)

            set now to current date

            GetTaskRecordIDs startDate (now - secondsSinceWorkingDayStart) endDate now
            set todaysRecordIDs to the fetchedTaskRecordIDs
            set todaysDuration to 0
            repeat with theRecordID in todaysRecordIDs
                GetRecordWithID theRecordID
                set theRecordDuration to the timedDuration of the lastFetchedTaskRecord
                set todaysDuration to todaysDuration + theRecordDuration
            end repeat

            return todaysDuration
        end tell
        '''])

    return str(datetime.timedelta(seconds=float(daily_total)))


def get_daily_records():
    api_daily_record_ids = subprocess.check_output(['osascript', '-e', r'''
        tell application "Tyme2"
            set nowInSeconds to the time of the (current date)
            -- start of the working day is currently at 6 o'clock
            set secondsSinceWorkingDayStart to (nowInSeconds - 60 * 60 * 6)

            set now to current date

            GetTaskRecordIDs startDate (now - secondsSinceWorkingDayStart) endDate now
            return fetchedTaskRecordIDs
        end tell
        '''])

    daily_record_ids = []
    for recordID in re.findall("[A-Z0-9-]+", api_daily_record_ids):
        daily_record_ids.append(recordID)

    daily_records = []
    for recordID in daily_record_ids:
        p = Popen(['osascript', '-e', r'''
            on run argv
                set theID to item 1 of argv
                tell application "Tyme2"
                    GetRecordWithID theID
                    set theStart to the timeStart of the lastFetchedTaskRecord
                    set theEnd to the timeEnd of the lastFetchedTaskRecord
                    set theTaskDuration to (theEnd - theStart)

                    set theID to the relatedTaskID of lastFetchedTaskRecord
                    set theTask to the first item of (every task of every project whose id = theID)
                    set theTaskName to the name of theTask

                    return "{\"taskname\":\"" & theTaskName & "\", \"duration\":" & theTaskDuration & "}"
                end tell
            end run
            ''', recordID], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()

        daily_records.append(json.loads(stdout))

    return daily_records
