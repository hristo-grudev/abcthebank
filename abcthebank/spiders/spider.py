import scrapy

from scrapy.loader import ItemLoader

from ..items import AbcthebankItem
from itemloaders.processors import TakeFirst
import requests

url = "https://www.abcthebank.com/wp-admin/admin-ajax.php"

payload = "action=pagination_request&sid=cdac1917gr&unid=&page={}&lang=&ajax_nonce=b28621388a"
headers = {
  'Connection': 'keep-alive',
  'Pragma': 'no-cache',
  'Cache-Control': 'no-cache',
  'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
  'Accept': '*/*',
  'X-Requested-With': 'XMLHttpRequest',
  'sec-ch-ua-mobile': '?0',
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'Origin': 'https://www.abcthebank.com',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Dest': 'empty',
  'Referer': 'https://www.abcthebank.com/',
  'Accept-Language': 'en-US,en;q=0.9,bg;q=0.8',
  'Cookie': 'PHPSESSID=619503017a2f11de45372f4ed94c6ade; __ss_tk=202103%7C6062dc9c50648759353658be; _ga=GA1.2.153930602.1618233412; __ss=1618388893430; __ss_referrer=https%3A//www.abcthebank.com/; _gid=GA1.2.249582471.1618388894; _gat_gtag_UA_178538257_1=1'
}


class AbcthebankSpider(scrapy.Spider):
	name = 'abcthebank'
	page = 1
	start_urls = ['https://www.abcthebank.com/abc-bank-sponsors-visa-oshwal-community-eye-clinic-kisumu/']

	def parse(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="entry-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//time[@class="entry-date"]/text()').get()

		item = ItemLoader(item=AbcthebankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		yield item.load_item()

		post_links = response.xpath('//a[@rel="next"]/@href').getall()
		print(post_links)
		yield from response.follow_all(post_links, self.parse)
