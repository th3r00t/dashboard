from dataclasses import dataclass

@dataclass
class Geometry:
    """
    The Geometry class holds all terminal measurements.
    """
    total_height: int
    total_width: int
    two_pane_width: int
    top_row_height: int = 1
    spacer_height: int = 1
    task_row_height: int = 0
    required_width : int = 120

    def __init__(self, stdscr) -> None:
        """
        Initializes the Geometry object based on the stdscr input.

        :param stdscr: curses stdscr object.
        :type stdscr: curses._CursesWindow
        :returns: None
        """
        self.total_height, self.total_width = stdscr.getmaxyx()
        self.two_pane_width = self.total_width // 2
        self.task_row_height = self.total_height - (
            self.top_row_height + self.spacer_height
        )

    def col_width(self, num_columns: int = 0, area: int = 0) -> int:
        """Defaults to single column width if num_columns is 0
        if area is 0 uses total screen width.

        :param num_columns: Desired number of columns
        :type num_columns: int
        :param area: Total area to compute against
        :type area: int
        :returns: int"""
        if area == 0:
            return self.total_width // num_columns
        else:
            return area // num_columns

    def bottom_row_height(self) -> int:
        """
        This method is not effective as it will not calculate the area of the articles list
        """
        return self.total_height - self.top_row_height - self.spacer_height
