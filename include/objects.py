from typing import List
from dataclasses import dataclass
from enum import Enum

class WindowType(Enum):
    """Window Types

        Attributes:
            TOP_BAR (str): topbar
            ARTICLE_LIST (str): alist
            ARTICLE_READER (str): aread
            TASK (str): task

        Raises:
            ExceptionName: Condition that raises this exception.

        Examples:
            >>> WindowType.TOP_BAR
            topbar

    """
    TOP_BAR = "topbar"
    ARTICLE_LIST = "alist"
    ARTICLE_READER = "aread"
    TASK = "task"
    
@dataclass
class State:
    active_window: WindowType
    cursor_position: List[int]
