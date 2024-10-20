from .base import BaseAgent


class SimpleSearchAgent(BaseAgent):
    """
    Search directly from ElasticSearch, and return result
    """

    pass


class AdvancedSearchAgent(BaseAgent):
    """
    Can use simple words or sentences for search, first determine the type
        of search language, such as text, image, audio, etc., and then search.

    可以用简单的词或句子进行搜索，首先会判断搜索语对应的类型，
        如文本、图片、音频等，然后再进行搜索。
    """

    pass
