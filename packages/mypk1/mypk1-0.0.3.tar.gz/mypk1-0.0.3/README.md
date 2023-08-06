## mypk1

测试项目

### 常用脚本

``` shell
#上传
python -m twine upload --repository testpypi dist/*
```

## 打包安装上传流程

### 测试环境

1. 编译打包方式一 这里打两种包sdist打包为tar.gz,bdist_wheel打包为whl
   `python setup.py sdist bdist_wheel`
2. 编译打包方式二 也是打包为两个包，作用一样
   `python -m build`
3. 本地包
   `python -m pip install ./dist/mypk1-0.0.3.tar.gz`
4. twine上传
   `python -m twine upload --repository testpypi dist/*`
5. 远程安装
   `pip install -i https://test.pypi.org/simple/ mypk1`
   `pip install -i https://test.pypi.org/simple/ mypk1==0.0.1`
   `pip install -i https://test.pypi.org/simple/ mypk1==0.0.2`
6. 升级安装
   `pip install --upgrade --extra-index-url https://test.pypi.org/simple/ mypk1`
7. 卸载
   `pip uninstall mypk1`

### 正式环境





