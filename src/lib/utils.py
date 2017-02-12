#!/usr/bin/python
# encoding: utf-8


def search_tasks_and_projects(item):
    elements = []
    elements.append(item['task'])
    elements.append(item['project'])

    return u' '.join(elements)
