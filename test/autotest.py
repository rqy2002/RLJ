#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import os

def clean_screen():
    print ('\n' * 100)

def change_dir(dir, cwd):
    os.chdir(cwd + "/" + dir)

def run_test(case):
    change_dir(case, work_dir)
    ret_code = os.system("py -3 ../../rlj/main.py")
    if ret_code != 0:
        clean_screen()
        print ("====================================")
        print ("Some thing wrong at test {0}".format(case))
        print ("====================================")
        exit(0)

test_cases = os.listdir()
test_cases.remove("autotest.py")
work_dir = os.getcwd()
for i in test_cases:
    run_test(i)
