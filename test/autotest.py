#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import os

def clean_screen():
    print ('\n' * 100)

def change_dir(dir):
    os.chdir(os.getcwd() + "/" + dir)

def run_test(case):
    change_dir(case)
    ret_code = os.system("rlj")
    if ret_code != 0:
        clean_screen()
        print ("====================================")
        print ("Some thing wrong at test {0}".format(case))
        print ("====================================")
        exit(0)

test_cases = os.listdir()
test_cases.remove("autotest.py")
for i in test_cases:
    run_test(i)
