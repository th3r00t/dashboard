import requests, shutil, subprocess
from .config import Config
from typing import List, Any, Dict

class Dashboard:
    """Main Dashboard object.

        Attributes:
            config (Config): Configuration object.
            term_size (tuple): [y, x].
            is_arch (bool): Is this Arch Linux?
            current_article (int): Article Id.
            refresh_rate (int): How often to refresh.
            wait_timer (int): How long to wait.
            browser (str): Which browser to scrape with.
            article_list (List): Main Article container.
        
        Methods:
            weather(): Gets wx info.
            updates(): Gets update count.
            top_story_ids(): Json of story top ids.
            articles(): List of article headers.
            os_info(): Dict of os related information scraped from /etc/os-release
            count_arch_updates(): Get the number of updates available via pacman
            article_reader(): List[str] Itterable representation of an Article

        Returns:
            Dashboard: A instantiated Dashboard object.

        Raises:
            ExceptionName: Condition that raises this exception.

        Examples:
            >>> dash = Dashboard()
            dash
    """
    def __init__(self):
        self.config: Config = Config()
        self.term_size: tuple = shutil.get_terminal_size()
        self.is_arch: bool = self.archlinux()
        # self.articles = self.get_news(50)
        self.current_article: int = 0
        self.refresh_rate: int = (60 * 10)
        self.wait_timer: int = 60
        self.browser: str = "lynx"
        self.article_list: List = []

    def weather(self) -> str:
        """Gets weather information from wttr.in
        it will get the location setting from the
        configuration file ~/.config/dashboard/config.ini

            Returns:
                str: Printable weather report.

            Raises:
                ExceptionName: Condition that raises this exception.

            Examples:
                >>> wx = Dashboard().weather()
                print(f"{wx}")

        """
        try:
            response = requests.get(f"https://wttr.in/{self.config.parser["Settings"]["wx_loc"]}", params={'format': '4'})
            if response.status_code == 200:
                weather = response.text
            else:
                weather = f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {e}"
        return weather

    def updates(self):
        if self.is_arch:
            return self.count_arch_updates()

    def top_story_ids(self) -> Any:
        """Get Json list of top story id's

            Returns:
                Any: Json.

            Raises:
                ExceptionName: Condition that raises this exception.

            Examples:
                >>> example_function_call()
                expected_output

        """
        return requests.get("https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty").json()

    def articles(self, number = 0, current = 0) -> List[str]:
        """Get the articles

            Args:
                number (int): Number of Articles to fetch.
                current (int): Current Article.

            Returns:
                List[str]: A List of Article headers.

            Raises:
                ExceptionName: Condition that raises this exception.

            Examples:
                >>> Dashboard().articles()
                ["1 Example Article Title 1", "2 Example Article Title 2", ". . ."]

        """
        if len(self.article_list) == 0:
            top_stories_ids = self.top_story_ids()
            stories = []
            if number == 0:
                number = len(self.article_list)
            for i in range(number):
                story_id = top_stories_ids[i]
                story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty"
                story_data = requests.get(story_url).json()
                url = story_data.get('url', 'No URL')
                # _avail_columns = self.term_size.columns - len(url) - 10
                _avail_columns = self.term_size.columns - len(url) - 5
                _ =  f"{story_data.get('url', 'No URL')}"
                stories.append(f"{story_id} > {story_data['title'][0:_avail_columns]}")
            self.article_list = stories
            return stories
        else: return self.article_list

    def archlinux(self) -> bool:
        """Determines if host is Arch Linux

            Returns:
                bool: Is this Arch Linux? 

            Raises:
                ExceptionName: Condition that raises this exception.

            Examples:
                >>> Dashboard().archlinux()
                True | False

        """
        return 'arch' in self.os_info()["id"]

    def os_info(self) -> Dict:
        """Dictionary of OS related information scraped from /etc/os-release

            Returns:
                Dict: OS Specific information.

            Raises:
                ExceptionName: Condition that raises this exception.

            Examples:
                >>> Dashboard().os_info()
                expected_output

        """
        res = {}
        try:
            with open('/etc/os-release', 'r') as f:
                os_info = f.read().lower()
            for line in os_info.strip().split('\n'):
                k,v = line.split("=", 1)
                v = v.strip('"')
                res[k] = v
            res["found"] = True
            return res
        except FileNotFoundError:
            res["found"] = False
        return res

    def count_arch_updates(self) -> int:
        """Count the number of available updates for Arch Linux.

            Returns:
                int: Number of updates available.

            Raises:
                ExceptionName: Condition that raises this exception.

            Examples:
                >>> Dashboard().count_arch_updates()
                0 | n

        """
        if self.is_arch:
            result = subprocess.run(['pacman', '-Qu'], capture_output=True, text=True)
            if result.stdout == "":
                return 0
            updates = result.stdout.strip().split('\n')
            if updates[0]:
                return len(updates)
            else:
                return 0
        else:
            return 0

    def article_reader(self, story_id = None) -> List[str]:
        """Returns Text rendered output of Article

            Args:
                story_id (int): Article id to parse.

            Returns:
                List[str]: Itterable article contents.

            Raises:
                ExceptionName: Condition that raises this exception.

            Examples:
                >>> Dashboard().article_reader(1)
                ["Example Article 1 Title","Something great about said article", ". . ."]

        """
        if story_id is None:
            story_id = self.top_story_ids()[0]
        else: 
            self.current_article = story_id
            story_id = self.top_story_ids()[story_id]
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty"
        story_data = requests.get(story_url).json()
        url = story_data.get('url', 'No URL')
        lynx_out = subprocess.run(["lynx", "-dump", url], stdout=subprocess.PIPE).stdout.decode('utf-8', errors='replace')

        return lynx_out.splitlines()
