# RLJ

一个便捷的本地评测器。By \_rqy & Margatroid.

![屏幕截图](https://raw.githubusercontent.com/rqy1458814497/RLJ/master/screenshoots/1.jpg)
![屏幕截图](https://raw.githubusercontent.com/rqy1458814497/RLJ/master/screenshoots/2.jpg)
![屏幕截图](https://raw.githubusercontent.com/rqy1458814497/RLJ/master/screenshoots/3.jpg)


## 安装

可以通过 ``pip3`` 安装。 **注：目前pip3落后更新**

```bash
 $ pip3 install --upgrade rlj
```

或者通过 ``git``

```bash
 $ git clone git@github.com:rqy1458814497/RLJ.git
 $ cd RLJ
 $ sudo python3 setup.py install
```


## 使用

### Config文件

创建 ``config.json`` 文件，该文件应包含以下几项：

``Source`` （可选）， ``Input`` ， ``Output`` ， ``#`` ， ``Time Limit`` ， ``Memory Limit``

例如：

```json
 {
   "Source"       : "example.cpp",
   "Input"        : "example#.in",
   "Output"       : "example#.ans",
   "#"            : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
   "Time Limit"   : 1000,
   "Memory Limit" : 128
 }
```

更简单的方法是输入

```bash
 $ rlj --genConfig [FILE]
```

生成 ``config.json`` （或指定FILE参数以更改文件名）。

### 数据

请将所需的输入输出数据文件置于 ``data`` 文件夹下。

如，上面的测试文件的例子中， ``data`` 下应有： ``example1.in``, ``example1.ans``, ``example2.in`` 等文件。


### 评测

```bash
 $ rlj [-s|--slient] [-j Source | --judge Source] [-c ConfigFile] [--O2]
```

只调用 ``rlj`` 即可评测。

若要简化其输出，请调用 ``rlj --silent`` 或 ``rlj -s``

具体用法请参照 ``rlj -h``

### 编译选项

默认无任何编译选项。

可通过在 ``config.json`` 中加入 ``Compiling Parameter`` 添加编译选项。

``--O2`` 可以在运行时制定，参照上文。

