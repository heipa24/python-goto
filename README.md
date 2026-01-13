**我没招了,最多只兼容到python3.10,因为3.11引用了[自适应解释器](https://docs.python.org/3/whatsnew/3.11.html#whatsnew311-pep659)**
# goto

A function decorator to use `goto` in Python.
Tested on Python 3.6 through 3.10.<br>
一个函数装饰器，可以在 Python 中使用“goto”。
在 Python 3.6 到 3.10 上进行了测试。


## Installation(安装)

```
pip install https://github.com/heipa24/python-goto/archive/refs/heads/master.zip
```

## Usage(使用)

```python
from goto import with_goto, label, goto

@with_goto
def main(i):
    label .start
    i=i+1
    if i < 5:
        print(f"{i}")
        goto .start
    print("完成循环")
main(0)
```
```
PS C:\Users\heipa>python 新建文本文档.py
1
2       
3       
4       
完成循环
```
## 注意:
1. 一段代码在结构上无法访问则会在编译时被优化掉包括label,所以if False:label .end不可行,但f=False,if f:label .end就可以
2. 在循环中跳入另一个循环非常容易出问题(跳转后还是使用上一个循环的上下文,break之类的操作也是应用在上一个循环),从循环中跳出也不是很稳定
3. 跳入循环和在同一个循环内跳转则正常许多(在循环代码块结束时检查条件,所以稳定的多)
## Implementation(实现说明)
`label .begin` and `goto .begin` are property access expressions that conform to Python syntax
Represents the start attributes of the acquired variables label and goto, respectively.
The Python interpreter is able to successfully parse the function and generate the following initial bytecode:<br>
label .begin与 goto .begin是符合 Python 语法的属性访问表达式
分别表示获取变量 label和 goto的 begin属性。
Python 解释器能够成功解析函数并生成以下初始字节码：

```
  5           0 LOAD_FAST                0 (start)
              2 STORE_FAST               2 (i)

  6           4 BUILD_LIST               0
              6 STORE_FAST               3 (result)

  8           8 LOAD_GLOBAL              0 (label)
             10 LOAD_ATTR                1 (begin)
             12 POP_TOP

  9          14 LOAD_FAST                2 (i)
             16 LOAD_FAST                1 (stop)
             18 COMPARE_OP               2 (==)
             20 POP_JUMP_IF_FALSE       28

 10          22 LOAD_GLOBAL              2 (goto)
             24 LOAD_ATTR                3 (end)
             26 POP_TOP

 12     >>   28 LOAD_FAST                3 (result)
             30 LOAD_METHOD              4 (append)
             32 LOAD_FAST                2 (i)
             34 CALL_METHOD              1
             36 POP_TOP

 13          38 LOAD_FAST                2 (i)
             40 LOAD_CONST               1 (1)
             42 INPLACE_ADD
             44 STORE_FAST               2 (i)

 14          46 LOAD_GLOBAL              2 (goto)
             48 LOAD_ATTR                1 (begin)
             50 POP_TOP

 16          52 LOAD_GLOBAL              0 (label)
             54 LOAD_ATTR                3 (end)
             56 POP_TOP

 17          58 LOAD_FAST                3 (result)
             60 RETURN_VALUE
```

The `with_goto` decorator then removes the respective bytecode that has been
generated for the attribute lookups of the `label` and `goto` variables, and
injects a `JUMP_ABSOLUTE` or `JUMP_RELATIVE` instruction for each `goto`:<br>
随后，with_goto装饰器会移除那些为访问 label和 goto属性而生成的字节码，
并为每个 goto语句注入相应的 JUMP_ABSOLUTE或 JUMP_RELATIVE跳转指令：
```
  5           0 LOAD_FAST                0 (start)
              2 STORE_FAST               2 (i)

  6           4 BUILD_LIST               0
              6 STORE_FAST               3 (result)

  8           8 NOP
             10 NOP
             12 NOP

  9     >>   14 LOAD_FAST                2 (i)
             16 LOAD_FAST                1 (stop)
             18 COMPARE_OP               2 (==)
             20 POP_JUMP_IF_FALSE       28

 10          22 JUMP_FORWARD            34 (to 58)
             24 NOP
             26 NOP

 12     >>   28 LOAD_FAST                3 (result)
             30 LOAD_METHOD              4 (append)
             32 LOAD_FAST                2 (i)
             34 CALL_METHOD              1
             36 POP_TOP

 13          38 LOAD_FAST                2 (i)
             40 LOAD_CONST               1 (1)
             42 INPLACE_ADD
             44 STORE_FAST               2 (i)

 14          46 JUMP_ABSOLUTE           14
             48 NOP
             50 NOP

 16          52 NOP
             54 NOP
             56 NOP

 17     >>   58 LOAD_FAST                3 (result)
             60 RETURN_VALUE
```

## Alternative implementation(替代实现)

The idea of `goto` in Python isn't new.
There is [another module](http://entrian.com/goto/) that has been released
as April Fool's joke in 2004. That implementation doesn't touch the bytecode,
but uses a trace function, similar to how debuggers are written.<br>
Python中的“goto”概念并不新鲜。
还有[另一个模块]（http://entrian.com/goto/）已经发布
作为2004年愚人节的笑话。该实现不涉及字节码，
但它使用追踪函数，类似于调试器的编写方式。

While this eliminates the need for a decorator, it comes with significant
runtime overhead and a more elaborate implementation. Modifying the bytecode,
on the other hand, is fairly simple and doesn't add overhead at function execution.<br>
虽然这消除了对装饰器的需要，但它具有重要的意义
运行时开销和更复杂的实现。修改字节码，
另一方面，它相当简单，并且不会增加函数的开销执行。