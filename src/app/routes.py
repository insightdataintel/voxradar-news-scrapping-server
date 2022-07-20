from distutils.debug import DEBUG
import json
import os
import argparse
from flask import Flask, jsonify, request
from flask_cors import CORS
from logzero import logger
from src.domain.scrapping_news_folha_uol_emcimadahora_service import ScrappingNewsFolhaEmcimadahoraService
from src.domain.scrapping_news_globo_g1_service import ScrappingNewsGloboG1Service
from src.domain.scrapping_news_globo_valor_service import ScrappingNewsGloboValorService
from src.domain.scrapping_news_jota_service import ScrappingNewsJotaService
from src.domain.scrapping_news_r7_agronegocios_service import ScrappingNewsR7AgronegociosService
from src.domain.scrapping_news_r7_brasilia_service import ScrappingNewsR7BrasiliaService
from src.domain.scrapping_news_r7_economia_service import ScrappingNewsR7EconomiaService
from src.domain.scrapping_news_r7_educacao_service import ScrappingNewsR7EducacaoService
from src.domain.scrapping_news_r7_internacional_service import ScrappingNewsR7InternacionalService
from src.domain.scrapping_news_r7_politica_service import ScrappingNewsR7PoliticaService
from src.domain.scrapping_news_r7_saude_service import ScrappingNewsR7SaudeService
from src.domain.scrapping_news_r7_tecnologiaeciencia_service import ScrappingNewsR7TecnologiaecienciaService
from src.domain.scrapping_news_uol_economia_service import ScrappingNewsUolEconomiaService
from src.domain.scrapping_news_uol_noticias_service import ScrappingNewsUolNoticiasService
from src.domain.select_news_estadao_service import SelectNewsEstadaoService
from src.domain.select_news_folha_uol_emcimadahora_service import SelectNewsFolhaEmcimadahoraService
from src.domain.select_news_globog1_service import SelectNewsGloboG1Service
from src.domain.select_news_globovalor_service import SelectNewsGloboValorService
from src.domain.select_news_jota_service import SelectNewsJotaService
from src.domain.select_news_r7_agronegocios_service import SelectNewsR7AgronegociosService
from src.domain.select_news_r7_brasilia_service import SelectNewsR7BrasiliaService
from src.domain.select_news_r7_economia_service import SelectNewsR7EconomiaService
from src.domain.select_news_r7_educacao_service import SelectNewsR7EducacaoService
from src.domain.select_news_r7_internacional_service import SelectNewsR7InternacionalService
from src.domain.select_news_r7_politica_service import SelectNewsR7PoliticaService
from src.domain.select_news_r7_saude_service import SelectNewsR7SaudeService
from src.domain.select_news_r7_tecnologiaeciencia_service import SelectNewsR7TecnologiaecienciaService
from src.domain.select_news_uol_economia_service import SelectNewsUolEconomiaService
from src.domain.select_news_uol_noticias_service import SelectNewsUolNoticiasService
from ..domain.scrapping_news_estadao_service import ScrappingNewsEstadaoService
from src.domain.scrapping_news_folha_service import ScrappingNewsFolhaService
from src.domain.select_news_folha_service import SelectNewsFolhaService
from src.domain.scrapping_news_valor_service import ScrappingNewsValorService
from src.domain.select_news_valor_service import SelectNewsValorService

from src.types.return_service import ReturnService
from ..domain.example import ExampleService


