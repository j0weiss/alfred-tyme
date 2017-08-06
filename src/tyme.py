#!/usr/bin/python
# encoding: utf-8

import sys
import argparse

from workflow import Workflow, ICON_CLOCK, ICON_SYNC, ICON_NOTE, ICON_INFO

from lib.database import *
from lib.utils import *


log = None


def main(wf):
    log.debug('Started Workflow')
    args = parse_args()

    # Get query from Alfred
    query = None
    if args.query:
        query = args.query[0]

    # retrieve tasks from cache if available
    tasks = wf.cached_data('tasks', get_tasks, max_age=0)
    # get all active tasks
    active_tasks = get_active_tasks()

    # if query is given, filter posts
    if query:
        tasks = wf.filter(query, tasks, key=search_tasks_and_projects)

    # loop through the tasks and add an item for each to the list of results for Alfred
    if args.active and not active_tasks:
            wf.add_item(title="There are no active tasks",
                        valid=False,
                        icon=ICON_NOTE)
    elif args.active:
        for task in tasks:
            if task['id'] in active_tasks:
                wf.add_item(title=task['task'],
                            subtitle=task['project'],
                            arg=task['id'],
                            valid=True,
                            icon=ICON_SYNC)
    elif args.statistics:
        wf.add_item(title=get_daily_total(),
                    subtitle='Daily Total',
                    valid=False)
        daily_records = get_daily_records()
        for record in daily_records:
            wf.add_item(title=record['taskname'],
                        subtitle=str(datetime.timedelta(seconds=record['duration'])),
                        valid=False,
                        icon=ICON_INFO)
    else:
        for task in tasks:
            icon = None
            if task['id'] in active_tasks:
                icon = ICON_SYNC
            else:
                icon = ICON_CLOCK

            wf.add_item(title=task['task'],
                        subtitle=task['project'],
                        arg=task['id'],
                        valid=True,
                        icon=icon)

    # Send the results to Alfred as XML
    wf.send_feedback()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--active', action='store_true',
                        help='show active tasks only')
    parser.add_argument('-stats', '--statistics', action='store_true',
                        help='show todays statistics')
    parser.add_argument('query', type=unicode, nargs=argparse.REMAINDER, help='query string')
    log.debug(workflow.args)
    args = parser.parse_args(workflow.args)
    return args


if __name__ == u"__main__":
    workflow = Workflow()
    log = workflow.logger
    sys.exit(workflow.run(main))
