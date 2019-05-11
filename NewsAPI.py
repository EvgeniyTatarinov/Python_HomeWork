from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

# API KEY: c6708f79471a46dc8f6b3b783b1aa4bc


class publications:
    """
    :param API_KEY: your API key
    :return json object
    You can change the following settings:
    pageSize: The number of results to return per page [type(int)]
    page: page number [type(int)]
    language: code of the language
    country: code country
    """
    def __init__(self, API_KEY):
        self.key = API_KEY
        self.pageSize = 20
        self.page = 1
        self.language = 'ru'
        self.country = 'ru'

    def publication_of_categories(self, category):
        """
        Recent publications on the list of categories
        """
        response = requests.get('https://newsapi.org/v2/top-headlines?'
                                f'category={category}&'
                                f'language={self.language}&'
                                f'country={self.country}&'
                                f'page_size={self.pageSize}&'
                                f'page={self.page}',
                                headers={'Authorization': self.key})
        return response.json()

    def publications_of_keywords(self, keyword):
        """
        The last publication in the list of keywords
        """
        response = requests.get('https://newsapi.org/v2/top-headlines?'
                                f'q={keyword}&'
                                f'language={self.language}&'
                                f'country={self.country}&'
                                f'page_size={self.pageSize}&'
                                f'page={self.page}',
                                headers={'Authorization': self.key})
        return response.json()

    def publications_on_request(self, search):
        """
        Search for publications on request
        """
        response = requests.get('https://newsapi.org/v2/everything?'
                                f'q={search}&'
                                'sortBy=relevancy&'
                                f'language={self.language}&'
                                f'page_size={self.pageSize}&'
                                f'page={self.page}',
                                headers={'Authorization': self.key})
        return response.json()


def pool_categoryes(*categoryes, key):
    """
    Search across multiple categories
    :param categoryes: pass categories as a dictionary
    :param key: your API key
    :return: json object {[the name of the category]:{}}
    """
    publik = publications(key)
    with ThreadPoolExecutor() as pool:
        list_categotyes = [
            pool.submit(publik.publication_of_categories, category)
            for category in categoryes
        ]
        result = {}
        for list_category in as_completed(list_categotyes):
            res = list_category.result()
            for category in categoryes:
                result[category] = res
    return result
