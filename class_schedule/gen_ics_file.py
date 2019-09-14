#-*- coding:utf8 -*-
# Copyright (c) 2019 barriery
# Python release: 3.7.4

import datetime
from uuid import uuid1
import pytz
from icalendar import Calendar, Event
import config
import login
import request_credit

CLASS_PERIOD_BEGIN_TIME = [(0, 0), (8, 0), (8, 50), \
                           (9, 50), (10, 40), (11, 30), \
                           (14, 00), (14, 50), (15, 50), \
                           (16, 40), (17, 30), (19, 0), \
                           (19, 50), (20, 40), (21, 30)]

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
    week_period_begin = int(course['week_period_begin'])
    week_period_end = int(course['week_period_end'])
    weekday = int(course['weekday'])
    class_period_begin = int(course['class_period_begin'])
    class_period_end = int(course['class_period_end'])
    name = course['course_name']
    place = course['place']
    teacher = course['teacher']
    credit = course['credit']
    course_id = course['course_id']

    # zero week is 2019/8/26 00:00:00
    begin_date = datetime.datetime(2019, 8, 26, 0, 0, 0, tzinfo=pytz.timezone("Asia/Shanghai"))
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
        event.add('description', 'teacher: %s, credit: %s, id: %s'%(teacher, credit, course_id))
        event.add('rrule', {
            'freq': 'weekly',
            'interval': 1,
            'count': week_period_end - week_period_begin + 1})
        events.append(event)
    return events

if __name__ == '__main__':
    COURSE_LIST = login.login_and_get_html(username=config.USERNAME,
                                           password=config.PASSWORD,
                                           xh=config.XH)
    request_credit.request_credit(student_type=config.STUDENT_TYPE,
                                  global_request_credit_dict=config.REQUEST_CREDIT,
                                  course_list=COURSE_LIST)
    gen_ics_file(COURSE_LIST, './class_schedule.ics')
