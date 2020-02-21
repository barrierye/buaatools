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
# 是否校外访问
VPN = True

# 本学期第零周的开始日期
BEGIN_DATE = datetime.datetime(2020, 2, 17, 0, 0, 0, tzinfo=pytz.timezone("Asia/Shanghai"))
# 选课时期（预选课阶段，调选课阶段，结束选课阶段） ['preparatory', 'adjustment', 'ending']
STAGE = 'preparatory'
# 是否显示课间休息
CLASSBREAK  = True
# （可选，此项是为了学分检查）学生类型，用于检查剩余学分要求。内置'软件工程（硕士）', '计算机科学与技术（硕士）', '计算机技术（全日制专硕）'三种培养方案。
STUDENT_TYPE = '软件工程（硕士）'
# （可选，此项是为了学分检查）培养方案设置。可以按照所给的三种培养方案自行添加，各个类目可以嵌套，必须包含'total'字段表示该类目所需的最低学分要求
REQUEST_CREDIT = {...}
# （可选，此项是为了学分检查）已修学分
PREVIOUS_FINISHED_CREDIT_LIST = [...]
```

## check_request_credit.py

根据培养方案检查学分情况（非当前学期的课程需要在配置文件中设置）

1. 修改`config.example.py`文件

2. 运行`check_request_credit.py`文件：

   ![运行结果](https://tva1.sinaimg.cn/large/0082zybply1gbzmge6ji9j31b00osdkw.jpg)

## gen_calendar_file.py (线上试用: www.barriery.cn:5000)

 通过学号获取选课信息，并生成.ICS文件。可以导入到Google calendar，iCal以及其他一些主流日历应用。

1. 修改`config.example.py`文件

1. 运行`gen_calendar_file.py`文件，文件夹内将生成.ICS文件`curriculum.ics`

2. 将`schedule.ics`文件导入到所需的日历应用中：

   - Google calendar

     ![Google calendar](https://tva1.sinaimg.cn/large/006y8mN6ly1g6zizxwh2aj31720lqq39.jpg)

   - 其他日历应用

## get_all_student_willingness_value.py

在预选课阶段）通过学号列表获取选课意愿值，并列出自己意愿值的在所选课中的排名。如果提供本系所有人的学号，在预选课阶段更合理地安排意愿值，程序会根据课程容量给出建议的意愿值。

1. 修改`config.example.py`文件

2. 设定学号列表

3. 运行`get_all_student_willingness_value.py`文件：

   ![运行结果](https://tva1.sinaimg.cn/large/0082zybply1gbzkq1h4bxj31cs0u045v.jpg)

## get_name_by_xh.py

通过学号获取姓名。

1. 修改`config.example.py`文件

2. 运行`get_name_by_xh.py`文件

## get_photo_by_xh.py

通过学号获取入学照片。

1. 修改`config.example.py`文件

2. 运行`get_photo_by_xh.py`文件

## get_total_courses.py

获取本学期所有课程信息（查询课容量）。

1. 修改`config.example.py`文件

2. 运行`get_total_courses.py`文件