class RouteApp():
    
    def create_app(config=None):
        app = Flask(__name__)

        # See http://flask.pocoo.org/docs/latest/config/
        app.config.update(dict(ENV='development', DEBUG=True))
        app.config.update(config or {})

        # Setup cors headers to allow all domains
        # https://flask-cors.readthedocs.io/en/latest/
        CORS(app)

        @app.route("/health")
        def health():
            logger.info("/health")
            return "I'm ok"

        @app.route("/example", methods=['POST'])
        def example():
            logger.info("/example")
            logger.info(request.get_json())

            ExampleService().exec(json.dumps(request.get_json()))
            return "I'm ok"

        @app.route("/select-news-estadao")
        def select_news_estadao():
            logger.info("/estadao")
            SelectNewsEstadaoService().exec()
            return "I'm ok"

        @app.route("/scrapping-news-estadao",methods=['POST'])
        def scrapping_news_estadao():
            logger.info("/estadao")
            ScrappingNewsEstadaoService().exec(json.dumps(request.get_json()))
            return "I'm ok"

        @app.route("/select-news-valor")
        def select_news_valor():
            logger.info("/valor")
            SelectNewsValorService().exec()
            return "I'm ok"

        @app.route("/scrapping-news-valor",methods=['POST'])
        def scrapping_news_valor():
            logger.info("/valor")
            ScrappingNewsValorService().exec(json.dumps(request.get_json()))
            return "I'm ok"

        @app.route("/select-news-folha")
        def select_news_folha():
            logger.info("/folha")
            SelectNewsFolhaService().exec()
            return "I'm ok"

        @app.route("/scrapping-news-folha",methods=['POST'])
        def scrapping_news_folha():
            logger.info("/folha")
            ScrappingNewsFolhaService().exec(json.dumps(request.get_json()))
            return "I'm ok"

        @app.route("/select-news-folha-uol-emcimadahora")
        def select_news_folha_uol_emcimadahora():
            logger.info("/folha-uol-emcimadahora")
            SelectNewsFolhaEmcimadahoraService().exec()
            return "I'm ok"

        @app.route("/scrapping-news-folha-uol-emcimadahora",methods=['POST'])
        def scrapping_news_folha_uol_emcimadahora():
            logger.info("/folha-uol-emcimadahora")
            ScrappingNewsFolhaEmcimadahoraService().exec(json.dumps(request.get_json()))
            return "I'm ok"

        @app.route("/select-news-uol-economia")
        def select_news_uol_economia():
            logger.info("/uol-economia")
            SelectNewsUolEconomiaService().exec()
            return "I'm ok"
        
        @app.route("/scrapping-news-uol-economia",methods=['POST'])
        def scrapping_news_uol_economia():
            logger.info("/uol-economia")
            ScrappingNewsUolEconomiaService().exec(json.dumps(request.get_json()))
            return "I'm ok"

        @app.route("/select-news-uol-noticias")
        def select_news_uol_noticias():
            logger.info("/uol-noticias")
            SelectNewsUolNoticiasService().exec()
            return "I'm ok"
        
        @app.route("/scrapping-news-uol-noticias",methods=['POST'])
        def scrapping_news_uol_noticias():
            logger.info("/uol-noticias")
            ScrappingNewsUolNoticiasService().exec(json.dumps(request.get_json()))
            return "I'm ok"
        
        @app.route("/select-news-globo-valor")
        def select_news_globo_valor():
            logger.info("/globo-valor")
            SelectNewsGloboValorService().exec()
            return "I'm ok"
        
        @app.route("/scrapping-news-globo-valor",methods=['POST'])
        def scrapping_news_globo_valor():
            logger.info("/globo-valor")
            ScrappingNewsGloboValorService().exec(json.dumps(request.get_json()))
            return "I'm ok"
                        
        @app.route("/select-news-globo-g1")
        def select_news_globo_g1():
            logger.info("/globo-g1")
            SelectNewsGloboG1Service().exec()
            return "I'm ok"
        
        @app.route("/scrapping-news-globo-g1",methods=['POST'])
        def scrapping_news_globo_g1():
            logger.info("/globo-g1")
            ScrappingNewsGloboG1Service().exec(json.dumps(request.get_json()))
            return "I'm ok"     

        @app.route("/select-news-r7-politica")
        def select_news_r7_politica():
            logger.info("/r7-politica")
            SelectNewsR7PoliticaService().exec()
            return "I'm ok"
        
        @app.route("/scrapping-news-r7-politica",methods=['POST'])
        def scrapping_news_r7_politica():
            logger.info("/r7-politica")
            ScrappingNewsR7PoliticaService().exec(json.dumps(request.get_json()))
            return "I'm ok"                                  
            
        @app.route("/select-news-r7-economia")
        def select_news_r7_economia():
            logger.info("/r7-economia")
            SelectNewsR7EconomiaService().exec()
            return "I'm ok"
        
        @app.route("/scrapping-news-r7-economia",methods=['POST'])
        def scrapping_news_r7_economia():
            logger.info("/r7-economia")
            ScrappingNewsR7EconomiaService().exec(json.dumps(request.get_json()))
            return "I'm ok"    

        @app.route("/select-news-r7-agronegocios")
        def select_news_r7_agronegocios():
            logger.info("/r7-agronegocios")
            SelectNewsR7AgronegociosService().exec()
            return "I'm ok"
        
        @app.route("/scrapping-news-r7-agronegocios",methods=['POST'])
        def scrapping_news_r7_agronegocios():
            logger.info("/r7-agronegocios")
            ScrappingNewsR7AgronegociosService().exec(json.dumps(request.get_json()))
            return "I'm ok"  
                        
        @app.route("/select-news-r7-tecnologiaeciencia")
        def select_news_r7_tecnologiaeciencia():
            logger.info("/r7-tecnologiaeciencia")
            SelectNewsR7TecnologiaecienciaService().exec()
            return "I'm ok"
        
        @app.route("/scrapping-news-r7-tecnologiaeciencia",methods=['POST'])
        def scrapping_news_r7_tecnologiaeciencia():
            logger.info("/r7-tecnologiaeciencia")
            ScrappingNewsR7TecnologiaecienciaService().exec(json.dumps(request.get_json()))
            return "I'm ok"  


        @app.route("/select-news-r7-saude")
        def select_news_r7_saude():
            logger.info("/r7-saude")
            SelectNewsR7SaudeService().exec()
            return "I'm ok"
        
        @app.route("/scrapping-news-r7-saude",methods=['POST'])
        def scrapping_news_r7_saude():
            logger.info("/r7-saude")
            ScrappingNewsR7SaudeService().exec(json.dumps(request.get_json()))
            return "I'm ok"  

        @app.route("/select-news-r7-brasilia")
        def select_news_r7_brasilia():
            logger.info("/r7-brasilia")
            SelectNewsR7BrasiliaService().exec()
            return "I'm ok"
        
        @app.route("/scrapping-news-r7-brasilia",methods=['POST'])
        def scrapping_news_r7_brasilia():
            logger.info("/r7-brasilia")
            ScrappingNewsR7BrasiliaService().exec(json.dumps(request.get_json()))
            return "I'm ok"              

        @app.route("/select-news-r7-internacional")
        def select_news_r7_internacional():
            logger.info("/r7-internacional")
            SelectNewsR7InternacionalService().exec()
            return "I'm ok"
        
        @app.route("/scrapping-news-r7-internacional",methods=['POST'])
        def scrapping_news_r7_internacional():
            logger.info("/r7-internacional")
            ScrappingNewsR7InternacionalService().exec(json.dumps(request.get_json()))
            return "I'm ok"              

        @app.route("/select-news-r7-educacao")
        def select_news_r7_educacao():
            logger.info("/r7-educacao")
            SelectNewsR7EducacaoService().exec()
            return "I'm ok"
        
        @app.route("/scrapping-news-r7-educacao",methods=['POST'])
        def scrapping_news_r7_educacao():
            logger.info("/r7-educacao")
            ScrappingNewsR7EducacaoService().exec(json.dumps(request.get_json()))
            return "I'm ok"      

        @app.route("/select-news-jota")
        def select_news_jota():
            logger.info("/jota")
            SelectNewsJotaService().exec()
            return "I'm ok"
        
        @app.route("/scrapping-news-jota",methods=['POST'])
        def scrapping_news_jota():
            logger.info("/jota")
            ScrappingNewsJotaService().exec(json.dumps(request.get_json()))
            return "I'm ok"  
                                                                                              
        return app
