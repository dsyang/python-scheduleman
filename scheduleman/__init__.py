#!/usr/bin/env python
#
# Copyright 2010, 2011 Dan Yang
#
# This file is part of python-scheduleman.
#
# python-scheduleman is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# python-scheduleman is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with python-scheduleman.  If not, see <http://www.gnu.org/licenses/>.

import urllib2 as urllib
import string
import re

"""
ScheduleMan ICS class:
Create an instance of the ScheduleMan class in order to parse a schedule
from a URL.

Note, create an instance in this manner:

schedule = ScheduleMan(url)

where url is the string representation of a fully-qualified URL (http:// and
all, folks).

"""
class ScheduleMan(object):
    def __init__(self, url=None):
        self.url=url
        self.classes = []
        self.semester = None
        strip_chars = ' \t\n\r\0\x0B\"'
        if self.url is not None:
            u = urllib.urlopen(url+ '.ics')
            
            #parsing keywords
            class_code = 'SUMMARY:'
            class_name = 'DESCRIPTION:'
            class_endclass = 'END:VEVENT'
            sem_check = 'RRULE:FREQ=WEEKLY'
            bad_recs = ('Lec')
            
            for ln in u.readlines():
                if(ln.startswith(class_code)):
                    summary = ln[len(class_code):].strip(strip_chars).replace('-','') #gives XXXXX Lec 3, XXXXX A/B/C/D etc..
                    rec = summary[6:] #the Lec 3, A/B/C/D part
                    code = summary[:5] # the XXXXX part
                    
                elif(ln.startswith(class_name)):
                    name = ln[len(class_name):].strip(strip_chars) #gives Introduction to Mathematical Software
                    
                elif(ln.startswith(sem_check)):
                    if(self.semester == None):
                        temp1 = ln[ln.find('UNTIL='):] #gives a time statement like UNTIL=_20110429_T235959;WKST=SU spring would be 201104, fall: 201112
                        if(temp1[10] == '0'): #10 is the point right after 2011
                            self.semester = 'S'
                        else:
                            self.semester = 'F'
                        self.semester += temp1[6:10]
                        
                elif(ln.startswith(class_endclass)):
                    if(not re.match('Lec', rec)): #not a lecture time...
                        self.classes.append({
                            'number': code,
                            'name': name,
                            'recitation': rec
                        })

        else:
            dom = None
    
    """
    ScheduleMan.get_url(self):
    Get URL used to generate this schedule
    """
    def get_url(self):
        return self.url    
        
        
    """
    ScheduleMan.get_semester(self):
    Get semester that schedule pertains to
    """
    def get_semester(self):
        return self.semester
    
    
    """
    ScheduleMan.get_schedule(self):
    Get list of dictionaries, one for each class, with following format:
        name: name of class
        number: class number
        recitation: recitation letter
    """        
    def get_schedule(self):
        return self.classes

    """
    ScheduleMan.get_numbers(self):
    Get list of class numbers in this schedule
    """
    def get_numbers(self):
        if self.classes:
            return [cls.get('number') for cls in self.classes]
        return []
        
        
    """
    ScheduleMan.get_class(self, number):
    Get dictionary for the class with the number given as `number`
    """
    def get_class(self, number):
        for cls in self.classes:
            if cls.get('number') == number:
                return cls
        return {}
    
    """
    ScheduleMan.get_name(self, number):
    Get verbose name of class with given number
    """
    def get_name(self, number):
        return self.get_class(number).get('name')
    
    """
    ScheduleMan.get_recitation(self, number):
    Get recitation of class with given number
    """
    def get_recitation(self, number):
        return self.get_class(number).get('recitation')
    
    """
    ScheduleMan.prettify(self):
    Get human-readable schedule string
    """
    def prettify(self):
        return '\n'.join([cls.get('number') +' ' + cls.get('recitation') + ' - ' + 
                           cls.get('name') for cls in self.get_schedule()])
    
def main(url):
    sch = ScheduleMan(url)
    print sch.get_semester()
    print sch.prettify()
    print "from", sch.get_url()

if __name__ == '__main__':
    url = "https://scheduleman.org/schedules/bsYn6rDO1Z"
    url = raw_input( "Schedulman URL:")
    main(url)
