# Class Schedule

通过模拟登录[BUAA研究生选课页面课程](http://gsmis.buaa.edu.cn/)，生成.ICS课表文件，并列出剩余学分要求。

ICS文件是标准日历格式文件，可以被导入到Google calendar，iCal，以及其他一些主流日历应用。

![Google icalendar效果](https://tva1.sinaimg.cn/large/006y8mN6ly1g6ziz237c8j31fx0u042n.jpg)

![剩余学分](https://tva1.sinaimg.cn/large/006y8mN6ly1g70g42snv1j30ym0he405.jpg)

## 环境要求

- Python3
- requests (`pip install requests`) 
- icalendar (`pip install icalender`)
- 校园网环境

## 如何使用

1. 修改`config.example.py`文件，并将新文件命名为`config.py`。`config.py`中参数含义如下：

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

2. 运行`gen_ics_file.py`文件，文件夹内将生成.ICS文件`class_schedule.ics`

3. 将`class_schedule.ics`文件导入到所需的日历应用中：

   - Google calendar

     ![Google calendar](https://tva1.sinaimg.cn/large/006y8mN6ly1g6zizxwh2aj31720lqq39.jpg)

   - 其他日历应用

## 需要注意什么

- Windows下列出剩余学分要求的Log无法修改颜色，建议在Linux或macOS下使用以获得更好的体验。