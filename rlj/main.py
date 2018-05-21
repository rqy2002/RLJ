#!/usr/bin/env python3
# -*- coding=utf-8 -*-
'''_Rqy's local judge.

Usage:
  rlj -h | --help | --version
  rlj [-s] [-j Source] [-c Config] [--O2]
  rlj --genConfig [FILE]
  rlj -d | --delete

Arguments:
  FILE  生成配置文件位置；若未指定，则为config.yml

Options:
  -h --help    输出此信息并退出
  --version    输出版本号并退出
  -s --silent  简化输出消息
  -j Source    评测制定源文件
  -c Config    指定配置文件 [default: config.yml]
  --O2         编译时打开O2选项
  --genConfig  生成配置文件
  -d --delete  刪除temp文件夹
'''

import colorama
import os
import sys
import docopt
from .constants import __version__
from .languages import getLanguage
from .judge import Judge
from .config import Config, genConfig


def addColor(color, text):
    return getattr(colorama.Fore, color) + text + colorama.Fore.RESET


def addBgColor(color, text):
    return getattr(colorama.Back, color) + getattr(colorama.Fore, 'BLACK')\
        + ' ' + text + ' ' + colorama.Fore.RESET + colorama.Back.RESET


def addStyle(style, text):
    return getattr(colorama.Style, style) + text + colorama.Style.RESET_ALL


def printResult(lang, result, silent=False):
    if not silent:
        print('=' * 70)
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
            print('\n' + '=' * 70)
        if compile_status[0] == 'ERROR':
            os.system('cat temp/compile.log')
            print('=' * 70)
        return False

    statusColor = {'AC': 'GREEN', 'WA': 'RED', 'TLE': 'YELLOW',
                   'MLE': 'BLUE', 'RE': 'CYAN'}
    if silent:
        num = {'AC': 0, 'WA': 0, 'TLE': 0, 'MLE': 0, 'RE': 0}
        for task in result:
            st = task[2].status
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
        print('=' * 70)
        print('编号\t输入文件\t输出文件\t状态\t内存\t时间')
        print('=' * 70)
        tot_time = 0
        max_memory = 0
        for task in result:
            s = '{0}\t{1[0]}\t{1[1]}\t'.format(task[0], task[1])
            st = task[2].status
            s += addBgColor(statusColor[st], st) + '\t'
            s += str(int(task[2].memory_used)) + 'MB' + '\t'
            s += ('%.3f' % (task[2].time_used / 1000)) + 's' + '\t'
            if task[2].status == 'AC':
                tot_time += task[2].time_used
                max_memory = max(max_memory, task[2].memory_used)
            print(s)
        print('=' * 70)
        print('总时:%.3fs\n最大空间:%dMB' % (tot_time / 1000, int(max_memory)))
    return True


def main():
    arguments = docopt.docopt(__doc__, help=True, version=__version__)
    # print(arguments)
    if arguments['--genConfig']:
        fileName = arguments['FILE']
        if fileName is None:
            fileName = 'config.yml'
        genConfig(fileName)
        return
    elif arguments['--delete']:
        os.system('rm -rf temp')
        return
    try:
        configFile = arguments['-c']
        if not os.path.exists(configFile):
            raise FileNotFoundError('配置文件{}不存在！'.format(configFile))
        config = Config(configFile, arguments)

        if not os.path.exists(config.source):
            raise FileNotFoundError('源文件{}不存在！'.format(config.source))

        is_silent = arguments['--silent']

        judger = Judge(config)
        if not printResult(getLanguage(config.source),
                           judger.judge(), is_silent):
            return 1

        if not is_silent and judger.runner.firstWA is not None:
            print('你在第{}个测试点出错了，\ndiff信息在diff_log中'.format(
                judger.runner.firstWA))
            print('=' * 70)
    except FileNotFoundError as e:
        print('错误：' + str(e))
        return 1


if __name__ == '__main__':
    exit(main())
