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
        self.Source = config['Source']
        self.parameter = config.get('Compiling Parameter', '')
        if os.path.exists('temp'):
            os.system('rm -rf temp')
        try:
            os.mkdir('temp')
        except FileExistsError:
            os.system('rm -rf temp')

    def compile(self):
        extension = os.path.splitext(self.Source)[1]
        temp_file = 'temp/temp{ext}'.format(ext=extension)
        compile_time_out = 'timeout 10s '
        os.system('cp {file} {temp}'.format(file=self.Source, temp=temp_file))
        lang = getLanguage(self.Source)

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
        self.Input = config['Input']
        self.Output = config['Output']
        self.Time = config['Time Limit']
        self.Memory = config['Memory Limit']
        self.Num = config['#']
        self.firstWA = None

    def _judge(self, tesk, prog):
        tesk = str(tesk)
        input_file = tesk.join(self.Input.split('#'))
        try:
            Input = open('data/' + input_file, 'r')
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
                if memory > self.Memory:
                    child.kill()
                    return JudgeStatus('MLE', time_used, max_memory)
                if time_used > self.Time:
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
            'diff -Z temp/temp.out data/{} >> temp/diff_log{}'.format(
                tesk.join(self.Output.split('#')), tesk))

        if diff_result == 0:
            os.system('rm -f temp/diff_log{}'.format(tesk))
            return JudgeStatus('AC', time_used, max_memory, 0)

        else:
            if self.firstWA is None:
                os.system('cp temp/diff_log{} diff_log'.format(tesk))
                self.firstWA = tesk
            return JudgeStatus('WA', time_used, max_memory, 0)

    def run(self, prog):
        self.firstWA = None
        for tesk in self.Num:
            yield (tesk, self._judge(tesk, prog))
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
        for tesk in self.runner.run(compile_status[2]):
            yield tesk
        return
