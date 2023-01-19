from datetime import datetime, timedelta
from typing import List
import wikipedia
import networkx
from collections import deque
import time

from main import logger, session, engine
from model import PageModel, LinkModel
import warnings


requests_per_minute = 100
links_per_page = 200
language = "uk"
max_time_script_execution = 10

wait_time_between_requests = 6000 / requests_per_minute

wikipedia.set_lang(language)
wikipedia.set_rate_limiting(rate_limit=True, min_wait=timedelta(milliseconds=wait_time_between_requests))
warnings.catch_warnings()
warnings.simplefilter("ignore")


def get_page_titles_from_db(title):
    titles = None
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
    try:
        page = wikipedia.page(title=title)
        titles = page.links[0:200]
    except wikipedia.exceptions.HTTPTimeoutError:
        return
    except wikipedia.exceptions.PageError:
        return titles
    except wikipedia.exceptions.DisambiguationError:
        return titles
    except Exception as err:
        logger.warning(f" Cannot get page`s titles: {title} from WIIKI. Action failed with error: {err}")
        return
    main_page = PageModel(title=title)
    for page in titles:
        new_page = session.query(LinkModel).where(LinkModel.title == page).first()
        if new_page is None:
            new_page = LinkModel(title=page)
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
    if titles is None:
        titles = get_page_titles_from_wiki(title)
    if titles is None:
        raise Exception('Search resources: DB and Wiki. Not available!')
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
                if not self.program_continue:
                    break
                titles = get_titles(item)
                if finish in titles:
                    graph.add_edge(item, finish)
                    continue
                for title in titles:
                    queue.append(title)
                    graph.add_edge(item, title)
                    if not self.program_continue:
                        break
                queue.popleft()

        try:
            result = list(networkx.dijkstra_path(graph, start, finish))
        except networkx.exception.NetworkXNoPath:
            return result
        return result