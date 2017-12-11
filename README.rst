---
RLJ
---

一个便捷的本地评测器。By _rqy.

.. contents::

.. section-numbering::

安装
====

可以通过 ``pip3`` 安装。

.. code-block:: bash

 $ pip3 install --upgrade https://github.com/rqy1458814497/RLJ/archive/master.tar.gz

或者通过 ``git``

.. code-block:: bash

 $ git clone git@github.com:rqy1458814497/RLJ.git
 $ cd RLJ
 $ sudo python3 setup.py install


使用
====

Config文件
----------

创建 ``config.json`` 文件，该文件应包含以下几项：

``Source`` （可选）， ``Input`` ， ``Output`` ， ``#`` ， ``Time Limit`` ， ``Memory Limit``

例如：

.. code-block:: json

 {
   "Source"       : "example.cpp",
   "Input"        : "example#.in",
   "Output"       : "example#.ans",
   "#"            : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
   "Time Limit"   : 1,
   "Memory Limit" : 128
 }

更简单的方法是输入

.. code-block:: bash

 $ rlj --genConfig

生成 ``config.json`` 。

评测
----

.. code-block:: bash

 $ rlj [-s|--slient] [-j Source | --judge Source] [-c Config]

只调用 ``rlj`` 即可评测。

具体用法请参照 ``rlj -h``


