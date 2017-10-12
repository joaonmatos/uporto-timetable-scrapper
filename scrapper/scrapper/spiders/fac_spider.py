import scrapy

class FacSpider(scrapy.Spider):
    name = "fac"

    start_urls = [
    'https://sigarra.up.pt/up/pt/web_base.gera_pagina?p_pagina=escolas']

    def parse(self, response):
        filename = "faculdades.txt"
        with open(filename, 'wb') as f:
            f.write(response.body)
        for fac in response.css('.menu-nivel-3 > a'):
            print({
                'acronym': fac.css('::attr(href)').extract_first()[2:],
                'name': fac.css('::attr(title)').extract_first()
            })
