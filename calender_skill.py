from ics import Calendar, Event
from pathlib import Path
import os
import yaml
from datetime import datetime
from dateutil.relativedelta import *
import pytz
from yaml import loader

calendar_filename = 'myfile.ics'
calendar_datafile = 'myfile.yml'


class CalenderSkill():
    c = Calendar()

    def add_event(self, begin: str, name: str, description: str = None) -> bool:
        ''' adds an event to the calendar '''
        e = Event()
        e.name = name
        e.begin = begin
        e.description = description
        try:
            self.c.events.add(e)
            return True
        except:
            print("there was a problem adding the event, sorry.")
            return False

    def remove_event(self, event_name: str):
        ''' Removes the event from the calendar '''
        # find the event
        for event in self.c.events:
            if event.name == event_name:
                # found it
                self.c.events.remove(event)
                print("removing event:", event_name)
                return True

        # not found
        print("Sorry Could not find that event:", event_name)
        return False

    def parse_to_dict(self):
        dict = []
        for event in self.c.events:
            my_event = {}
            my_event['begin'] = event.begin.datetime
            my_event['name'] = event.name
            my_event['description'] = event.description
            dict.append(my_event)
            # print('parsing file:', yaml.dump(dict, default_flow_style=False))
        return dict

    def save(self):
        # Save the Calendar ICS file
        with open(calendar_filename, 'w') as my_file:
            my_file.writelines(self.c)
        # Save the YAML Data file

        # first check that there are some entries in the dictionary, otherwise remove the file
        if self.c.events == set():
            print("No Events - Removing YAML file")
            try:
                os.remove(calendar_datafile)
            except:
                print("oops couldn't delete the YAML file")
        else:
            with open(calendar_datafile, 'w') as outfile:

                yaml.dump(self.parse_to_dict(), outfile,
                          default_flow_style=False)

    def load(self):
        ''' load the Calendar data from the YAML file '''
        filename = calendar_datafile
        my_file = Path(filename)

        # check if the file exists
        if my_file.is_file():
            stream = open(filename, 'r')
            events_list = yaml.load(stream)
            for item in events_list:
                e = Event()
                e.begin = item['begin']
                e.description = item['description']
                e.name = item['name']
                self.c.events.add(e)
        else:
            # file doesnt exist
            print("file does not exist")

    def list_events(self, period: str = None) -> bool:
        ''' Lists the upcoming events 
            if `period` is left empty it will default to today
            other options are:
            `all` - lists all events in the calendar
            `this week` - lists all the events this week
            `this month` - lists all the events this month
        '''

        if period == None:
            period = "this week"

        # check that there are events
        if self.c.events == set():
            # no events found
            print("No Events In Calendar")
            return False
        else:
            event_list = []
            # have to fix the localisation - thats the +00 timezone bit on the date
            # otherwise it complains of non-naive date being compared with naive date
            now = pytz.utc.localize(datetime.now())
            if period == "this week":
                nextperiod = now+relativedelta(weeks=+1)
            if period == "this month":
                nextperiod = now+relativedelta(months=+1)
            if period == "all":
                nextperiod = now+relativedelta(years=+100)
            for event in self.c.events:
                event_date = event.begin.datetime
                if (event_date >= now) and (event_date <= nextperiod):
                    event_list.append(event)
            return event_list
