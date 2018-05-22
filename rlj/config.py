import re
import yaml
import os
from os.path import join


class DataError(Exception):
    def __init__(self, arg):
        Exception.__init__(self, arg)


def showWarning(s):
    print('Warning: ' + s)


def matchData(rIn, rOut, data_dir):
    fileList = os.listdir(data_dir)
    # print(fileList, rIn, rOut)
    inData = {}
    outData = {}
    for name in fileList:
        res1 = rIn.fullmatch(name)
        res2 = rOut.fullmatch(name)
        if res1 and res2:
            raise DataError('文件"{}"同时匹配输入/输出文件格式'.format(name))
        elif res1:
            g = res1.groups()
            if g in inData:
                raise DataError(
                    '文件"{}"与"{}"匹配输入文件格式的groups相同（都为{}）'
                    .format(name, inData[g]))
            else:
                inData[g] = name
        elif res2:
            g = res2.groups()
            if g in outData:
                raise DataError(
                    '文件"{}"与"{}"匹配输出文件格式的groups相同（都为{}）'
                    .format(name, outData[g]))
            else:
                outData[g] = name

    # print(inData, outData)
    res = []
    for k in inData:
        if k not in outData:
            showWarning('没有输出文件与"{}"匹配（将被忽略）'.format(inData[k]))
        else:
            res.append((join(data_dir, inData[k]), join(data_dir, outData[k])))
    for k in outData:
        if k not in inData:
            showWarning('没有输入文件与"{}"匹配（将被忽略）'
                        .format(outData[k]))
    if not res:
        raise DataError('没有合法的输入输出文件')
    res.sort()
    return res


class Config(object):
    def __init__(self, config_file, argument):
        with open(config_file) as f:
            config = yaml.load(f.read())
        if argument['-j'] is not None:
            self.source = argument['-j']
        else:
            self.source = config['Source']
        data_dir = config.get('Data Dir', 'data/')
        rIn = re.compile(config.get('Input Data', '.*(\\d*)\\.in'))
        rOut = re.compile(config.get('Output Data', '.*(\\d*)\\.(?:out|ans)'))
        self.datas = matchData(rIn, rOut, data_dir)
        self.time_limit = config['Time Limit']
        self.memory_limit = config['Memory Limit']
        self.compiling_parameter = config.get('Compiling Parameter', '')
        self.silent = argument['--silent']
        if argument['--O2']:
            self.compiling_parameter = '-O2' + self.compiling_parameter


def genConfig(fileName):
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

    if os.path.exists(fileName):
        ans = input('文件{}已存在，是否要覆盖(Y/n)？'.format(fileName)).strip()
        while ans != '' and (len(ans) > 1 or ans not in 'YyNn'):
            ans = input(
                '文件{}已存在，是否要覆盖(Y/n)？'.format(fileName)).strip()
        if ans == 'N' or ans == 'n':
            return

    name = getArgument('题目名')
    source = getArgument('源文件名', (name + '.cpp'))
    print('数据:')
    input_file = getArgument('输入文件', name + '(\\d*)\\.in', 2)
    output_file = getArgument('输出文件', name + '(\\d*)\\.(?:ans|out)', 2)
    time_limit = getArgument('时间限制(ms)', '1000')
    memory_limit = getArgument('空间限制(MB)', '128')
    with open(fileName, 'w') as f:
        f.writelines([
            'Source: {}\n'.format(source),
            'Input Data: {}\n'.format(input_file),
            'Output Data: {}\n'.format(output_file),
            'Time Limit: {}\n'.format(time_limit),
            'Memory Limit: {}\n'.format(memory_limit),
            ])
