from contextlib import suppress


class PageObject:
    _id = None
    _click_area = None

    def __init__(self, driver, web_elem=None, parent=None):
        self.driver = driver
        self.web_elem = web_elem if web_elem is not None else driver
        self.parent = parent
        self._ignore_id = False

    def is_displayed(self):
        return self.web_elem.is_displayed()

    def click(self):
        click_area = self._click_area
        if click_area is None:
            click_area = self.web_elem

        is_enabled = (click_area.is_enabled() and
                      'disabled' not in click_area.get_attribute('class'))
        if is_enabled and click_area.is_displayed():
            click_area.click()
        else:
            raise RuntimeError(f'unable to click on {self}')

    def __str__(self):
        name = type(self).__name__
        parent_name = f' in {self.parent}' if self.parent is not None else ''

        if not self._ignore_id and self._id is not None:
            # in case when retrieving _id fails and recurse into __str__
            # omit this part as to not fall into infinite recursion
            self._ignore_id = True

            with suppress(RuntimeError):
                name = f'{self._id} {name}'

            self._ignore_id = False

        return name + parent_name


class Button(PageObject):
    def __call__(self):
        self.click()

    def is_enabled(self):
        return (self.web_elem.is_enabled() and
                'disabled' not in self.web_elem.get_attribute('class'))

    def is_active(self):
        return 'active' in self.web_elem.get_attribute('class')


class NamedButton(Button):

    @property
    def text(self):
        return self.web_elem.text

    _id = text
