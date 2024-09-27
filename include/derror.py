from dataclasses import dataclass
from enum import Enum
from typing import Optional

class ErrorMsg(Enum):
    """Error Messages

        Attributes:
            SCREENWIDTH (str): "Screen width less than required size"
            INVALID_INPUT (str): ""

        Returns:
            str: The mapped Error message.
        Raises:
            ExceptionName: Condition that raises this exception.

        Examples:
            >>> ErrorMsg.SCREENWIDTH
            Screen width less than required size
    """
    SCREENWIDTH = "Screen width less than required size"
    INVALID_INPUT = "Invalid Input"

class Severity(Enum):
    INFO = "Info"
    WARNING = "Warning"
    ERROR = "Error"
    CRITICAL = "Critical"

@dataclass
class ErrorInfo:
    code: int
    message: str
    severity: Severity
    details: Optional[str] = None

class DError(Enum):
    SCREENWIDTH = ErrorInfo(1001, ErrorMsg.SCREENWIDTH.value, Severity.CRITICAL)
    INVALID_INPUT = ErrorInfo(1002, ErrorMsg.INVALID_INPUT.value, Severity.INFO)
