#!/usr/bin/env python
#
# Copyright 2010, 2011 Sri Raghavan
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

"""
Python client library for The Tartan's ScheduleMan service.

This client library is designed to allow read-only access and parsing of class 
schedules generated through the ScheduleMan service, in lieu of a true API.
"""
import urllib2 as urllib
from BeautifulSoup import BeautifulSoup
import re

"""
ScheduleMan class:
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
        
        if self.url is not None:
            u = urllib.urlopen(url)
            soup = BeautifulSoup(u)
            u.close()
            
            for cls in soup('li', id=re.compile('^course*')):
                code = cls.find('h3', 'number').contents[0].strip().replace('-', '')
                name = cls.find('h4', 'name').contents[0].strip()
                rec =  cls.find('span', 'selected_section').contents[0].strip()
                self.classes.append({
                    'number': code,
                    'name': name,
                    'recitation': rec,
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
    
def main():
    sch = ScheduleMan("https://scheduleman.org/schedules/bsYn6rDO1Z")
    print sch.prettify()
    print "from", sch.get_url()

if __name__ == '__main__':
    main()
