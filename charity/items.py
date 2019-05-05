# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

# TEST WITH THIS!!!
# scrapy shell -s USER_AGENT="" "url" 

# USEFUL URLS
# https://www.charitynavigator.org/index.cfm?bay=search.alpha
# https://github.com/Minger/charity-navigator-scraper

import scrapy

class CharityItem(scrapy.Item):

    name = scrapy.Field()
    state = scrapy.Field()
    # address = scrapy.Field()
    ein = scrapy.Field()
    motto = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    score = scrapy.Field()
    fscore = scrapy.Field()
    ascore = scrapy.Field()

    fp_program_expenses= scrapy.Field()
    fp_admin_expenses= scrapy.Field()
    fp_fund_expenses= scrapy.Field()
    fp_fund_efficiency= scrapy.Field()
    fp_wcr = scrapy.Field()     
    fp_program_expenses_growth= scrapy.Field()
    fp_liabilities_to_assets= scrapy.Field()

    # account_metrics = scrapy.Field()

    revenue = scrapy.Field()
    expenses = scrapy.Field()

    leader = scrapy.Field()
    leader_comp = scrapy.Field()
    leader_comp_p  = scrapy.Field()
    # leader_title = scrapy.Field()

    # historical scores?
    # detailed expenses?
    # detailed accountability metrics?

