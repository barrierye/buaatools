#-*- coding:utf8 -*-
# Copyright (c) 2019 barriery
# Python release: 3.7.4
"""
module docstring here: TODO
"""

import datetime
import sys
import pytz
from uuid import uuid1
from icalendar import Calendar, Event
try:
    import class_schedule_pb2
    from google.protobuf import text_format
except ImportError:
    pass

CLASS_PERIOD_BEGIN_TIME = [(0, 0), (8, 0), (8, 50), \
                           (9, 50), (10, 40), (11, 30), \
                           (14, 00), (14, 50), (15, 50), \
                           (16, 40), (17, 30), (19, 0), \
                           (19, 50), (20, 40), (21, 30)]

def get_data_from_directly_writen(filename):
    ''' get data from directly writen file '''
    course_list = eval(sys.stdin.read())
    return course_list

def get_data_from_protobuf(filename):
    ''' get data from protobuf '''
    course_list = class_schedule_pb2.CourseList()
    with open(filename, 'r') as file:
        text_format.Parse(file.read(), course_list)
    return course_list.course

def gen_ics_file(courses, filename):
    ''' generate iCalendar file '''
    cal = Calendar()
    cal.add('prodid', '-//barriery Inc//BUAA Class Schedule//CN')
    cal.add('version', '2.0')
    for course in courses:
        events = get_events_by_course(course)
        for event in events:
            cal.add_component(event)
    with open(filename, 'wb') as file:
        file.write(cal.to_ical())

def get_events_by_course(course):
    ''' get events by course '''
    if isinstance(course, dict):
        week_period_begin = int(course['week_period_begin'])
        week_period_end = int(course['week_period_end'])
        weekday = int(course['weekday'])
        class_period_begin = int(course['class_period_begin'])
        class_period_end = int(course['class_period_end'])
        name = course['course_name']
        place = course['place']
        teacher = course['teacher']
        grade = course['grade']
    elif isinstance(course, class_schedule_pb2.Course):
        week_period_begin = course.week_period_begin
        week_period_end = course.week_period_end
        weekday = course.weekday
        class_period_begin = course.class_period_begin
        class_period_end = course.class_period_end
        name = course.name
        place = course.place
        teacher = course.teacher
        grade = course.grade
    else:
        print('error type')
        exit(1)

    begin_date = datetime.datetime(2019, 8, 26, 0, 0, 0, tzinfo=pytz.timezone("Asia/Shanghai")) # zero week is 2019/8/26 00:00:00
    current_day = begin_date + datetime.timedelta(days=7*week_period_begin+weekday-1)
    events = []
    for class_period in range(class_period_begin, class_period_end+1):
        hour, minute = CLASS_PERIOD_BEGIN_TIME[class_period]
        current_date = current_day \
                          + datetime.timedelta(hours=hour) \
                          + datetime.timedelta(minutes=minute)
        event = Event()
        event.add('uid', str(uuid1()) + '@barriery')
        event.add('summary', name)
        event.add('dtstart', current_date)
        event.add('dtend', current_date + datetime.timedelta(minutes=45))
        event.add('dtstamp', datetime.datetime.now())
        event.add('location', place)
        event.add('description', 'teacher: ' + teacher + ', grade: ' + grade)
        event.add('rrule', {
            'freq': 'weekly',
            'interval': 1,
            'count': week_period_end - week_period_begin + 1})
        events.append(event)
    return events

if __name__ == '__main__':
    # use protobuf
    #  COURSES = get_data_from_protobuf('./class_schedule.data')
    COURSES = get_data_from_directly_writen('./class_schedule.data')
    gen_ics_file(COURSES, './class_schedule.ics')
