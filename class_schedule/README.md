# Class Schedule

解析[BUAA研究生选课页面课程](http://gsmis.buaa.edu.cn/)，生成.ICS文件。

ICS文件是标准日历格式文件，可以被导入到Google calendar，iCal，以及其他一些主流日历应用。

![Google icalendar效果](https://tva1.sinaimg.cn/large/006y8mN6ly1g6x6dbgjb9j31bf0u0djx.jpg)

![iCal效果](https://tva1.sinaimg.cn/large/006y8mN6gy1g6ust9morsj31850u0qrs.jpg)



## Need

- Python3
- icalendar (使用`pip install icalender`命令安装

## Usage

1. 修改`CONFIG.example.py`文件，并将新文件命名为`CONFIG.py`

2. 运行下列命令，文件夹内将生成.ICS文件`class_schedule.ics`

   ```bash
   python gen_ics_file.py
   ```

5. 将`class_schedule.ics`文件导入到所需的日历应用中：

   - Google calendar
   
     ![Google calendar](https://tva1.sinaimg.cn/large/006y8mN6gy1g6uq3o0zckj316o0gwjrn.jpg)
   
   - iCal
   
     ![iCal](https://tva1.sinaimg.cn/large/006y8mN6gy1g6uq226cjuj30fo07aac8.jpg)
     
   - 其他日历应用
   
