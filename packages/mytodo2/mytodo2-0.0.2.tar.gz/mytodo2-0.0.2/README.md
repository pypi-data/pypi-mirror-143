## 质量考试题库

## 正式编译打包发布项目
### 编译
python3 setup.py build
### 打包
python3 setup.py sdist bdist_wheel
### 上传
python3 -m twine upload dist/*

### 本地编译
1. py_modules 只能指定一个文件
2. packages 配置包地址,默认不包含包的子包
3. 打包模块给别人安装

```
python3 setup.py build
python setup.py sdist
dist/mypk1-1.0.zip
解压后使用
python setup.py install即可
```

### 开发调试

发布模块到本地环境

在项目根目录下,
```
python setup.py install
```

这样，系统会编译启动命令道script,但是lib指向的是本地开发代码

## 开发

在根目录下执行 python3 package2/test3.py
不要在package2里面直接执行test3.py这样会报依赖找不到
可以指定PYTHONPATH为E:\wk\myproj\mypython4,再执行
