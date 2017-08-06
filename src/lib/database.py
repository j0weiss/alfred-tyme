#!/usr/bin/python
# encoding: utf-8

import datetime
import applescript


def get_tasks():
    scpt = applescript.AppleScript('''
        set taskList to {}

        tell application "Tyme2"
            set projectList to every project
            repeat with p in projectList
                set pTasks to every task of p
                repeat with t in pTasks
                    set tName to the name of t
                    set tID to the the id of t
                    set pName to the name of p
                    set newTask to {task_name:tName, task_id:tID, project_name:pName}
                    copy newTask to end of taskList
                end repeat
            end repeat
        end tell

        return taskList
    ''')

    tasks = scpt.run()

    for task in tasks:
        task["task"] = task.pop("task_name")
        task["id"] = task.pop("task_id")
        task["project"] = task.pop("project_name")

    return tasks


def get_active_tasks():
    scpt = applescript.AppleScript('''
        tell application "Tyme2"
            set trackedTasks to trackedTaskIDs
        end tell
        ''')

    return scpt.run()


def get_daily_total():
    scpt = applescript.AppleScript('''
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
        ''')

    daily_total = scpt.run()

    return str(datetime.timedelta(seconds=float(daily_total)))


def get_daily_records():
    scpt = applescript.AppleScript('''
        tell application "Tyme2"
            set nowInSeconds to the time of the (current date)
            -- start of the working day is currently at 6 o'clock
            set secondsSinceWorkingDayStart to (nowInSeconds - 60 * 60 * 6)

            set now to current date

            GetTaskRecordIDs startDate (now - secondsSinceWorkingDayStart) endDate now
            return fetchedTaskRecordIDs
        end tell
        ''')

    daily_record_ids = scpt.run()

    daily_records = []
    for recordID in daily_record_ids:
        scpt = applescript.AppleScript('''
            on run {theID}
                tell application "Tyme2"
                    GetRecordWithID theID
                    set theStart to the timeStart of the lastFetchedTaskRecord
                    set theEnd to the timeEnd of the lastFetchedTaskRecord
                    set theTaskDuration to (theEnd - theStart)

                    set theID to the relatedTaskID of lastFetchedTaskRecord
                    set theTask to the first item of (every task of every project whose id = theID)
                    set theTaskName to the name of theTask

                    return {taskname:theTaskName, duration:theTaskDuration}
                end tell
            end run
            ''')

        daily_records.append(daily_records_script.run(recordID))

    return daily_records


def set_note(task_id, note):
    set_note_script = applescript.AppleScript('''
        on run {theID, theNote}
            tell application "Tyme2"
                set theTask to the first item of (every task of every project whose id = theID)
                set theRecords to every taskRecord of theTask

                repeat with theRecord in theRecords
                    set theRecordTimeEnd to timeEnd of theRecord
                    log theRecordTimeEnd
                end repeat

                set theCurrentRecord to the last item of theRecords
                set theCurrentRecordTimeEnd to timeEnd of theCurrentRecord
                log theCurrentRecordTimeEnd
                set the properties of theCurrentRecord to {note:theNote}
            end tell
        end run
    ''')

    set_note_script.run(task_id, note)
