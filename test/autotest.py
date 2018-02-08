#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import os

def clean_screen():
    print ('\n' * 100)

def change_dir(dir, cwd):
    os.chdir(cwd + "/" + dir)

def run_test(case):
    change_dir(case, work_dir)
    ret_code = os.system("python3 ../../rlj/main.py")

test_cases = os.listdir()
test_cases.remove("autotest.py")
work_dir = os.getcwd()
for i in test_cases:
    run_test(i)
