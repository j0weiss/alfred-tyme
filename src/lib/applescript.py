#!/usr/bin/python
# encoding: utf-8

import subprocess


# Run the given AppleScript and return the standard output and error
def asrun(ascript):
    osa = subprocess.Popen(['osascript', '-'],
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE)

    return osa.communicate(ascript)[0]


# Return the AppleScript equivalent of the given string
def asquote(astr):
    astr = astr.replace('"', '" & quote & "')

    return '"{}"'.format(astr)
