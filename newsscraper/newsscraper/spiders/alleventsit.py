import scrapy
import re

class AllEventsIT(scrapy.Spider):
    name = "alleventsit"
    start_urls = [
        "https://all-events.ru/events/calendar/city-is-nizhniy_novgorod/"
    ]

    def get_title(self, info):
        return info.css("div.event_flex_content").css("div.event_order_1").css("a.event_name_new::text").get()

    def get_start_date(self, info):
        result = info.xpath('.//div[@class="event-date"]/div[not(@class)]/text()').get()
        return result[0:10]

    def get_end_date(self, info):
        text = info.xpath('.//div[@class="event-date"]/div[not(@class)]/text()').get()
        text = text.replace('\xa0', ' ').strip()
        match = re.search(r'(\d{2}\.\d{2}\.\d{4})(?:\s*-\s*(\d{2}\.\d{2}\.\d{4}))?', text)
        if match:
            if match.group(2):
                return match.group(2)
            return match.group(1)

        return None
    
    def get_location(self, info):
        return ','.join(info.css(
            "div.event_flex_content div.event_width.order_3 div.event_info_new "
            "a.event_info_new_text.svg_hybrid span:nth-of-type(2)::text,"
            "div.event_flex_content div.event_width.order_3 div.event_info_new "
            "a.event_info_new_text.svg_ span:nth-of-type(2)::text,"
            "div.event_flex_content div.event_width.order_3 div.event_info_new "
            "a.event_info_new_text.svg_offline span:nth-of-type(2)::text"
        ).getall())
    
    def get_description(self, info):
        return ""
    
    def get_tags(self, info):
        tags_div = info.css("div.event_flex_content div.event_width.order_2 div.teg_content").get()
        # Получаем все ссылки (теги) из div
        tags = info.css("div.teg_content a::text").getall()
        return ', '.join(tag.strip() for tag in tags)  # Объединяем их в строку через запятую

    def parse(self, response):

        for info in response.css("div.event_flex_item"):
            yield {
                "name": self.get_title(info),
                "start": self.get_start_date(info),
                "end": self.get_end_date(info),
                "location": self.get_location(info),
                "description": self.get_description(info),
                "tags": self.get_tags(info)
            }