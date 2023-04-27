import pyjokes
from datetime import datetime
from ai import AI
from todo import Todo, Item
from weather import Weather
from calender_skill import CalenderSkill
import dateparser


melody = AI()
todo = Todo()
calender = CalenderSkill()
calender.load()


# jokes
def joke():
    for_fun = pyjokes.get_jokes()
    print(for_fun)
    melody.say(for_fun)


# todos
def add_todo() -> bool:
    item = Item()
    melody.say('Tell me what to add')
    try:
        item.title = melody.listen()
        todo.new_item(item)
        message = "Added" + item.title
        melody.say(message)
        return True
    except:
        print("some thing went wrong")
        return False


def list_todos():
    if len(todo) > 0:
        melody.say("Here are your todos list")
        for item in todo:
            melody.say(item.title)
    else:
        melody.say('List is empty!')


def remove_todo() -> bool:
    melody.say('Which item to remove?')
    try:
        item_title = melody.listen()
        todo.remove_item(item_title)
        message = "Removed" + item_title
        melody.say(message)
        return True
    except:
        print("There is a error")
        return False


# weather
def weather():
    myweather = Weather()
    forecast = myweather.forecast
    print(forecast)
    melody.say(forecast)


# calendar
def add_event() -> bool:
    melody.say("What is the name of the event")
    try:
        event_name = melody.listen()
        melody.say("When is this event?")
        event_begin = melody.listen()
        event_isodate = dateparser.parse(
            event_begin).strftime("%Y-%m-%d %H:%M:%S")
        melody.say("What is the event description?")
        event_description = melody.listen()
        message = "Ok, adding event " + event_name
        print(message)
        melody.say(message)
        calender.add_event(begin=event_isodate, name=event_name,
                           description=event_description)
        calender.save()
        return True
    except:
        print("opps there was an error")
        return False


def remove_event() -> bool:
    melody.say("What is the name of the event you want to remove?")
    try:
        event_name = melody.listen()
        try:
            calender.remove_event(event_name=event_name)
            melody.say("Event removed successfully")
            calender.save()
            return True
        except:
            melody.say("Sorry I could not find the event", event_name)
            return False
    except:
        print("opps there was an error")
        return False


def list_events(period) -> bool:
    this_period = calender.list_events(period=period)
    if this_period is not None:
        message = "There "
        if len(this_period) > 1:
            message = message + 'are '
        else:
            message = message + 'is '
        message = message + str(len(this_period))
        if len(this_period) > 1:
            message = message + ' events'
        else:
            message = message + ' event'
        message = message + " in the diary"
        # print(message)
        melody.say(message)
        for event in this_period:
            event_date = event.begin.datetime
            weekday = datetime.strftime(event_date, "%A")
            day = str(event.begin.datetime.day)
            month = datetime.strftime(event_date, "%B")
            year = datetime.strftime(event_date, "%Y")
            time = datetime.strftime(event_date, "%I:%M %p")
            name = event.name
            description = event.description
            message = "On " + weekday + " " + day + \
                " of " + month + " " + year + " at " + time
            message = message + ", there is an event called " + name
            message = message + " with an event description of " + description
            print(message)
            melody.say(message)


command = ''
melody.say('Hello')
while True and command != "goodbye":
    try:
        command = melody.listen()
        command = command.lower()
    except:
        print('Sorry i dont get that!')
        command = ''

    print("Command was: ", command)

    # jokes
    if command == "tell me a joke":
        joke()
        command = ''

    # todos
    if command in ['add to do', "add item", "add todo"]:
        add_todo()
        command = ''
    if command in ["list todos", "list todo", "list to do"]:
        list_todos()
        command = ''
    if command in ['remove to do', "remove item", "mark done", "remove todos"]:
        remove_todo()

    # weather
    if command in ['what is the weather']:
        weather()

    # calender
    if command in ['add event', 'add to calendar', 'new event', 'add a new event']:
        add_event()
    if command in ['delete event', 'remove event', 'cancel event']:
        remove_event()
    if command in ['list events', "what's on this month", "what's coming up this month"]:
        list_events(period='this month')
    if command in ["what's on this week", "what's coming up this week", "what's happening"]:
        list_events(period='this week')
    if command in ['list all events']:
        list_events(period='all')

melody.say('I am go to bed now')
