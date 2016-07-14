#!/usr/bin/python
# encoding: utf-8

import subprocess
import re
import json
import datetime


def get_tasks ():
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
		taskName = re.findall("(?<=taskName:)(.+?)(?=,)", item)[0]
		taskID = re.findall("(?<=taskID:)([A-Z0-9-]+)(?=,)", item)[0]
		projectName = re.findall("(?<=projectName:)(.+?)(?=,)", item)[0]

		json_string = '{"task": "' + taskName + '"' + ', "id": "' + taskID + '"' + ', "project": "' + projectName + '"}'
		# print json_string
		data.append(json.loads(json_string))

	return data


def get_active_tasks ():
	api_active_tasks = subprocess.check_output(['osascript', '-e', r'''
		tell application "Tyme2"
			set trackedTasks to trackedTaskIDs
		end tell
		'''])
	
	active_tasks = []
	for taskID in re.findall("[A-Z0-9-]+", api_active_tasks):
		active_tasks.append(taskID)

	return active_tasks


def get_daily_total ():
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
