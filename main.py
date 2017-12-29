import lxml.html
import scraper as sc
import requests


class Scraping:

    def __init__(self):
        self.default_url = 'http://www.sgc.org.sg/members/members-directory/?no_cache=1&tx_cpsmvz_pi1[pointer]='
        self.url = lambda number: self.default_url+str(number)
        self.number = 1
        self.data = []

    def get_data(self):
        for i in range(1, 27):
            print(self.url(self.number))
            self.source = requests.get(self.url(self.number))
            self.tree = lxml.html.fromstring(self.source.content)
            self.etree = self.tree.xpath('//div[@class="listWrap"]/div[@class="listItemWrap"]')
            for element in self.etree:
                self.site = sc.get_href(element.xpath('./h3/a[@href]'))
                self.name = sc.first_value(element.xpath('./h3/a/text()'))
                self.location = sc.get_text(element.xpath('./text()'))
                self.data.append([self.name, self.site, self.location])
            self.number += 1
        sc.Database(('name', 'site', 'location')).push_data(self.data)


Scraping = Scraping()
Scraping.get_data()
