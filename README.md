# buaatools

提供BUAA校内事项的Python库和一些日常生活小工具。

目前利用`buaatools`可以实现：

- 通过学号获取选课信息，并生成课表日历文件
- 通过学号获取学生姓名
- 通过学号获取入学照片
- （在预选课阶段）通过学号列表获取选课意愿值
- （在预选课阶段）查询所有课程容量
- 根据培养方案检查学分情况

## Requirements

Python 3

## Installation

```bash
pip install wheel
python setup.py bdist_wheel
pip install dist/buaatools-0.0.2-py3-none-any.whl
```

## Usage

在`./examples`下存放一些简单的使用例子，具体用法请查看`./examples/README.md`：

```bash
$ tree examples
examples
├── README.md
├── check_request_credit.py
├── config.example.py
├── gen_calendar_file.py
├── get_all_student_willingness_value.py
├── get_name_by_xh.py
├── get_photo_by_xh.py
└── get_total_courses.py
```

- check_request_credit.py 根据培养方案检查学分情况（非当前学期的课程需要在配置文件中设置）
- config.example.py 配置文件
- gen_calendar_file.py 通过学号获取选课信息，并生成.ICS文件。可以导入到Google calendar，iCal以及其他一些主流日历应用。
- get_all_student_willingness_value.py （在预选课阶段）通过学号列表获取选课意愿值，并列出自己意愿值的在所选课中的排名。如果提供本系所有人的学号，在预选课阶段更合理地安排意愿值，程序会给出建议的意愿值。
- get_name_by_xh.py 通过学号获取姓名。
- get_photo_by_xh.py 通过学号获取入学照片。
- get_total_courses.py 获取本学期所有课程信息（查询课容量）。


## Disclaimer

使用该仓库脚本造成的信息安全问题，作者概不负责。