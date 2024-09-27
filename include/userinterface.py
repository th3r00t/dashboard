import curses
from enum import Enum
from .geometry import Geometry
from .dashboard import Dashboard
from .objects import WindowType, State
from .derror import *
from .systeminfo import SystemInfo
from .tasks import Task

class UserInterface:
    def __init__(self, stdscr) -> None:
        self.stdscr = stdscr
        self.geometry = Geometry(stdscr)
        self.dash = Dashboard()
        self.article_count = 0
        self.task_start_row = None
        self.hline = curses.ACS_HLINE
        self.vline = curses.ACS_VLINE
        self.state = State(active_window = WindowType.TOP_BAR, cursor_position = [0,0])

    def center_pos(self, msg, width = None):
        if width is None:
            _avail_columns = self.geometry.total_width
        else:
            _avail_columns = width
        _msg_len = len(msg)
        return ((_avail_columns * .5) - (_msg_len * .5))

    def print_section_header(self, msg, width = None):
        _spacer = ""
        for _ in range(self.center_pos(msg, width).__int__()):
            _spacer = _spacer + " "
        return f"{_spacer}{msg}"

    def draw_error(self, e: Enum):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, self.print_section_header("<== Dashboard: Error ==>"), curses.A_BOLD)
        if e.value.severity is Severity.CRITICAL:
            format = curses.color_pair(1)
        elif e.value.severity is Severity.ERROR:
            format = curses.color_pair(2)
        elif e.value.severity is Severity.WARNING:
            format = curses.color_pair(3)
        elif e.value.severity is Severity.INFO:
            format = curses.A_ITALIC
        else:
            format = curses.A_STANDOUT
        self.stdscr.addstr(1, 0, self.print_section_header(f"** {e.value.code}: {e.value.message} **" if e is not None else f"Panic"), format)
        self.stdscr.addstr(self.geometry.total_height - 1, 1, "Press 'q' to exit.", curses.A_BOLD)
        self.stdscr.refresh()

    def render(self, article = 0):
        if self.geometry.total_height >= 40 and self.geometry.total_width >= 120:
            remaining_rows = self.draw_top_bar()
            self.article_count = remaining_rows - 10
            self.task_start_row = (self.geometry.total_height - remaining_rows) + self.article_count
            self.dash.articles(self.article_count)
            self.draw_article_list(0)
            self.draw_task_list()
            if self.geometry.total_width >= 150:
                self.read_article(article)
            else:
               self.keybinds() 
                # - [ ] Breaking due to keybind and flow control in read_article. $id{c4c337ac-d3de-48fe-b3c8-56011429a6b9}
        else:
            self.draw_error(e = DError.SCREENWIDTH)
            while True:
                key = self.stdscr.getch()
                if key == ord('q'):
                    break
            self.stdscr.clear()
            exit()

    def draw_top_bar(self) -> int:
        """Draws Main Menu Bar aka top_bar
            :param: items [wx, updates, news_headline]
        """
        wx, updates, sysinfo = self.dash.weather(), f"Updates: {self.dash.updates()}", SystemInfo()
        cpu_modelname = sysinfo.cpu['modelname']
        cpu_cores = sysinfo.cpu['cpucores']
        cpu_MHz = int(float(sysinfo.cpu["cpuMHz"]))
        cpu_str = f"{cpu_cores} Core {cpu_modelname} @ {cpu_MHz} MHz"
        menu_btn_str = f"[F1] Menu"
        self.stdscr.addstr(0, 0, menu_btn_str, curses.color_pair(3))
        self.stdscr.addstr(0, (self.geometry.total_width - len(wx) + 1 - len(updates) - len(cpu_str) - 10), cpu_str, curses.color_pair(1))
        self.stdscr.addstr(0, (self.geometry.total_width - len(wx) + 1 - len(updates) - 5), updates)
        self.stdscr.addstr(0, (self.geometry.total_width - len(wx)), wx)
        # Print Separator
        self.stdscr.hline(self.geometry.top_row_height, 0, self.hline, self.geometry.total_width, curses.A_BOLD)
        self.stdscr.refresh()
        # Determine how many rows are left in the current terminal
        remaining_rows = (self.geometry.total_height - (self.geometry.top_row_height + self.geometry.spacer_height)) 
        return remaining_rows

    def draw_task_list(self):
        task = Task()
        if task.installed:
            self.stdscr.hline(self.task_start_row, 0, self.hline, self.geometry.two_pane_width)
            self.stdscr.addstr(self.task_start_row + 1, 0, self.print_section_header("Active Tasks", self.geometry.two_pane_width), curses.A_BOLD)
            pendingtasks = task.pending_tasks_list()
            for i, taskitem in enumerate(pendingtasks, start=2):
                self.stdscr.addstr(self.task_start_row + i, 0, taskitem, curses.A_BOLD)
            self.stdscr.refresh()

    def draw_article_list(self, active: int = 0):
        articles = self.dash.articles()
        for i in range((self.geometry.top_row_height + self.geometry.spacer_height), self.geometry.total_height):
            self.stdscr.move(i, self.geometry.two_pane_width)
            self.stdscr.clrtoeol()
        for i, article in enumerate(articles, start=0):
            article_snippet = article[:self.geometry.two_pane_width-5]
            if ((i + self.geometry.top_row_height + self.geometry.spacer_height) < self.geometry.total_height):
                if i != active:
                    self.stdscr.addstr(self.geometry.top_row_height + self.geometry.spacer_height + i, 0, article_snippet, curses.color_pair(2))
                else:
                    self.stdscr.addstr(self.geometry.top_row_height + self.geometry.spacer_height + i, 0, article_snippet, curses.color_pair(1))
        self.state.active_window = WindowType.ARTICLE_LIST
        self.state.cursor_position = self.stdscr.getyx()
        self.stdscr.refresh()

    def draw_menu(self):
        self.stdscr.clear()
        self.stdscr.addstr(1, 1, "Menu Opened! Press 'q' to exit this menu.", curses.A_BOLD)
        self.stdscr.refresh()
        while True:
            key = self.stdscr.getch()
            if key == ord('q'):
                break
        self.stdscr.clear()
        draw_ui(self.stdscr)

    def line_formater(self, line: str) -> str:
        if (len(line) > self.geometry.two_pane_width):
            line_split = ""
            while line:
                line_split += f"{line[0:self.geometry.two_pane_width]}\n"
                line = line[self.geometry.two_pane_width:]
            return line_split
        return line

    def read_article(self, number = 0):
        self.depth_counter = 0
        self.scroll_offset = 0
        self.article = self.dash.article_reader(number)
        while True:
            for i in range((self.geometry.top_row_height), self.geometry.total_height):
                self.stdscr.move(i, self.geometry.two_pane_width)
                self.stdscr.clrtoeol()

            for i, line in enumerate(self.article[self.scroll_offset:]):
                if i + self.geometry.top_row_height + self.geometry.spacer_height >= self.geometry.bottom_row_height():
                    break
                self.stdscr.addstr(self.geometry.top_row_height + self.geometry.spacer_height + i, self.geometry.two_pane_width, self.line_formater(line))

            self.stdscr.hline(self.geometry.top_row_height, 0, self.hline, self.geometry.total_width)
            self.stdscr.vline(self.geometry.top_row_height + self.geometry.spacer_height, self.geometry.two_pane_width -1, self.vline, self.geometry.bottom_row_height() - self.geometry.spacer_height)
            self.stdscr.refresh()
            self.state.active_window = WindowType.ARTICLE_READER
            self.state.cursor_position = self.stdscr.getyx()
            self.keybinds(number)

    def keybinds(self, number = 0):
        key = self.stdscr.getch()
        if key == curses.KEY_F1:
            self.draw_menu()
        if key == ord('q'):
            self.stdscr.clear()
            sys.exit()
        
        if self.state.active_window == WindowType.ARTICLE_READER or self.state.active_window == WindowType.ARTICLE_LIST:
            if self.state.active_window is WindowType.ARTICLE_READER:
                if key == curses.KEY_UP or key == ord('k') and self.scroll_offset > 0:
                    self.scroll_offset -= 1
                elif key == curses.KEY_DOWN or key == ord('j') and self.scroll_offset < len(self.article) - self.geometry.bottom_row_height() + self.geometry.spacer_height:
                    self.scroll_offset += 1  # Scroll down
                elif key == 14:
                    number = number + 1
                    self.depth_counter += 1
                    self.draw_article_list(number)
                    self.read_article(number)
                elif key == 16:
                    self.depth_counter -= 1
                    number = number - 1
                    self.draw_article_list(number)
                    self.read_article(number)
            if self.state.active_window is WindowType.ARTICLE_LIST:
                if key == curses.KEY_UP or key == ord('k') and self.scroll_offset > 0:
                    number = number + 1
                    self.depth_counter += 1
                    self.draw_article_list(number)
                    self.read_article(number)
                elif key == curses.KEY_DOWN or key == ord('j') and self.scroll_offset < len(self.article) - self.geometry.bottom_row_height() + self.geometry.spacer_height:
                    self.depth_counter -= 1
                    number = number - 1
                    self.draw_article_list(number)
                    self.read_article(number)
