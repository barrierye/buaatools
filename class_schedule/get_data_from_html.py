#-*- coding:utf8 -*-
# Copyright (c) 2019 barriery
# Python release: 3.7.4
"""
module docstring here: TODO
"""

import sys
import re
try:
    import class_schedule_pb2
    from google.protobuf import text_format
except ImportError:
    pass

def get_courses():
    ''' parse html text which from stdin to course list '''
    courses = []
    for line in sys.stdin:
        if '<head>' not in line:
            continue
        row_pattern = re.compile(r'<tr.*?/tr>')
        col_pattern = re.compile(r'<td.*?/td>')
        empty_pattern = re.compile(r'<td data-v-.{8}="">(<!---->)*</td>')
        course_pattern = re.compile(r'Course-name.*?([0-9])分.*?title="(.*?)".*?title="(.*?)".*?\[(\d*?)-(\d*?)周\](\d*?)-(\d*?)节</span></p><p data-v-.{8}="">(.*?)</p><p data')
        key = ['grade',
               'course_name',
               'teacher',
               'week_period_begin',
               'week_period_end',
               'class_period_begin',
               'class_period_end',
               'place']
        rows = row_pattern.findall(line)

        # Remove the first line(header)
        for row in rows[1:]:
            weekday = 0 # [1, 7]
            cols = col_pattern.findall(row)
            for col in cols:
                if '上午' in col or '下午' in col or '晚上' in col:
                    continue
                weekday += 1
                if empty_pattern.match(col):
                    continue
                course = course_pattern.findall(col)
                for item in course:
                    course_item = dict(zip(key, item))
                    course_item['weekday'] = str(weekday)
                    courses.append(course_item)
    return courses

def write_protobuf_file(courses, filename):
    ''' write protobuf file manually '''
    with open(filename, 'w') as file:
        for course in courses:
            file.write('course {\n')
            file.write('    name: "%s"\n' % course['course_name'])
            file.write('    week_period_begin: %s\n' % course['week_period_begin'])
            file.write('    week_period_end: %s\n' % course['week_period_end'])
            file.write('    class_period_begin: %s\n' % course['class_period_begin'])
            file.write('    class_period_end: %s\n' % course['class_period_end'])
            file.write('    weekday: %s\n' % course['weekday'])
            file.write('    grade: %s\n' % course['grade'])
            file.write('    teacher: "%s"\n' % course['teacher'])
            file.write('    place: "%s"\n' % course['place'])
            file.write('}\n')

def gen_protobuf_file(courses, filename):
    ''' generate protobuf file by protobuf-API'''
    course_list_proto = class_schedule_pb2.CourseList()
    for course in courses:
        course_proto = course_list_proto.course.add()
        course_proto.grade = int(course['grade'])
        course_proto.name = course['course_name']
        course_proto.teacher = course['teacher']
        course_proto.week_period_begin = int(course['week_period_begin'])
        course_proto.week_period_end = int(course['week_period_end'])
        course_proto.class_period_begin = int(course['class_period_begin'])
        course_proto.class_period_end = int(course['class_period_end'])
        course_proto.place = course['place']
        course_proto.weekday = int(course['weekday'])
    with open(filename, 'w') as file:
        # human-firendly: https://stackoverflow.com/questions/33557965/print-human-friendly-protobuf-message
        file.write(text_format.MessageToString(course_list_proto))

def write_directly(courses):
    ''' write data file directly '''
    print(str(courses))

if __name__ == '__main__':
    COURSES = get_courses()
    # use protobuf
    #  gen_protobuf_file(COURSES, './class_schedule.data')
    #  write_protobuf_file(COURSES, './class_schedule.data')
    write_directly(COURSES)
