#!/usr/bin/env python3
# -*- coding=utf-8 -*-
'''_Rqy's local judge.

Usage:
  rlj -h | --help | --version
  rlj [-s | --silent] [-j Source] [-c Config] [--O2]
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

import os
import docopt
from .constants import __version__
from .judge import Judge
from .config import Config, makeConfig, genConfig
from .output import printResult

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
        config = makeConfig(configFile, arguments)

        if not os.path.exists(config.source):
            raise FileNotFoundError('源文件{}不存在！'.format(config.source))

        judger = Judge(config)

        if not printResult(config, judger.judge()):
            return 1

        if not config.silent and judger.runner.firstWA is not None:
            print('你在第{}个测试点出错了，\ndiff信息在diff_log中'.format(
                judger.runner.firstWA))
    except FileNotFoundError as e:
        print('错误：' + str(e))
        return 1


if __name__ == '__main__':
    exit(main())
