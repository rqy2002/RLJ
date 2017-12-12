---
RLJ
---

一个便捷的本地评测器。By _rqy.

.. class:: no-web

    .. image:: https://raw.githubusercontent.com/rqy1458814497/RLJ/master/screenshoots/1.gif
        :alt: HTTPie compared to cURL
        :width: 100%
        :align: centerk

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
   "Time Limit"   : 1000,
   "Memory Limit" : 128
 }

更简单的方法是输入

.. code-block:: bash

 $ rlj --genConfig [FILE]

生成 ``config.json`` （或指定FILE参数以更改文件名）。

数据
----

请将所需的输入输出数据文件置于 ``data`` 文件夹下。

如，上面的测试文件的例子中， ``data`` 下应有： ``example1.in``, ``example1.ans``, ``example2.in`` 等文件。


评测
----

.. code-block:: bash

 $ rlj [-s|--slient] [-j Source | --judge Source] [-c ConfigFile]

只调用 ``rlj`` 即可评测。

若要简化其输出，请调用 ``rlj --silent`` 或 ``rlj -s``

具体用法请参照 ``rlj -h``


