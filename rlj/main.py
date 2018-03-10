#!/usr/bin/env python3
# -*- coding=utf-8 -*-
'''_Rqy's local judge.

Usage:
  rlj -h | --help | --version
  rlj [-s] [-j Source] [-c Config] [--O2]
  rlj --genConfig [FILE]
  rlj -d | --delete

Arguments:
  FILE  生成配置文件位置；若未指定，则为config.json

Options:
  -h --help                  输出此信息并退出
  --version                  输出版本号并退出
  -s --silent                简化输出消息
  -j Source --judge=Source   评测制定源文件
  -c Config --config=Config  指定配置文件 [default: config.json]
  --O2                       编译时打开O2选项
  --genConfig                生成配置文件
  -d --delete                刪除temp文件夹
'''

import colorama
import os
import json
import sys
import docopt
from .constants import __version__
from .languages import getLanguage
from .judge import Judge


def addColor(color, text):
    return getattr(colorama.Fore, color) + text + colorama.Fore.RESET


def addBgColor(color, text):
    return getattr(colorama.Back, color) + getattr(colorama.Fore, 'BLACK')\
        + ' ' + text + ' ' + colorama.Fore.RESET + colorama.Back.RESET


def addStyle(style, text):
    return getattr(colorama.Style, style) + text + colorama.Style.RESET_ALL


def printResult(lang, result, silent=False):
    if not silent:
        print('=' * 30)
        print(addStyle('BRIGHT', addColor('BLUE', 'Language: '))
              + addBgColor('BLUE', lang['name']))
        print('正在编译...')

    compileStatusColor = {'CTLE': 'YELLOW', 'ERROR': 'RED', 'DONE': 'GREEN'}

    compile_status = result.__next__()
    color = compileStatusColor[compile_status[0]]
    print(addBgColor(color, compile_status[0])
          + addColor(color, compile_status[1]), end='')
    if compile_status[0] == 'DONE':
        print(addColor(color, ', 用时：%.3fs' % compile_status[2]))
    else:
        if not silent:
            print('\n' + '=' * 30)
        if compile_status[0] == 'ERROR':
            os.system('cat temp/compile.log')
            print('=' * 30)
        return False

    statusColor = {'AC': 'GREEN', 'WA': 'RED', 'TLE': 'YELLOW',
                   'MLE': 'BLUE', 'RE': 'CYAN'}
    if silent:
        num = {'AC': 0, 'WA': 0, 'TLE': 0, 'MLE': 0, 'RE': 0}
        for tesk in result:
            st = tesk[1].status
            print(addBgColor(statusColor[st], st[0]), end='')
            num[st] += 1
            sys.stdout.flush()
        print()
        for st in statusColor:
            if not num[st]:
                continue
            print(addBgColor(statusColor[st], st[0] + ':%d' % num[st]),
                  end=' ')
        print()
    else:
        print('=' * 30)
        print('测试点\t状态\t内存\t时间')
        print('=' * 30)
        tot_time = 0
        max_memory = 0
        for tesk in result:
            s = str(tesk[0]) + '\t'
            st = tesk[1].status
            s += addBgColor(statusColor[st], st) + '\t'
            s += str(int(tesk[1].memory_used)) + 'MB' + '\t'
            s += ('%.3f' % (tesk[1].time_used / 1000)) + 's' + '\t'
            if tesk[1].status == 'AC':
                tot_time += tesk[1].time_used
                max_memory = max(max_memory, tesk[1].memory_used)
            print(s)
        print('=' * 30)
        print('总时:%.3fs\n最大空间:%dMB' % (tot_time / 1000, int(max_memory)))
    return True


def checkFiles(config):
    Input = config['Input']
    Output = config['Output']
    if not os.path.exists(config['Source']):
        raise FileNotFoundError('源文件{}不存在！'.format(config['Source']))
    for tesk in config['#']:
        inputName = str(tesk).join(Input.split('#'))
        outputName = str(tesk).join(Output.split('#'))
        if not os.path.exists('data/' + inputName):
            raise FileNotFoundError('输入文件{}不存在！'.format(inputName))
        if not os.path.exists('data/' + outputName):
            raise FileNotFoundError('输出文件{}不存在！'.format(outputName))


def getArgument(name, default=None, indent=0):
    indent = ' ' * indent
    if default is not None:
        value = input('%s%s（默认为%s）: ' % (indent, name, default)).strip()
        if not value:
            value = default
    else:
        value = input('%s%s: ' % (indent, name)).strip()
        while not value:
            value = input('%s请输入%s: ' % (indent, name)).strip()
    return value


def genConfig(fileName):
    if os.path.exists(fileName):
        ans = input('文件{}已存在，是否要覆盖(Y/n)？'.format(fileName)).strip()
        while ans != '' and (len(ans) > 1 or ans not in 'YyNn'):
            ans = input(
                '文件{}已存在，是否要覆盖(Y/n)？'.format(fileName)).strip()
        if ans == 'N' or ans == 'n':
            return

    name = getArgument('题目名')
    source = getArgument('源文件名', default=(name + '.cpp'))
    print('数据:')
    input_file = getArgument('输入文件', default=(name + '#.in'), indent=2)
    output_file = getArgument('输出文件', default=(name + '#.ans'), indent=2)
    a, b = None, None
    while a is None or a > b:
        if a is not None:
            print('  输入错误（可能你想输入{} {}）'.format(b, a))
            a = b = None
        try:
            num_str = getArgument('"#"的范围', default='1 1', indent=2)
            a, b = map(int, num_str.split())
        except ValueError:
            pass
    num = range(a, b + 1)
    time_limit = getArgument('时间限制(ms)', default='1000')
    memory_limit = getArgument('空间限制(MB)', default='128')
    with open(fileName, 'w') as f:
        f.writelines([
            '{\n',
            '  "Source"      : "{}",\n'.format(source),
            '  "Input"       : "{}",\n'.format(input_file),
            '  "Output"      : "{}",\n'.format(output_file),
            '  "#"           : {},\n'.format(list(num)),
            '  "Time Limit"  : {},\n'.format(time_limit),
            '  "Memory Limit": {}\n'.format(memory_limit),
            '}\n',
            ])


def main():
    arguments = docopt.docopt(__doc__, help=True, version=__version__)
    # print(arguments)
    if arguments['--genConfig']:
        fileName = arguments['FILE']
        if fileName is None:
            fileName = 'config.json'
        genConfig(fileName)
        return
    elif arguments['--delete']:
        os.system('rm -rf temp')
        return
    try:
        configFile = arguments['--config']
        if not os.path.exists(configFile):
            raise FileNotFoundError('配置文件{}不存在！'.format(configFile))
        with open(configFile, 'r') as f:
            config = json.load(f)
        if arguments['--O2']:
            config['Compiling Parameter'] = '-O2 ' + config.get(
                    'Compiling Parameter', '')
        if arguments['--judge'] is not None:
            config['Source'] = arguments['--judge']

        checkFiles(config)

        is_silent = arguments['--silent']

        judger = Judge(config)
        if not printResult(getLanguage(config['Source']),
                           judger.judge(), is_silent):
            exit(1)

        if not is_silent and judger.runner.firstWA is not None:
            print('你在第{}个测试点出错了，\ndiff信息在diff_log中'.format(
                judger.runner.firstWA))
            print('=' * 30)
    except FileNotFoundError as e:
        print('错误：' + str(e))
        exit(1)


if __name__ == '__main__':
    main()
