from aenum import Enum
from datetime import date
from uuid import uuid4


class Status(Enum):
    NOT_STARTED = 0,
    IN_PROGRESS = 1,
    COMPLETED = 2


class Priority(Enum):
    LOW = 0,
    MEDIUM = 1,
    HIGH = 2,


class Item():
    __create_date = date.today()
    __title = "empty"
    __status = Status.NOT_STARTED
    __priority = Priority.LOW
    __flag = False
    __url = ''
    __due_date = date
    __state = False
    __notes = ""

    def __init__(self, title: str = None):
        if title is not None:
            self.__title = title
            self.__id = str(uuid4())

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value

    @property
    def priority(self):
        return self.__priority

    @priority.setter
    def priority(self, value):
        self.__priority = value

    @property
    def create_date(self):
        return self.__create_date

    @create_date.setter
    def create_date(self, value):
        self.__create_date = value

    @property
    def age(self):
        return self.__create_date - date.today()

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value: bool):
        self.__state = value

    @property
    def notes(self):
        return self.__notes

    @notes.setter
    def notes(self, value: str):
        self.__value = value


class Todo():
    __todos = []

    def __init__(self):
        print("New todo list has created")
        self._current = -1

    def __iter__(self):
        return self

    def __next__(self):
        if self._current < len(self.__todos) - 1:
            self._current += 1
            print(self.__todos[self._current].title)
            return self.__todos[self._current]
        else:
            self._current = -1
        raise StopIteration

    def __len__(self):
        return len(self.__todos)

    def new_item(self, item: Item):
        self.__todos.append(item)

    @property
    def items(self) -> list:
        return self.__todos

    def show(self):
        print('*' * 79)
        for item in self.__todos:
            print(item.title, item.status, item.priority, item.age)

    def remove_item(self, uuid: str = None, title: str = None) -> bool:
        if title is None and uuid is None:
            print(
                "You need to provide some details for me to remote it, either UUID or title")
        if uuid is None and title:
            for item in self.__todos:
                if item.title == title:
                    self.__todos.remove(item)
                    return True
            print("Item with title", title, 'not found')
            return False
        if uuid:
            self.__todos.remove(uuid)
            return True
