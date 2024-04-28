from abc import ABC
from abc import ABC, abstractmethod
from warnings import warn
import arxiv
from dataclasses import dataclass 
from datetime import datetime
import requests
import json
import time
import wikipediaapi
@dataclass
class MetaData:
    '''
    para:
        language:str: optional on [en/zh/fa/de/...] the specific language 
        data_creator:str: who create the datapoint, optional on [human/chatgpt-35/chatgpt-4/claude-3/Llama-3/...]
        task_type:int: if the data is not created by human, you should specify the detailed task, optional on [1/2/3], otherwise fill it with 0 or None
        data_source:str: where to get the data, page name for wiki, paper id for arxiv and book id for gutendex
        date:DateTime: if available, when did the data was created
        other: Anything important
    '''
    language:str = None
    data_creator:str = None
    task_type:int = None
    data_source:str = None
    category:str = None
    date:datetime = None
    other=None

    
class BaseEngine(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def query_meta(self):
        '''
        This function is for processing the metadata of each raw data point. 
        You should implement the function in your engine to determine the way to process metadata.
        '''
        raise NotImplementedError('You should not call the text_process in BaseEngine class')


    @abstractmethod
    def text_process(self,text):
        '''
        This function is for processing the text of each raw data point. 
        You should implement the function in your engine to determine the way to process raw text.
        '''
        raise NotImplementedError('You should not call the text_process in BaseEngine class')

class ArxivEngine(BaseEngine):
    '''
    When using arxivEngine, initialize an instance and then call create meta.
    We use the RedPajama-1T collection of Arxiv data and retrieve the meta data to complete the collection 
    '''
    def __init__(self) -> None:
        self.client = arxiv.Client()

    def get_category(self,primary_category):
        '''
        Process the retrieved category into our format
        '''
        pass

    def text_process(self, text):
        '''
        Process the raw data into our format
        '''
        pass


    def query_meta(self,arxiv_id):
        '''
        check https://github.com/lukasschwab/arxiv.py for more information of the API usage.
        '''
        search = arxiv.Search(id_list=[arxiv_id])
        first_result = next(self.client.results(search))
        category = self.get_category(first_result.primary_category)
        return MetaData(
            language='en',
            data_creator='human',
            task_type='0',
            data_source=arxiv_id,
            category= category,
            date=first_result.updated,
            other=None
        )
    
    def create_data(self, raw_text, arxiv_id):
        '''
        By default, we create one data point for each raw data point, you can create multiple data ponts as well.
        Feel free to modify this function.
        '''
        processed_text = self.text_process(raw_text)
        meta = self.query_meta(arxiv_id)
        return (processed_text, meta)



class GutendexEngine(BaseEngine):
    '''
    We need to get the data from Project Gutenberg directly, because there are too many unrelated books in the collected dataset
    '''
    def __init__(self) -> None:
        self.base_url = "https://gutendex.com/books/?"

    def parse_url(self, url):
        response = requests.get(url)
        parsed_page = json.loads(response.content)
        return parsed_page
    
    def fetech_page(self, page):
        result = []
        for item in page['results']:
            try:
                print(f"\rID: {item['id']} | Title: {item['title']} | Author: {item['authors'][0]['name']}", end="")
                x = requests.get(item['formats']['text/plain; charset=us-ascii'])
                book_record = {
                    "id": {item['id']},
                    "title": {item['title']},
                    "author": {item['authors'][0]['name']},
                }
                result.append((book_record, x.content))
                time.sleep(3)  
            except Exception as e:
                print(f"\nAn error occurred while processing book ID: {item['id']}. Error: {str(e)} \nThis sometimes happens when there is no plaintext version available")
        return result
    
    def get_books(self, query, language):
        result = []
        cnt = 1
        start_point = self.parse_url(self.base_url+f"topic={query}&languages={language}")
        print(f'Processing books of {query}, total number is {start_point.get('count')}')
        print(f'Fetching the data on {cnt}-th page.')
        result.extend(self.fetech_page(start_point))
        next_page = start_point.get("next")
        while next_page:
            cnt+=1
            current_point = self.parse_url(next_page)
            next_page = current_point.get("next")
            print(f'Fetching the data on {cnt}-th page.')
            result.extend(self.fetech_page(current_point))
        return result

    def text_process(self, text):
        '''
        Process the raw data into our format
        '''
        pass

    def query_meta(self,raw, category, language):
        return MetaData(
            language=language,
            data_creator='human',
            task_type='0',
            data_source=raw['id'],
            category= category,
            date=None,
            other=raw
        )

    def create_data(self, category,language='en'):
        raw_data = self.get_books(category)
        result = []
        for raw in raw_data:
            meta, text = raw
            metadata = self.query_meta(meta, category, language)
            text_procesced = self.text_process(text)
            result.append({
                'text':text_procesced,
                'meta': metadata
            })
        return result
    
class WikiEngine(BaseEngine):
    def __init__(self, language='en') -> None:
        self.wiki_wiki = wikipediaapi.Wikipedia('AIdetect (merlin@example.com)', language)
        self.language = language

    def get_categorymembers(self, categorymembers, record, level=0, max_level=1):
        for c in categorymembers.values():
            print("%s: %s (ns: %d)" % ("*" * (level + 1), c.title, c.ns))
            record.append((level+1, c.title))
            if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
                self.get_categorymembers(c.categorymembers, record, level=level + 1, max_level=max_level)


    def text_process(self, text):
        '''
        Process the raw data into our format
        '''
        pass

    def query_meta(self, title, category, level):
        return MetaData(
            language=self.language,
            data_creator='human',
            task_type='0',
            data_source=title,
            category= category,
            date=None,
            other={'level':level}
        )

    def create_data(self, category):
        print('Fetching all pages of depth 1 in a given category')
        record = []
        cat = self.wiki_wiki.page(f"Category:{category}")
        print("Category members: Category:Physics")
        self.get_categorymembers(cat.categorymembers, record)
        print('start fetching')
        result = []
        for level, title in record:
            page= self.wiki_wiki.page(title)
            if not page.exists():
                print(f'Page {title} is not existed')
                continue
            meta = self.query_meta(title, category, level)
            text_procesced = self.text_process(page.text)
            result.append({
                'text':text_procesced,
                'meta': metadata
            })
        return result
            
        
            



