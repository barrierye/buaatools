# BUAA-Tools

本仓库将存放BUAA的一些日常生活小工具。

## 免责声明

使用该仓库脚本时请务必遵循`网络安全法`。

使用该仓库脚本造成的信息安全问题，作者概不负责。

## 目录

```bash
.
├── README.md
├── config.example.py
├── course.README.md
├── course.gen_calendar_file.py
├── course.get_all_student_willingness_value.py
├── helper
│   ├── __init__.py
│   └── bylogger.py
└── spider
    ├── README.md
    ├── __init__.py
    ├── bycourse.py
    └── bylogin.py
```

- config.example.py 

  配置文件

- course.README.md

  course文件相关的README

- course.gen_calendar_file.py

  通过模拟登陆选课网站爬取课程信息，并生成.ICS文件，可以导入到Google calendar，iCal以及其他一些主流日历应用。

- course.get_all_student_willingness_value.py

  获取所给学号列表的所有人预选课的意愿值，并列出自己意愿值的在所选课中的排名。

- [spider](http://gitlab.act.buaa.edu.cn/yebw/buaa-tools/tree/master/spider) 校内网站模拟登陆工具

  > bylog.py
  
  提供登陆校内网站的API。目前只支持`http://gsmis.buaa.edu.cn/`
  
  > bycourse.py
  
  提供查询课程相关的API。目前只支持`查询预选课信息`以及`检查方案完成情况`。

## 环境要求

- Python3
- requests (`pip install requests`) 
- icalendar (`pip install icalender`)
- 校园网环境
