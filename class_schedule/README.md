# Class Schedule

解析[BUAA研究生选课页面课程](http://gsmis.buaa.edu.cn/)，生成.ICS文件。

ICS文件是标准日历格式文件，可以被导入到Google calendar，iCal，以及其他一些主流日历应用。

![Google icalendar效果](https://tva1.sinaimg.cn/large/006y8mN6ly1g6ziz237c8j31fx0u042n.jpg)

![iCal效果](https://tva1.sinaimg.cn/large/006y8mN6ly1g6zizdqj1cj31dt0u0432.jpg)



## Need

- Python3
- icalendar (`pip install icalender`)

## Usage

1. 修改`config.example.py`文件，并将新文件命名为`config.py`

2. 运行下列命令，文件夹内将生成.ICS文件`class_schedule.ics`

   ```bash
   python gen_ics_file.py
   ```

5. 将`class_schedule.ics`文件导入到所需的日历应用中：

   - Google calendar
   
     ![Google calendar](https://tva1.sinaimg.cn/large/006y8mN6ly1g6zizxwh2aj31720lqq39.jpg)
   
   - iCal
   
     ![iCal](https://tva1.sinaimg.cn/large/006y8mN6ly1g6zj05tx4dj30ho0bq40d.jpg)
     
   - 其他日历应用
   

