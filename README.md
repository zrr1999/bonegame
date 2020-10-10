# PyTex

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)![Upload Python Package](https://github.com/zrr1999/PyTex/workflows/Upload%20Python%20Package/badge.svg)

本代码库基于OpenCV实现了若干小游戏，主要目的是完成人工智能概论课程的大作业。

## 背景

...

## 优势
- LaTex
    1. 本辅助库可以有效避免拼写错误，漏加空格等低级错误。
    2. 本辅助库可以借助Python提供更多的功能。
    3. 本辅助库在插入图片、生成表格等方面有巨大优势。
- Word
    1. 本辅助库可以更加自由地编写文档。
    2. 本辅助库可以借助Python提供更多的功能。


## 安装[![Downloads](https://pepy.tech/badge/bone-games)](https://pepy.tech/project/bone-games)

这个项目使用 [Python](https://www.python.org/downloads/) 开发，请确保你本地安装了它。

建议使用pip安装本库。

```sh
$ pip install bone-games
```

## 使用说明

使用时，您可以创建一个文档实例。

```python
from pytex import MathDocument
```

如果你使用了默认的标准页，可以通过命令添加队伍信息

```python
board = Board(7, 7)
players = [Player(f"p{i}", i, f"p{i}") for i in range(1, 3)]

game = Game(board, players)
```

你可以将md文档转换为latex

```python
from pytex.utils import md2tex, MarkDown
latex_code1 = md2tex(path="examples/md/abstract.md")
latex_code2 = md2tex(file=open("examples/md/abstract.md", 'r', encoding='UTF-8'))
latex_code3 = MarkDown("md/abstract.md")
```

你可以在文档中添加标题、摘要、目录。

```python
doc.add_title()
keys = ["出租车资源配置", "供求匹配模型", "缓解程度判断模型", "分区域动态实时补贴方案"]
doc.add_abstract(latex_code, keys)
doc.add_toc()
```

你可以在文档中添加 使用固定格式编写的md文档 作为一个section。

```python
doc.add_section(path="examples/md/wtcs.md")
```

你可以在文档中添加指定标题和内容的 section。

```python
doc.add_section(title="符号说明", content="大家好啊")
```

你可以在文档中添加变量，将会自动添加到变量表中，同时还可以使用符号转化器将其转换为latex代码

```python
from pytex.utils import SymbolTransformer
from pylatex import NoEscape
x = doc.add_var("x", NoEscape("这是一个优秀的$x$"))
st = SymbolTransformer()
formula, name = st.sym2tex((x**2+7)*5)
```

最后，你可以生成tex文档，或者pdf文档

```python
doc.generate_pdf('resources/math', compiler='XeLatex', clean_tex=False, clean=False)
```

## 特色功能
## 更新日志
- (2020.10.10) v0.1.0 发布
    - 实现了五子棋并提供了接口允许开发者进行扩展。

## 维护者

[@詹荣瑞](https://github.com/tczrr1999)

## 如何贡献

非常欢迎你的加入！[提一个 Issue](https://github.com/tczrr1999/bonegame/issues/new) 或者提交一个 Pull Request。

### 贡献者

感谢以下参与项目的人：

## 使用许可

禁止将本辅助库及衍生品上传到百度网盘。
[GNU](LICENSE) © Rongrui Zhan