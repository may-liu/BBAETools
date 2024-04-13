# BBAETools

本工具只是给BBAE做对账单导出用的。目前没有考虑其他用途，也没有做过深度的检查和校验，
给需要的人提供一些帮助，如果你并不知道这是什么请勿使用，谢谢。

## 用法
超级简单：
#### part 1: 
准备python环境，各个包版本见requirements.txt, 内容略。
#### part 2: 
直接运行： python .\statement.py --file-path=xxx/*.pdf 即可，如果pdf文件就在当前目录，可以不加参数。
#### part 3: 
最终的文件名为：oprations.csv, 生成到当前工作目录下。