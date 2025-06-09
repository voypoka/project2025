import scrapy
import re

class Itc2Go(scrapy.Spider):
    name = "itc2go"
    start_urls = [
        "https://ict2go.ru/regions/Nizhny_Novgorod/"
    ]

    def get_title(self, info):
        return info.css("div.index-events div#index_events div.index-events-item.media div.media-body a.event-title::text").get()
    
    def get_start_date(self, info):
        return info.css("div.index-events div#index_events div.index-events-item.media div.media-body div.date-place").get()


    def get_end_date(self, info):
        return None
    
    def get_location(self, info): #надо переходить по ссылке
        return ""
    
    def get_description(self, info):
        return ""
    
    def get_tags(self, info):
        tags_div = info.css("div.index-events div#index_events div.index-events-item.media div.media-body div.event-themes").get()
        # Получаем все ссылки (теги) из div
        tags = info.css("div.event-themes a::text").getall()
        return ', '.join(tag.strip() for tag in tags)  # Объединяем их в строку через запятую
            
    
    def parse(self, response):
        for info in response.css("div.index-events div#index_events div.index-events-item.media"):
            yield {
                "name": self.get_title(info),
                "start": self.get_start_date(info),
                "end": self.get_end_date(info),
                "location": self.get_location(info),
                "description": self.get_description(info),
                "tags": self.get_tags(info)
            }