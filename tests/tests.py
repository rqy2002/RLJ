# import pytest
from rlj import Judge, JudgeStatus, Config, makeConfig
import os


arguments = {
    '--O2': False,
    '--delete': False,
    '--genConfig': False,
    '--help': False,
    '--silent': False,
    '--version': False,
    '-c': 'config.yml',
    '-j': None,
    'FILE': None
}


def getConfig(st):
    new_arg = arguments.copy()
    new_arg['-j'] = st + '.cpp'
    return makeConfig('config.yml', new_arg)


def runTest1(st):
    result = list(Judge(getConfig(st)).judge())
    compile_status = result[0]
    print(result)
    print(compile_status)
    assert compile_status[0] == 'DONE'
    assert compile_status[1] == '编译成功'
    assert result[1] == (1, ('data/test1.in', 'data/test1.ans'),
                         JudgeStatus(st, 2, 0.5, 0))
    assert result[2] == (2, ('data/test2.in', 'data/test2.ans'),
                         JudgeStatus(st, 2, 0.5, 0))


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
