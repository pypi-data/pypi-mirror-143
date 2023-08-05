# python 开发之前必须知道的一些事情


## Where is Python's sys.path initialized from?


https://stackoverflow.com/questions/897792/where-is-pythons-sys-path-initialized-from

## 了解一下 PEP 吧 Python Enhancement Proposals 

使用 setup.py develop 进行开发
会将当前包路径加到 sys.path 中，
有相同左右的有 requirement.txt 中添加一行 -e .
pip install .[xxx] 将使用 setup.py 中的 extras_require xxx键值对应的依赖

## setup 的参数设置
https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/
sample project about setup
https://github.com/pypa/sampleproject
为 PYPI 服务，https://pypi.org/

* name，不区分大小写，并且任意多的 _-. 看做是一个 .
* version，[schema](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#choosing-a-versioning-scheme) 查看 
* description
    * description
    * long_description
    * long_description_type
* url， homepage of project
* author='A. Random Developer',
    * author
    * author_email
* license
* classifiers，classifiers 列表提供项目的分类 https://pypi.org/classifiers/
* keywords='sample setuptools development'
* project_urls={
    'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
    'Funding': 'https://donate.pypi.org',
    'Say Thanks!': 'http://saythanks.io/to/example',
    'Source': 'https://github.com/pypa/sampleproject/',
    'Tracker': 'https://github.com/pypa/sampleproject/issues',
},
￼![avatar](./asset/Projectlinks.png)
* packages，使用 find_packages 定位到本项目的package
定位出一下的包 find_packages(where="src")
![avatar](./asset/find_packages.png)
￼
* py_modules=["",]， contains any single-file Python modules
* install_requires=['',’’] 每一项如同 requirements.txt 的一行，使用 pip install .  会使用该项安装依赖 ，[install_requires 和 requirements.txt 的区别](https://packaging.python.org/en/latest/discussions/install-requires-vs-requirements/#id6)  ('brosoul_data', glob('md/**/*', recursive=True)

* python_requires=''，运行的 python 版本要求
* package_data={
        # If any package contains *.txt or *.rst files, include them:  
        "": ["*.txt", "*.rst"],  
        # And include any *.msg files found in the "hello" package, too:  
        "hello": ["*.msg"],  
    }
* data_files=[('my_data', ['data/data_file'])] 'data_file' will be installed into '<sys.prefix>/my_data'，[递归写法](https://stackoverflow.com/questions/27829754/include-entire-directory-in-python-setup-py-data-files)
* entry_points={
    'console_scripts': [
        'pytest'='pytest:console_main',
    'py.test'='pytest:console_main'
    ], 
},  pytest 示例
* 





setup tools 和 disutils 中都有 setup()
setuptools是distutils的增强版。setuptools有一个entry_points功能很方便，类似linux启动某个服务，如在linux命令行里firefox能启动火狐浏览器。


### 打包项目
1. 首先安装 build。 python3 -m pip install build
2. 打包
    -  打包成 source Distribution，生成在 dist 下。 python3 -m build --sdist
    - python3 -m build --wheel
    -  run build without --wheel or --sdist，会有两种产物
3. 测试
3. 上传 twine upload dist/*

上传过程中使用 $HOME/.pypirc 下的账号信息
```bash
[pypi]
username = __token__
password = <the token value, including the `pypi-` prefix>
```