## global.R ##
# Katy's Charity Webscraping Project # May 2019 # NYCDSA

#### set up #####################################################

library(shiny)
library(DT)
library(tidyverse)
library(ggplot2)
library(data.table)
library(leaflet)
library(maps)
library(tigris)
library(formattable) # to use currency format
library(ggExtra)

# Read rawdata
df = fread("./CLEAN_charity_data.csv") 
df = df %>% mutate(category = factor(category), subcategory = factor(subcategory))

# size / exp data
size_exp_df = df %>% group_by(size) %>% summarise(admin = mean(admin_exp), program = mean(program_exp), fund = mean(fund_exp)) %>% gather(exp_type, dollar_amt, c('admin','program','fund'))

# global leader data
leadsumdf1 = df %>% group_by(size) %>% summarise(avg_comp = mean(leader_comp, na.rm = T), 
                                          avg_p = mean(leader_comp_p, na.rm = T),
                                          avg_tot_exp = mean(tot_exp))
leadsumdf2 = df %>% group_by(category) %>% summarise(avg_comp = mean(leader_comp, na.rm = T), 
                                                    avg_p = mean(leader_comp_p, na.rm = T),
                                                    avg_tot_exp = mean(tot_exp)) %>% arrange(desc(avg_comp)) %>% head(3)
leadsumdf3 = df %>% group_by(category) %>% summarise(avg_comp = mean(leader_comp, na.rm = T), 
                                                     avg_p = mean(leader_comp_p, na.rm = T),
                                                     avg_tot_exp = mean(tot_exp)) %>% arrange(desc(avg_p)) %>% head(3)

# state data
statedf = df %>% group_by(state) %>% summarise(count = n(),avg_exp = currency(mean(tot_exp)/100000))
merge_state = geo_join(states(cb=T), statedf, "STUSPS", "state")
merge_state = subset(merge_state, !is.na(merge_state$count))