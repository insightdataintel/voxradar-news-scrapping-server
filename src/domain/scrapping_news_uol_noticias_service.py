import json
import datetime
from flask import request
import datetime
from src.integration.sqs.sqs import Sqs
from src.types.voxradar_news_save_data_queue_dto import VoxradarNewsSaveDataQueueDTO
from src.types.voxradar_news_scrapping_uol_noticias_queue_dto import VoxradarNewsScrappingUolNoticiasQueueDTO
from src.utils.utils import Utils
from ..config.envs import Envs
from .base.base_service import BaseService
from ..types.return_service import ReturnService
from bs4 import BeautifulSoup
import unicodedata
import requests


class ScrappingNewsUolNoticiasService(BaseService):

    sqs: Sqs

    def __init__(self):
        super().__init__()
        # self.log_repository = ViewEstadaoLogRepository()
        # self.s3 = S3()
        self.sqs = Sqs()

    def exec(self, body:str) -> ReturnService:
        self.logger.info(f'\n----- Scrapping News Uol Noticias Service | Init - {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %z")} -----\n')
        uol_dict = {'title': [], 'domain':[],'source':[],'date': [], 'body_news': [], 'link': [],'category': [],'image': []}
        voxradar_news_scrapping_uol_noticias_queue_dto:VoxradarNewsScrappingUolNoticiasQueueDTO = self.__parse_body(body)
        url_news = voxradar_news_scrapping_uol_noticias_queue_dto.url
        page = requests.get(url_news).text
        soup = BeautifulSoup(page, 'html.parser')   

    #title
        #
        title = soup.find("meta", attrs={'property': 'og:title'})
        title = str(title).split("content=")[1].split("property=")[0].replace('"','')
        if (title==""):
            self.logger.error(f"It is cannot possible to retrieve date from Valor")
            title = " "
            pass                 
        #
        #Stardandizing Date
        date = soup.find("script", type="application/ld+json")
        date = str(date).split('"datePublished":')[1].split(',')[0].replace('T', ' ').replace('Z', '').replace('"','').strip()
        date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
        delta = datetime.timedelta(hours=3)
        date = date - delta
        date = "%s-3:00"%(str(date.strftime('%Y-%m-%d %H:%M:%S')))  

        #
        #Pick body's news
        mode = ['div']
        classk = ['text','content']
        paragraf = ['p']
        body_new = ''

        for i in range(0,len(mode)):
            for j in range(0,len(classk)):
                try:
                    yes = soup.find(mode[i],class_= classk[j])
                    if(len(yes)>0):
                        break
                except:
                    None

                    

        for k in range(0,len(paragraf)):
            try:
                body_news = [x.text for x in soup.find(mode[i], class_ = [classk[j],classk[1]]).find_all(paragraf[k]) if len(x.text)>20]
                if(len(body_news)>0):
                    break
            except:
                body_news = [x.text for x in soup.find(mode[i], id = 'textContent').find_all(paragraf[k]) if len(x.text)>20]
                if(len(body_news)>0):
                    break



        no_text = ['Cartola','Leia outras','podcast','Foto','clique aqui','Assine o Premiere','VÍDEOS:','Li e concordo com os Termos de Uso']
        for x in body_news:
            for item in no_text:
                if item in x:
                    x = ''
            if x=='':
                pass
            else:
                body_new = body_new+x+' \n' ##

        # Pick category news
        #   
        category_news = 'noticias'
        category_news = Utils.translate_portuguese_english(category_news)

        #
        #
        #
        # Pick image from news
        #
        ass = soup.find("meta", property="og:image")
        image_new = str(ass).split("content=")[1].split(" ")[0].replace('"','')
        #
        #
        domain = url_news.split("://")[1].split("/")[0]
        source = url_news.split("://")[1].split(".")[1]
        #
        #
        uol_dict["title"].append(title)
        uol_dict["domain"].append(domain)
        uol_dict["source"].append(source)
        uol_dict["date"].append(date)
        uol_dict["body_news"].append(body_new)
        uol_dict["link"].append(url_news)
        uol_dict["category"].append(category_news)
        uol_dict["image"].append(image_new)
        

        print(uol_dict)

        self.__send_queue(title, domain, source, body_new, date, category_news, image_new, url_news)

        return ReturnService(True, 'Sucess')

    def __parse_body(self, body:str) -> VoxradarNewsScrappingUolNoticiasQueueDTO:
        body = json.loads(body)
        return VoxradarNewsScrappingUolNoticiasQueueDTO(body.get('url'))
    
    def __send_queue(self, title: str, domain: str, source: str, content: str, date: str, category: str, image: str, url: str):
        message_queue:VoxradarNewsSaveDataQueueDTO = VoxradarNewsSaveDataQueueDTO(title, domain, source, content, date, category, image, url)
        
        #self.log(None, 'Send to queue {} | {}'.format(Envs.AWS['SQS']['QUEUE']['SIGARP_SAVE_DATA_FOLHA'], message_queue.to_json()), Log.INFO)

        self.sqs.send_message_queue(Envs.AWS['SQS']['QUEUE']['VOXRADAR_NEWS_SAVE_DATA'], message_queue.__str__())



