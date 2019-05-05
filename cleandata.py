# -*- coding: utf-8 -*-
# This script is meant to clean up the data taken from charity webscraper. Written by yours truly (Katy Qian)
# It has 21 columns of X charities, a subset of all after running the scraper for 3hrs on May-3-2019.

# name
# state - DROP rows any not in XX format
# ein 
# category - split into cat/subcat
# score 
# fscore
# ascore
# fp_program_expense 
# revenue
# expenses - DROP rows with ")" badscrape
# leader
# leader_comp - not comp = 0 / not reported = na
# leader_comp_p -  not comp = 0 / not reported = na
# description - consider basic NLP
# motto
# fp_admin_expense- < 0.01% to 0.01
# fp_fund_expense - < 0.01% to 0.01
# fp_fund_efficiency - < $0.01 to 0.01
# fp_wcr - DROP
# fp_program_expenses_growth - DROP
# fp_liabilities_to_asset - DROP

# ADD COLUMNS
# program_exp = program_exp_p * tot_exp
# fund_exp = fp_fund_expense & expense
# admin_exp =  fp_admin_expense & expense
# size - depending on total expenses, 3.5M & 13.5M are cutoffs


################################

# setup
#import sklearn
#import matplotlib as mplot
#import seaborn as sns
#from textblob import TextBlob

import pandas as pd
import numpy as np
filename = 'charitytest.csv'

# pull in raw data & make copy
df = pd.read_csv('./' + filename)

# drop & rename columns
df.drop(['fp_liabilities_to_assets', 'fp_program_expenses_growth', 'fp_wcr'], axis = 1, inplace = True)
df.rename(columns={'expenses':'tot_exp', 'revenue':'tot_rev', 'fp_program_expenses':'program_exp_p','fp_admin_expenses':'admin_exp_p','fp_fund_expenses':'fund_exp_p', 'fp_fund_efficiency':'fund_eff'}, inplace=True)

# drop bad rows
df = df.drop(df[df['state'].str.len() > 2].index) # remove rows with bad states ~.5%
df = df.drop(df[df['tot_exp'] == ")"].index) # remove rows with bad exp ~2.5%

# replacing values - leaders section / fund efficiency
df.loc[:, 'leader_comp'].replace("None reported", np.nan, inplace = True)
df.loc[:, 'leader_comp'].replace("Not compensated", "0", inplace = True)
df.loc[df['leader_comp']== "0", 'leader_comp_p'] = "0"
df.loc[pd.isnull(df['leader_comp']), 'leader_comp_p'] = np.nan

df.loc[:, 'admin_exp_p'].replace("< 0.1%", "0.1%", inplace = True)
df.loc[:, 'fund_exp_p'].replace("< 0.1%", "0.1%", inplace = True)
df.loc[:, 'fund_eff'].replace("< $0.01", "$0.01", inplace = True)

# categories
sub_cat = df['category'].str.split(" : ", n=1, expand = True)
df['category'] = sub_cat[0]
df['subcategory'] = sub_cat[1]
del sub_cat

# convert $strings to floats
dollar_convert = lambda x: x.str.replace("$","").str.replace(",","").astype(float)
df['tot_exp'] = dollar_convert(df['tot_exp'])
df['tot_rev'] = dollar_convert(df['tot_rev'])
df['leader_comp'] = dollar_convert(df['leader_comp'])
df['fund_eff'] = dollar_convert(df['fund_eff'])

# convert string% to floats
percent_convert = lambda y: y.str.replace("%","").astype(float)/100
df['leader_comp_p'] = percent_convert(df['leader_comp_p'])
df['admin_exp_p'] = percent_convert(df['admin_exp_p'])
df['fund_exp_p'] = percent_convert(df['fund_exp_p'])
df['program_exp_p'] = percent_convert(df['program_exp_p'])

# add more columns - size & dollar amounts
df['size'] = np.where(df['tot_exp']>=13500000, 'big',  np.where(df['tot_exp']<=3500000, 'small', 'mid'))
df['program_exp'] = df['program_exp_p']*df['tot_exp']
df['fund_exp'] = df['fund_exp_p']*df['tot_exp']
df['admin_exp'] = df['admin_exp_p']*df['tot_exp']

# print new object types
print(df.dtypes)

# save polished data
df.to_csv('CLEAN' + filename, index=False)
