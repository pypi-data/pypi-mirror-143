## mypk1

测试项目

## 打包安装上传流程

### 安装相关工具

```shell
## 打包工具
python -m pip install --upgrade setuptools wheel
## 打包工具2
python -m pip install --upgrade build
## 上传工具twine
python -m pip install --upgrade twine
```

### 准备工作

到https://test.pypi.org/simple/和 https://pypi.org/project注册相关账号，并将token分别保存到`~/.pypirc`



### 测试环境

1. 编译打包方式一 这里打两种包sdist打包为tar.gz,bdist_wheel打包为whl
   `python setup.py sdist bdist_wheel`
2. 编译打包方式二 也是打包为两个包，作用一样
   `python -m build`
3. 使用本地包安装
   `python -m pip install ./dist/mypk1-0.0.3.tar.gz`
4. twine上传
   `python -m twine upload --repository testpypi dist/*`
5. 从远程安装
   `pip install -i https://test.pypi.org/simple/ mypk1`
   `pip install -i https://test.pypi.org/simple/ mypk1==0.0.1`
   `pip install -i https://test.pypi.org/simple/ mypk1==0.0.2`
6. 升级安装
   `pip install --upgrade -i https://test.pypi.org/simple/ mypk1`
7. 卸载
   `pip uninstall mypk1`

### 正式环境

1. 上传
   `python -m twine upload --repository pypi dist/*`
2. 安装
   `pip install -i https://pypi.org/project mypk1`





