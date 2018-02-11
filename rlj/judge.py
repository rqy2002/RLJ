# -*- coding=utf-8 -*-
import os
import psutil
import subprocess
import time


class JudgeInfo(object):
    ''' Info of a judge.  '''
    def __init__(self, status, time_used=None,
                 memory_used=None, returncode=None):
        self.status = status
        self.time_used = time_used
        self.memory_used = memory_used
        self.returncode = returncode


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

        if extension in ['.py']:
            compile_method = 'python3 {para} -m py_compile {temp}\
                >{null} 2> temp/compile.log'
        elif extension in ['.js']:
            compile_method = 'node -c {temp}\
                >{null} 2> temp/compile.log'
        elif extension in ['.hs', '.lhs']:
            compile_method = 'ghc {para} {temp} -o temp/prog\
                >{null} 2> temp/compile.log'
        elif extension in ['.ml', '.mli']:
            compile_method = 'ocamlc {para} {temp} -o temp/prog\
                >{null} 2> temp/compile.log'
        elif extension in ['.go']:
            compile_method = 'go build {para} -o temp/prog {temp}\
                >{null} 2> temp/compile.log '
        elif extension in ['.rb']:
            compile_method = 'ruby -c {temp}\
                >{null} 2> temp/compile.log'
        elif extension in ['.vb']:
            compile_method = 'vbnc {para} /out:temp/prog {temp}\
                >{null} 2> temp/compile.log'
        elif extension in ['.kt']:
            compile_method = 'kotlinc {para} {temp} -include-runtime -d temp/prog.jar'
        elif extension in ['.cs']:
            compile_method = 'mcs {para} /out:temp/prog {temp}\
                >{null} 2> temp/compile.log'
        elif extension in ['.c']:
            compile_method = 'gcc {para} {temp} -fdiagnostics-color=always -o temp/prog\
                >{null} 2> temp/compile.log'
        else:  # elif extension in ['.cpp', '.cxx']:
            compile_method = 'g++ {para} {temp} -fdiagnostics-color=always -o temp/prog\
                >{null} 2> temp/compile.log'

        begin_time = time.time()
        complier_returncode = os.system(compile_time_out + compile_method.format(
            null=os.devnull, para=self.parameter, temp=temp_file))
        time_used = time.time() - begin_time

        # os.system('rm -f {temp}'.format(temp=temp_file))

        if complier_returncode != 0:
            return (False, time_used)
        else:
            command = 'temp/prog'

            if extension in ['.py']:
                pycache = 'temp/__pycache__'
                ll = os.listdir(pycache)
                command = 'python3 ' + pycache + '/' + ll[0]
            elif extension in ['.js']:
                command = 'node {file}'.format(file=temp_file)
            elif extension in ['.rb']:
                command = 'ruby {file}'.format(file=temp_file)
            elif extension in ['.cs', '.vb']:
                command = 'mono {file}'.format(file="temp/prog")
            elif extension in ['.kt']:
                command = 'java -jar {file}'.format(file="temp/prog.jar")

            return (True, time_used, command)


class Judge(object):
    ''' The judge of RLJ.  '''
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
            os.system('rm -f temp/diff_log{}'.format(tesk))
            return JudgeInfo('AC', time_used, max_memory)

        else:
            if self.firstWA is None:
                os.system('cp temp/diff_log{} diff_log'.format(tesk))
                self.firstWA = tesk
            return JudgeInfo('WA', time_used, max_memory)

    def judge(self, prog):
        self.firstWA = None
        for tesk in self.Num:
            yield (tesk, self._judge(tesk, prog))
        return
