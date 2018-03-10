# import pytest
from rlj import Judge, JudgeStatus
import os

config = {
    'Input': 'test#.in',
    'Output': 'test#.ans',
    '#': [1, 2],
    'Time Limit': 100,
    'Memory Limit': 1
}


def getConfig(st):
    new_config = config.copy()
    new_config['Source'] = st + '.cpp'
    return new_config


def runTest1(st):
    result = list(Judge(getConfig(st)).judge())
    compile_status = result[0]
    assert compile_status[0] == 'DONE'
    assert compile_status[1] == '编译成功'
    assert result[1] == (1, JudgeStatus(st, 2, 0.5, 0))
    assert result[2] == (2, JudgeStatus(st, 2, 0.5, 0))


def test_1():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    runTest1('AC')
    runTest1('WA')
    runTest1('TLE')
    runTest1('MLE')
    runTest1('RE')


def runTest2(st, chn):
    result = list(Judge(getConfig(st)).judge())
    compile_status = result[0]
    assert compile_status[0] == st
    assert compile_status[1] == chn


def test_2():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    runTest2('ERROR', '编译错误')
    runTest2('CTLE', '编译超时')
