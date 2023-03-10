from datetime import datetime, timedelta
from typing import List
import wikipedia
import networkx
from collections import deque


from main import logger, session
from model import PageModel
import warnings


requests_per_minute = 100
links_per_page = 200
language = "uk"
max_time_script_execution = 2000

wait_time_between_requests = 6000 / requests_per_minute

wikipedia.set_lang(language)
wikipedia.set_rate_limiting(rate_limit=True, min_wait=timedelta(milliseconds=wait_time_between_requests))
warnings.catch_warnings()
warnings.simplefilter("ignore")



def get_page_titles_from_db(title):
    titles = []
    page = None
    try:
        page = session.query(PageModel).filter(PageModel.title == title).first()
    except Exception as err:
        logger.warning(f" Cannot get page title: {title}from DB. Action failed with error: {err}")
    if page is not None:
        titles = [title.title for title in page.links_on_page]
    return titles


def get_page_titles_from_wiki(title):
    titles = []
    main_page = None
    try:
        page = wikipedia.page(title=title)
        titles = page.links[0:200]
    except (wikipedia.exceptions.PageError,
            wikipedia.exceptions.DisambiguationError,
            Exception) as err:
        logger.warning(f" Cannot get page`s titles: {title} from WIIKI. Action failed with error: {err}")
        return titles
    try:
       main_page = session.query(PageModel).filter(PageModel.title == title).first()
    except Exception as err:
        logger.warning(f" Cannot create page with title: {title}. Action failed with error: {err}")
    if main_page is None:
        main_page = PageModel(title=title)
    for title in titles:
        new_page = session.query(PageModel).filter(PageModel.title == title).first()
        if new_page is None:
            new_page = PageModel(title=title)
        main_page.links_on_page.append(new_page)
    session.add(main_page)
    session.commit()
    return titles


def get_titles(title):
    """ Function take titles on the page.
        Try to take titles from different source:
        1) Database
        2) site Wikipedia

        In the future we can add:
         - Cache (don`t work now)
     """
    titles = get_page_titles_from_db(title)
    if not titles:
        titles = get_page_titles_from_wiki(title)
    return titles


class WikiRacer:

    def __init__(self):
        self.start_time = datetime.now()
        self.max_time_execution = timedelta(seconds=max_time_script_execution)

    @property
    def program_continue(self):
        delta = datetime.now() - self.start_time
        return delta < self.max_time_execution

    def find_path(self, start: str, finish: str) -> List[str]:
        result = []
        graph = networkx.Graph()
        queue = deque()
        queue.append(start)
        print()
        print("Script Start:", self.start_time.time())
        print(f"Max time script execution:{max_time_script_execution} seconds.")

        while self.program_continue:
            for item in list(queue):
                titles = get_titles(item)
                for title in titles:
                    if not self.program_continue:
                        return result
                    queue.append(title)
                    graph.add_edge(item, title)
                    try:
                        result = list(networkx.shortest_path(graph, start, finish))
                        return result
                    except networkx.exception.NetworkXNoPath:
                        continue
                    except networkx.exception.NodeNotFound:
                        continue
                queue.popleft()
        return result

def app():
    """
    Should to add data validation in the future with marshmallow.
    """
    start = input("Enter start title:")
    finish = input("Enter finish title:")
    race = WikiRacer()
    print(f"Result: {race.find_path(start, finish)}")


if __name__ == "__main__":
    app()