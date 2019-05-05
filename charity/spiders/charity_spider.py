from scrapy import Spider, Request
from charity.items import CharityItem
import re

class CharitySpider(Spider):
    name = 'charity_spider'
    allowed_urls = ['https://www.charitynavigator.org/']
    start_urls = ['https://www.charitynavigator.org/index.cfm?bay=search.alpha']

    def parse(self, response):

        # get abcurls - there are two SETS so only take the first half
        abc_urls = response.xpath('//p[@class="letters"]/a/@href').extract()
        abc_urls = abc_urls[:int(len(abc_urls)/2)]

        for abc_url in abc_urls: #testing one page first
            yield Request(url = abc_url, callback = self.parse_result_page)

    def parse_result_page(self, response):

        # gets list of charity URLS that start with that letter
        charity_urls = response.xpath('//div[@class="mobile-padding charities"]//a/@href').extract()

        # gets name & state and stores into list for meta pass
        charity_namestates = response.xpath('//div[@class="mobile-padding charities"]//a/text()').extract() 
        charity_name, charity_state = map(list, zip(*(s.split(" - ") for s in charity_namestates)))

        for charity_url in charity_urls:
            yield Request(url = charity_url, callback = self.parse_charity_page, meta = {'name' : charity_name[charity_urls.index(charity_url)], 'state' : charity_state[charity_urls.index(charity_url)]})

    def parse_charity_page(self, response):

        # gets meta data and stores for writing later
        name = response.meta['name']
        state = response.meta['state']

        # Grab info for all of the fields
        motto = response.xpath('//h2[@class="tagline"]/text()').extract_first().strip()
        description = response.xpath('//div[@class ="accordion-item-bd"]/p/text()').extract_first().strip()
        category = response.xpath('//p[@class="crumbs"]/text()').extract_first().strip()

        # EIN ##########################################################
        ein = response.xpath('//div[@class="rating"]/p/text()').extract()
        ein = "".join(ein)
        ein = re.findall(": \d+-\d+",ein)[0].replace(": ","").strip()        

        # Overall Scores ##########################################################
        OSCORES = response.xpath('//div[@class = "shadedtable"]//td/text()').extract()
        OSCORES = [i.strip() for i in OSCORES]
        score = OSCORES[0]
        fscore = OSCORES[1]
        ascore = OSCORES[2]

        # Financial Performance Metrics ##########################################################
        FPM = response.xpath('//div[@class = "accordion-item-bd"]//td[@align="right"]/text()').extract()
        FPM = [i.strip() for i in FPM]
        fp_program_expenses = FPM[0]
        fp_admin_expenses= FPM[1]
        fp_fund_expenses= FPM[2]
        fp_fund_efficiency= FPM[3]
        fp_wcr = FPM[4]
        fp_program_expenses_growth= FPM[5]
        fp_liabilities_to_assets= FPM[6]

        # Account Metrics ##########################################################
        # account_metrics = 

        # Revenues & Expenses ##########################################################
        REVEX = response.xpath('//div[@class="accordion-item-bd rating"]//td//strong/text()').extract()
        REVEX = [i.strip() for i in REVEX]
        revenue = REVEX[3]
        expenses = REVEX[5]

        # Leader Details ##########################################################
        LEAD1 = response.xpath('//div[@class="accordion-item-bd"]//tr//span[@class="rightalign"]/text()').extract()
        LEAD1 = [i.strip() for i in LEAD1]
        leader_comp = LEAD1[0]
        leader_comp_p  = LEAD1[1]
        leader = response.xpath('//div[@class="accordion-item-bd"]//tr//td[@class="text-no-wrap"]/text()').extract_first().strip()

        # assigns everything to item to write to dictionary later ##########################################################
        item = CharityItem()

        item['name'] = name
        item['state'] = state
        # item['address'] = address
        item['ein'] = ein
        item['motto'] = motto
        item['description' ] = description
        item['category'] = category

        item['score'] = score
        item['fscore'] = fscore
        item['ascore'] = ascore

        item['fp_program_expenses' ] = fp_program_expenses
        item['fp_admin_expenses' ] = fp_admin_expenses
        item['fp_fund_expenses' ] = fp_fund_expenses
        item['fp_fund_efficiency' ] = fp_fund_efficiency
        item['fp_wcr' ] = fp_wcr
        item['fp_program_expenses_growth' ] = fp_program_expenses_growth
        item['fp_liabilities_to_assets' ] = fp_liabilities_to_assets

        # item['account_metrics'] = account_metrics

        item['revenue'] = revenue
        item['expenses'  ] = expenses

        item['leader'] = leader
        item['leader_comp'] = leader_comp
        item['leader_comp_p'  ] = leader_comp_p 
        # item['leader_title' ] = leader_title

        yield item


