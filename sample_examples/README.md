# sample examples Readme

## config.example.py

按以下说明修改`config.example.py`文件，并将新文件命名为`config.py`。`config.py`中参数含义如下：

```python
# 统一认证账号用户名
USERNAME = 'barriery'
# 统一认证账号密码
PASSWORD = '***********'
# 学号
XH = 'SY1906***'

# 选课时期（目前只实现了预选课，挑选课阶段） ['preparatory', 'adjustment']
STAGE = 'adjustment'
# 是否显示课间休息
CLASSBREAK  = True
# （可选）学生类型，用于检查剩余学分要求。内置'软件工程（硕士）', '计算机科学与技术（硕士）', '计算机技术（全日制专硕）'三种培养方案。
STUDENT_TYPE = '软件工程（硕士）'
# 培养方案设置。可以按照所给的三种培养方案自行添加，各个类目可以嵌套，必须包含'total'字段表示该类目所需的最低学分要求
REQUEST_CREDIT = {...}
```

## gen_calendar_file.py

1. 修改`config.example.py`文件

1. 运行`gen_ics_file.py`文件，文件夹内将生成.ICS文件`curriculum.ics`

2. 将`class_schedule.ics`文件导入到所需的日历应用中：

   - Google calendar

     ![Google calendar](https://tva1.sinaimg.cn/large/006y8mN6ly1g6zizxwh2aj31720lqq39.jpg)

   - 其他日历应用

