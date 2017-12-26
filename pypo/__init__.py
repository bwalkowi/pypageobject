from functools import partial
from ._page_objects import (PageObject, Button as ButtonPageObject,
                            NamedButton as NamedButtonPageObject)
from ._page_elements import (AbstractPageElement, Element, Label, Input)


Button = partial(Element, cls=ButtonPageObject)
NamedButton = partial(Element, cls=NamedButtonPageObject)
