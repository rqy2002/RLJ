# -*- coding=utf-8 -*-
" The Compiler and Judger of rlj "
import os
import psutil
import subprocess
import time
from .languages import getLanguage


class JudgeStatus(object):
    ''' Info of a judge.  '''
    def __init__(self, status, time_used=None,
                 memory_used=None, returncode=None):
        self.status = status
        self.time_used = time_used
        self.memory_used = memory_used
        self.returncode = returncode

    def __str__(self):
        return 'JudgeStatus({}, {}, {}, {})'.format(
            self.status, self.time_used, self.memory_used, self.returncode)

    def __repr__(self):
        return 'JudgeStatus({}, {}, {}, {})'.format(
            self.status, self.time_used, self.memory_used, self.returncode)

    def __eq__(self, other):
        return self.status == other.status


class Compiler(object):
    ''' The compiler of RLJ.  '''
    def __init__(self, config):
        self.source = config.source
        self.parameter = config.compiling_parameter
        if os.path.exists('temp'):
            os.system('rm -rf temp')
        try:
            os.mkdir('temp')
        except FileExistsError:
            os.system('rm -rf temp')

    def compile(self):
        extension = os.path.splitext(self.source)[1]
        temp_file = 'temp/temp{ext}'.format(ext=extension)
        compile_time_out = 'timeout 10s '
        os.system('cp {file} {temp}'.format(file=self.source, temp=temp_file))
        lang = getLanguage(self.source)

        compile_command = lang['compile_command']\
            + '>{null} 2> temp/compile.log'

        begin_time = time.time()
        complier_returncode = os.system(
            compile_time_out + compile_command.format(
                null=os.devnull, para=self.parameter, file=temp_file))
        time_used = time.time() - begin_time

        # os.system('rm -f {temp}'.format(temp=temp_file))

        if complier_returncode != 0:
            return (False, time_used)
        else:
            command = lang['run_command'].format(
                para=self.parameter, file=temp_file)

            return (True, time_used, command)


class Runner(object):
    ''' The program runner and checker of RLJ.  '''
    def __init__(self, config):
        self.datas = config.datas
        self.time = config.time_limit
        self.memory = config.memory_limit
        self.firstWA = None

    def _judge(self, task, data, prog):
        input_file = data[0]
        try:
            Input = open(input_file, 'r')
            Output = open('temp/temp.out', 'w')
            Err = open('temp/stderr', 'w')
            begin_time = time.time()
            max_memory = 0
            time_used = 0
            child = subprocess.Popen(prog.split(), stdin=Input,
                                     stdout=Output, stderr=Err)
            ps = psutil.Process(child.pid)
            while child.poll() is None:
                try:
                    tmp_mem_info = ps.memory_full_info()
                except:
                    break
                else:
                    mem_info = tmp_mem_info
                memory = float(mem_info.uss) / 1048576
                time_used = int((time.time() - begin_time) * 1000)
                max_memory = max(max_memory, memory)
                if memory > self.memory:
                    child.kill()
                    return JudgeStatus('MLE', time_used, max_memory)
                if time_used > self.time:
                    child.kill()
                    return JudgeStatus('TLE', time_used, max_memory)
            child.poll()
            returncode = child.returncode
        finally:
            Input.close()
            Output.close()
            Err.close()

        if returncode != 0:
            return JudgeStatus('RE', time_used, max_memory, returncode)

        diff_result = os.system(
            'diff -Z temp/temp.out {} >> temp/diff_log{}'.format(
                data[1], task))

        if diff_result == 0:
            os.system('rm -f temp/diff_log{}'.format(task))
            return JudgeStatus('AC', time_used, max_memory, 0)

        else:
            if self.firstWA is None:
                os.system('cp temp/diff_log{} diff_log'.format(task))
                self.firstWA = task
            return JudgeStatus('WA', time_used, max_memory, 0)

    def run(self, prog):
        self.firstWA = None
        task = 0
        for data in self.datas:
            task += 1
            yield (task, data, self._judge(task, data, prog))
        return


class Judge(object):
    ''' The judge of rlj. '''
    def __init__(self, config):
        self.config = config
        self.runner = Runner(config)
        self.compiler = Compiler(config)

    def compile(self):
        compile_status = self.compiler.compile()
        return compile_status

    def judge(self):
        compile_status = self.compile()
        if not compile_status[0]:
            if compile_status[1] >= 9:
                yield ('CTLE', '编译超时')
            else:
                yield ('ERROR', '编译错误')
            os.system('cat temp/compile.log')
            return
        else:
            yield ('DONE', '编译成功', compile_status[1])
        for task in self.runner.run(compile_status[2]):
            yield task
        return
