from enum import Enum
from itertools import islice
from typing import Optional, Type
from abc import ABC, abstractmethod

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from . import PageObject


class Selector(Enum):
    CSS = By.CSS_SELECTOR
    ID = By.ID
    NAME = By.NAME
    XPATH = By.XPATH
    LINK_TEXT = By.LINK_TEXT
    PARTIAL_LINK_TEXT = By.PARTIAL_LINK_TEXT
    TAG_NAME = By.TAG_NAME
    CLASS_NAME = By.CLASS_NAME

    def __repr__(self):
        return f'{type(self).__name__}.{self.name}'


class AbstractPageElement(ABC):
    def __init__(self, locator: str, *, selector: Selector = Selector.CSS):
        self.locator = locator
        self.selector = selector

    @abstractmethod
    def __get__(self, instance, owner):
        if instance is None:
            return self

        try:
            item = instance.find_element(self.selector.value, self.locator)
        except NoSuchElementException:
            raise RuntimeError(f'unable to find {self.name} in {instance}')
        else:
            return item

    def __set__(self, instance, value):
        raise AttributeError("can't set attribute")

    def __delete__(self, instance):
        raise AttributeError("can't delete attribute")

    def __set_name__(self, owner, name):
        self.name = name.replace('_', ' ').strip().upper()


class Label(AbstractPageElement):
    def __get__(self, instance, owner):
        if instance is None:
            return self

        return super().__get__(instance, owner).text


class Input(AbstractPageElement):
    def __get__(self, instance, owner):
        if instance is None:
            return self

        return super().__get__(instance, owner).get_attribute('value')

    def __set__(self, instance, val):
        input_box = super().__get__(instance, type(instance))
        input_box.clear()
        if val != '':
            # sometimes send_keys doesn't send all keys, so it is necessary
            # to try sending them several times
            for _ in range(10):
                input_box.send_keys(val)
                assert input_box.get_attribute('value') == val, \
                    f'entering "{val}" to {self.name} in {instance} failed'


class Element(AbstractPageElement):
    def __init__(self, *args, cls: Optional[Type[PageObject]] = None,
                 text: Optional[str] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.cls = cls
        self.text = text

    def __get__(self, instance, owner):
        if instance is None:
            return self

        if self.text is None:
            item = super().__get__(instance, owner)
        else:
            items = instance.find_elements(self.selector.value, self.locator)
            for item in items:
                if item.text.lower() == self.text.lower():
                    break
            else:
                raise RuntimeError(f'no {self.name} with "{self.text}" '
                                   f'text found in {instance}')

        if self.cls is not None:
            return self.cls(instance.driver, item, instance)
        else:
            return item


class Elements(Element):
    def __get__(self, instance, owner):
        if instance is None:
            return self

        items = instance.find_elements(self.selector.value, self.locator)
        if self.text is not None:
            items = [item for item in items if item.text.lower() == self.text]

        if self.cls is not None:
            return PageObjectsSequence(instance.driver, items, instance, self.cls)
        else:
            return items


class PageObjectsSequence:

    def __init__(self, driver, items, parent, cls):
        self.driver = driver
        self.items = items
        self.parent = parent
        self.cls = cls

    def __len__(self):
        return len(self.items)

    def __getitem__(self, sel):
        cls = type(self)
        if isinstance(sel, int):
            item = self.items[sel] if sel < len(self) else None
            if item:
                return self.cls(self.driver, item, self.parent)
            else:
                raise IndexError(f'Index out of range. Requested item at '
                                 f'{sel} while limit is {len(self)} in '
                                 f'{self.parent}')
        elif isinstance(sel, slice):
            return cls(self.driver, self.items[sel], self.parent, self.cls)
        else:
            raise TypeError(f'{cls.__name__} must be integers or slices')
