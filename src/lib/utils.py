#!/usr/bin/python
# encoding: utf-8

import argparse


def search_tasks_and_projects(item):
	elements = []
	elements.append(item['task'])
	elements.append(item['project'])
	return u' '.join(elements)


# def parse_args():
# 	parser = argparse.ArgumentParser()
# 	parser.add_argument("-a", "--active", help="show active tasks", action="store_true")
# 	args = parser.parse_args()
# 	return args

