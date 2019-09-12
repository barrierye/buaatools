# Class Schedule

解析[BUAA研究生选课页面课程](http://gsmis.buaa.edu.cn/)，生成.ICS文件。

ICS文件是标准日历格式文件，可以被导入到Google calendar，iCal，以及其他一些主流日历应用。

![最终效果](https://tva1.sinaimg.cn/large/006y8mN6gy1g6ust9morsj31850u0qrs.jpg)



## Need

- Python3
- icalendar (pip install icalender)



## Usage

1. 登陆选课系统，打开已选课程页面，`command+s`手动保存页面

![手动保存页面](https://tva1.sinaimg.cn/large/006y8mN6ly1g6t7p79pkyj31760u0gpf.jpg)

2. 将保存好的html文件复制进项目文件夹并进入文件夹

   ```bash
   mv example.html BUAAClassSchedule/ && cd BUAAClassSchedule/
   ```

3. 解析html文件，生成.ICS文件`class_schedule.ics`

   ```bash
   cat example.html | python get_data_from_html.py | python gen_ics_file.py
   ```

5. 将`class_schedule.ics`文件导入到所需的日历应用中：

   - Google calendar
   
     ![Google calendar](https://tva1.sinaimg.cn/large/006y8mN6gy1g6uq3o0zckj316o0gwjrn.jpg)
   
   - iCal
   
     ![iCal](https://tva1.sinaimg.cn/large/006y8mN6gy1g6uq226cjuj30fo07aac8.jpg)
   
   
   





## TODO

模拟登陆保存html页面（期待一个好心人）



