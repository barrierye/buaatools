# buaatools

提供BUAA校内事项的Python库和一些日常生活小工具。

目前利用`buaatools`可以实现：

- 通过学号获取选课信息，并生成课表日历文件
- 在预选课阶段查询给定学号列表同学的选课意愿值

## Requirements

- Python 3
- pip
- Wheel

## Installation

```bash
python setup.py bdist_wheel
pip install dist/buaatools-0.0.1-py3-none-any.whl
```

## Usage

```python
from buaatools.spider import login

target = 'https://gsmis.e.buaa.edu.cn:443'
username = 'username'
password = 'password'
xh = 'SY1906123'
# 校外登陆校内网站
session = bylogin.login_with_vpn(target=target, username=username, password=password)
# 获取当前学号的选课信息
courses = bycourse.query_course_by_xh(stage='ending', xh=xh, session=session, vpn=True)
if courses:
    # 生成课程日历文件
    courses.gen_ics_file(classbreak=False, filename='curriculum.ics')
```

## Some sample examples

在`./sample_examples`下存放一些简单的使用例子，具体用法请查看`./sample_examples/README.md`：

```bash
$ tree sample_examples
sample_examples
├── README.md
├── config.example.py
├── gen_calendar_file.py
└── get_all_student_willingness_value.py
```

- config.example.py 配置文件
- gen_calendar_file.py 通过模拟登陆选课网站爬取课程信息，并生成.ICS文件，可以导入到Google calendar，iCal以及其他一些主流日历应用。

- get_all_student_willingness_value.py 获取所给学号列表的所有人预选课的意愿值，并列出自己意愿值的在所选课中的排名。


## Disclaimer

- 使用该仓库脚本时请务必遵循`网络安全法`。
- 使用该仓库脚本造成的信息安全问题，作者概不负责。