# -*- coding=utf-8 -*-
import os
import psutil
import subprocess
import time


class JudgeInfo(object):
    """
    Info of a judge.
    """
    def __init__(self, status, time_used=None,
                 memory_used=None, returncode=None):
        self.status = status
        self.time_used = time_used
        self.memory_used = memory_used
        self.returncode = returncode


class Compiler(object):
    """
    The compiler of RLJ.
    """
    def __init__(self, config):
        self.config = config
        if os.path.exists("temp"):
            for f in os.listdir("temp"):
                os.remove("temp/"+f)
        else:
            os.mkdir("temp")

    def compile(self, source=None):
        begin_time = time.time()
        compile_Parameter = self.config.get('Compiling Parameter', '')
        if source is None:
            source = self.config.get('Source')
            if source is None:
                raise FileNotFoundError(
                    '没有源文件！（请在config.json里设置源文件或执行时指定！）')
        compile_method = "g++ {file} {Para} -o temp/prog 2> temp/compile.log"
        command = compile_method.format(file=source, Para=compile_Parameter)
        if os.system(command):
            return (False, time.time() - begin_time)
        else:
            return (True, time.time() - begin_time)


class Judge(object):
    """
    The judge of RLJ.
    """
    def __init__(self, config):
        self.Input = config['Input']
        self.Output = config['Output']
        self.Time = config['Time Limit']
        self.Memory = config['Memory Limit']
        self.Num = config['#']
        self.firstWA = None

    def _judge(self, tesk):
        tesk = str(tesk)
        input_file = tesk.join(self.Input.split('#'))
        try:
            Input = open('data/' + input_file, 'r')
            Output = open('temp/temp.out', 'w')
            Err = open('temp/stderr', 'w')
            begin_time = time.time()
            max_memory = 0
            time_used = 0
            child = subprocess.Popen('temp/prog', stdin=Input,
                                     stdout=Output, stderr=Err)
            ps = psutil.Process(child.pid)
            while child.poll() is None:
                mem_info = ps.memory_full_info()
                memory = float(mem_info.uss) / 1048576
                time_used = int((time.time() - begin_time) * 1000)
                max_memory = max(max_memory, memory)
                if memory > self.Memory:
                    child.kill()
                    return JudgeInfo('MLE', time_used, max_memory)
                if time_used > self.Time:
                    child.kill()
                    return JudgeInfo('TLE', time_used, max_memory)
            child.poll()
            returncode = child.returncode
        finally:
            Input.close()
            Output.close()
            Err.close()

        if returncode != 0:
            return JudgeInfo('RE', time_used, max_memory, returncode)

        diff_result = os.system(
            'diff -Z temp/temp.out data/{} >> temp/diff_log{}'.format(
                tesk.join(self.Output.split('#')), tesk))

        if diff_result == 0:
            return JudgeInfo('AC', time_used, max_memory)

        else:
            if self.firstWA is None:
                os.system('cp temp/diff_log' + str(tesk) + ' diff_log')
                self.firstWA = tesk
            return JudgeInfo('WA', time_used, max_memory)

    def judge(self):
        self.firstWA = None
        for tesk in self.Num:
            yield (tesk, self._judge(tesk))
        return
