#!/usr/bin/env python3
#-*- coding=utf-8 -*-
'''_Rqy's local judge.

Usage:
  rlj -h | --help | --version
  rlj [-s] [-j Source] [-c Config] [--O2]
  rlj --genConfig [FILE]

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
'''

__author__  = '_rqy'
__version__ = '1.0.2'
__license__ = 'MIT Linsence'
from . import judge
import colorama
import os
import json
import sys
import docopt


def addColor(color, text):
	return getattr(colorama.Fore, color) + text + colorama.Fore.RESET

def printResult(result, silent=False):
	statusColor = {
			'AC' : 'GREEN',
			'WA' : 'RED',
			'TLE' : 'YELLOW',
			'MLE' : 'BLUE',
			'RE' : 'CYAN'
			}
	if silent:
		num = {'AC': 0, 'WA': 0, 'TLE': 0, 'MLE': 0, 'RE': 0}
		for tesk in result:
			st = tesk[1].status
			print(addColor(statusColor[st], st[0]), end='')
			num[st] += 1
			sys.stdout.flush()
		print()
		for st in statusColor:
			if not num[st]: continue
			print(addColor(statusColor[st], st[0] + ':%d' % num[st]), end = ' ')
		print()
	else:
		print('=' * 30)
		print('测试点\t状态\t内存\t时间')
		print('=' * 30)
		for tesk in result:
			s = str(tesk[0]) + '\t'
			st = tesk[1].status
			s += addColor(statusColor[st], st) + '\t'
			s += str(int(tesk[1].memory_used)) + 'MB' + '\t'
			s += ('%.3f' % (tesk[1].time_used / 1000)) + 's' + '\t'
			print(s)
		print('=' * 30)

def checkIOFiles(config):
	Input = config['Input']
	Output = config['Output']
	for tesk in config['#']:
		inputName = str(tesk).join(Input.split('#'))
		outputName = str(tesk).join(Output.split('#'))
		if not os.path.exists('data/' + inputName):
			raise FileNotFoundError('输入文件{}不存在！'.format(inputName))
		if not os.path.exists('data/' + outputName):
			raise FileNotFoundError('输出文件{}不存在！'.format(outputName))

def genConfig(fileName):
	if os.path.exists(fileName):
		ans = input('文件{}已存在，是否要覆盖(Y/n)？'.format(fileName)).strip()
		while ans != '' and (len(ans) > 1 or ans not in 'YyNn'):
			ans = input('文件{}已存在，是否要覆盖(Y/n)？'.format(fileName)).strip()
		if ans == 'N' or ans == 'n':
			return

	name = input('题目名：').strip()
	while not name: name = input('请输入题目名：').strip()
	source = input('源文件名（默认为"{}"):'.format(name+'.cpp'))
	if not source: source = name + '.cpp'
	print('数据:')
	input_file = input('  输入文件（默认为"{}"）:'.format(name+'#.in'))
	if not input_file: input_file = name + '#.in'
	output_file = input('  输出文件（默认为"{}"）:'.format(name+'#.ans'))
	if not output_file: output_file = name + '#.ans'
	a, b = None, None
	while a is None or a > b:
		if a is not None:
			print('输入错误（可能你想输入{} {}）'.format(b, a))
			a = b = None
		try:
			num_str = input('  "#"的范围（默认为1 1）:')
			if not num_str: num_str = '1 1'
			a, b = map(int, num_str.split())
		except ValueError:
			pass
	num = range(a, b + 1)
	time_limit = input('  时间限制(ms)（默认为1000）:')
	if not time_limit: time_limit = '1000'
	memory_limit = input('  空间限制(MB)（默认为128）:')
	if not memory_limit: memory_limit = '128'
	with open(fileName, 'w') as f:
		f.writelines([
			'{\n',
			'  "Source"       : "{}",\n'.format(source),
			'  "Input"        : "{}",\n'.format(input_file),
			'  "Output"       : "{}",\n'.format(output_file),
			'  "#"            : {},\n'.format(list(num)),
			'  "Time Limit"   : {},\n'.format(time_limit),
			'  "Memory Limit" : {}\n'.format(memory_limit),
			'}\n',
			])

def main():
	arguments = docopt.docopt(__doc__, help=True, version=__version__)
	# print(arguments)
	if arguments['--genConfig']:
		fileName = arguments['FILE']
		if fileName is None: fileName = 'config.json'
		genConfig(fileName)
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
		checkIOFiles(config)
		compiler = judge.Compiler(config)
		is_silent = arguments['--silent']
		if not is_silent:
			print('=' * 30)
			print('正在编译...')
		compile_status = compiler.compile(source=arguments['--judge'])
		if not compile_status[0]:
			print(addColor('RED', '编译失败'))
			exit(1)
		elif not is_silent:
			print(addColor('GREEN', '编译成功，用时{0:.3f}秒'.format(compile_status[1])))

		judger = judge.Judge(config)
		printResult(judger.judge(), is_silent)

		if not is_silent and judger.firstWA is not None:
			print('你在第{}个测试点出错了，\ndiff信息在diff_log中'.format(
				judger.firstWA))
			print('=' * 30)
	except FileNotFoundError as e:
		print('错误：' + str(e))
		exit(1)

if __name__ == '__main__':
	main()
