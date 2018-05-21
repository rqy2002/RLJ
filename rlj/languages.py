# -*- coding=utf-8 -*-
" Languages which rlj supports "
import os


class LanguageUnsupported(Exception):
    def __init__(self, arg):
        Exception.__init__(self, 'Unsupported language "{}"'.format(arg))


languages = [
    {
        'name': 'C',
        'extensions': ['c'],
        'compile_command': 'gcc {para} {file} -o temp/prog',
        'run_command': 'temp/prog'
    },
    {
        'name': 'C#',
        'extensions': ['cs'],
        'compile_command': 'mcs {para} /out:temp/prog {file}',
        'run_command': 'mono temp/prog'
    },
    {
        'name': 'C++',
        'extensions': ['cpp', 'cc', 'cxx'],
        'compile_command': 'g++ {para} {file} -o temp/prog',
        'run_command': 'temp/prog'
    },
    {
        'name': 'Go',
        'extensions': ['go'],
        'compile_command': 'go build {para} -o temp/prog {file}',
        'run_command': 'temp/prog'
    },
    {
        'name': 'Haskell',
        'extensions': ['hs', 'lhs'],
        'compile_command': 'ghc {para} {file} -o temp/prog',
        'run_command': 'temp/prog'
    },
    {
        'name': 'Java',
        'extensions': ['java'],
        'compile_command':
            'rm -rf temp && mkdir temp && cp {file} temp/prog.java && javac {para} temp/prog.java -d temp/',
        'run_command': 'java -cp temp/ prog'
    },
    {
        'name': 'Kotlin',
        'extensions': ['kt'],
        'compile_command':
            'kotlinc {para} {file} -include-runtime -d temp/prog.jar',
        'run_command': 'java -jar temp/prog.jar'
    },
    {
        'name': 'NodeJS',
        'extensions': ['js'],
        'compile_method': 'node -c {file}',
        'run_command': 'node {file}'
    },
    {
        'name': 'OCaml',
        'extensions': ['ml', 'mli'],
        'compile_command': 'ocamlc {para} {file} -o temp/prog',
        'run_command': 'temp/prog'
    },
    {
        'name': 'Python',
        'extensions': ['py'],
        'compile_command': 'python3 {para} -m py_compile {file}',
        'run_command': 'python3 temp/__pycache__/*.pyc'
    },
    {
        'name': 'Ruby',
        'extensions': ['rb'],
        'compile_command': 'ruby -c {file}',
        'run_command': 'ruby {file}'
    },
    {
        'name': 'Scala',
        'extensions': ['scala'],
        'compile_command':
            'rm -rf temp && mkdir temp && cp {file} temp/prog.scala && scalac {para} temp/prog.scala -d temp/',
        'run_command': 'scala -cp temp/ prog'
    },
    {
        'name': 'Visual Basic',
        'extensions': ['vb'],
        'compile_command': 'vbnc {para} /out:temp/prog {file}',
        'run_command': 'mono temp/prog'
    }
]


def getLanguage(source):
    extension = os.path.splitext(source)[1][1:]
    for lang in languages:
        if extension in lang['extensions']:
            return lang
    raise LanguageUnsupported(extension)
