import scrapy
import string

class Dicionario(scrapy.Spider):
    name = "Dicionario"

    def start_requests(self):
        all_pagination = list(range(0,25000,100))
        urls = []
        for letter in string.ascii_lowercase:
            for pagination in all_pagination:
                urls.append(f'http://www.portaldalinguaportuguesa.org/index.php?action=syllables&act=list&letter={letter}&start={pagination}')
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #print('\n\n\n',response.request.url)
        table = response.xpath('//table[@id="rollovertable"]')
        for row in table.xpath('tr'):
            palavra = row.xpath('td[1]/b/a/text()').extract_first()
            categoria = row.xpath('td[1]/text()').extract_first()
            separacao = row.xpath('td[2]')
            silaba = row.xpath('td[2]/u/b/text()').extract_first()
            #print(f'palavra{palavra},categoria{categoria},separacao{separacao},silaba{silaba}')
            yield {
                'palavra': palavra,
                'categoria': categoria,
                'separacao': ''.join(separacao.xpath('.//text()').extract()).strip(),
                'silaba': silaba,
                }
