import scrapy
import re

class Itc2Go(scrapy.Spider):
    name = "itc2go"
    start_urls = [
        "https://ict2go.ru/regions/Nizhny_Novgorod/"
    ]

    def get_title(self, info):
        return ""
    
    def get_date(self, info):
        return ""
    
    def get_location(self, info):
        return ""
    
    def get_description(self, info):
        return ""
    
    def get_tags(self, info):
        return ""
            
    
    def parse(self, response):
        for info in response.css("div.event.panel.panel-default"): # вот тут нужно думать
            yield {
                "name": self.get_title(info),
                "start": self.get_date(info),
                "end": self.get_date(info),
                "location": self.get_location(info),
                "description": self.get_description(info),
                "tags": self.get_tags(info)
            }

