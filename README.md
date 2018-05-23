# RLJ

[![Build Status](https://travis-ci.org/rqy1458814497/RLJ.svg?branch=master)](https://travis-ci.org/rqy1458814497/RLJ)

一个便捷的本地评测器，具有**实验性**跨平台功能。By \_rqy & Margatroid.

*若您遇到问题，请提出issue.*

[屏幕截图](https://github.com/rqy1458814497/RLJ/blob/master/screenshoots)

## 安装

可以通过 ``pip3`` 安装。

**不要忘记sudo!!!**

```bash
 $ sudo pip3 install --upgrade rlj
```

或者通过 ``git`` 。***Note:*** 如果您以此方式安装，请自行安装依赖 (docopt, colorama, psutil, pyyaml).

```bash
 $ git clone git@github.com:rqy1458814497/RLJ.git
 $ cd RLJ
 $ sudo python3 setup.py install
```
### Windows用户

如果您是Windows用户，请您安装`git-bash`

## 使用

### Config文件

创建 ``config.yml`` 文件，该文件应包含以下几项：

``Source`` （可选）， ``Input Data`` ， ``Output Data`` ， ``Time Limit`` ， ``Memory Limit``

例如：

```yaml
Source: example.cpp
Input Data: example(\d*)\.in
Output Data: example(\d*)\.ans
Time Limit: 1000
Memory Limit: 128
```

其中 ``Input Data/Output Data`` 项使用正则表达式匹配，要求两项中group（即用圆括号括起来的）个数相同。若某个输入与某个输出数据中每个group对应相同，则其会被匹配。注意：``(?:``开头的组不会被考虑在内。

如果您不知道什么叫正则表达式，没关系，您只需要

```yaml
Input Data: xxx(\d*)\.in
Output Data: xxx(\d*)\.out
```

就可以做到评测所有``xxx1.in/xxx1.out``或``xxx123.in/xxx123.out``项。

更简单的方法是输入

```bash
 $ rlj --genConfig [FILE]
```

生成 ``config.yml`` （或指定FILE参数以更改文件名）。

### 数据

请将所需的输入输出数据文件置于 ``data`` 文件夹下。

如，上面的测试文件的例子中， ``data`` 下应有： ``example1.in``, ``example1.ans``, ``example2.in`` 等文件。

也可在 ``config.yml`` 内制定 ``Data Dir`` 项更改数据存放位置。如

```yaml
Data Dir: ./
```

表示数据文件存放于当前文件夹下。


### 评测

```bash
 $ rlj [-s|--slient] [-j Source | --judge Source] [-c ConfigFile] [--O2]
```

只调用 ``rlj`` 即可评测。

若要简化其输出，请调用 ``rlj --silent`` 或 ``rlj -s``

具体用法请参照 ``rlj -h``

### 编译选项

默认无任何编译选项。

可通过在 ``config.ymp`` 中加入 ``Compiling Parameter`` 项添加编译选项。

``--O2`` 可以在运行时制定，参照上文。

## TODO

- [x] Make a todo list.
- [ ] Special Judge Supporting.
- [x] Input/Answer file name auto matching.
- [ ] Press ^C to exit directly (instead of get **one** RE).
- [ ] Find more *TODO*.
