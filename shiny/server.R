# server.R #
# Katy's Charity Webscraping Project # May 2019 # NYCDSA

shinyServer(function(input, output, session) {
  
  # State map showing counts of charities
  output$statemap = renderLeaflet({
    
    pal = colorNumeric("Greens", domain = merge_state$count)
    popup_sb = paste0("<strong>", merge_state$NAME, "</strong>",
                      "<br />Charities: ", as.character(merge_state$count), 
                      "<br />Avg Exp: ", as.character(merge_state$avg_exp), "M")
      
    leaflet() %>% 
      addProviderTiles("CartoDB.Positron") %>%
      setView(-98.483330, 38.712046, zoom = 5) %>%
      addPolygons(data=merge_state, 
                  fillColor = ~pal(merge_state$count),
                  weight = .5,
                  fillOpacity = 0.7,
                  popup = ~popup_sb
                  )

  })
  
  # Pie Charts showing size vs Spending percentages
  output$ssplot <- renderPlot({
    ggplot(size_exp_df, aes(x=factor(1), y=dollar_amt, fill=exp_type)) + geom_bar(width = 1, position = "fill", stat = "identity") + xlab("") + ylab("") + facet_grid(facets=. ~ size) + coord_polar("y") + theme(legend.position = "right", axis.text = element_blank(), text = element_text(size=15))
     
  })
  
  # Violin Chart showing CATs vs Spendings
  output$catplot <- renderPlot({
    ggplot(df, aes(x=category, y=tot_exp/1000000)) + geom_violin(aes(fill = category)) + coord_cartesian(ylim = c(0,20)) + theme(legend.position = "None", text = element_text(size=15), axis.text.x = element_text(angle = 20, hjust = 1)) + ylab("Total Expenses in $ Millions") + xlab("") + geom_hline(yintercept=c(3.5,13.5), linetype="dashed")
    
  })

  # Scatter plot showing A & F score correlations  
  output$scorecorr <- renderPlot({
      ggMarginal(ggplot(filter(df, fscore >0), aes(x=fscore, y=ascore)) 
       + geom_point(aes(color = size, size = size), position = "jitter")
       + scale_size_manual(values=c(3,2,1))
       + theme(legend.position = "top", text = element_text(size=20))
       + labs(y = "Accountability Score", x="Financial Score"), type = "histogram", fill="transparent")
    })
  
  # Data Table showing just the leader details
  output$leadlist = DT::renderDataTable({
      tempdf = df %>% select(leader, leader_comp, leader_comp_p, category, size, name, score) %>% arrange(desc(leader_comp))
      datatable(tempdf, rownames=FALSE) %>% formatCurrency('leader_comp') %>% formatPercentage('leader_comp_p', 2) })

  output$leadsum1 = DT::renderDataTable({ 
      datatable(leadsumdf1, rownames=FALSE, options = list(dom = 't')) %>% formatCurrency(c('avg_comp', 'avg_tot_exp')) %>% formatPercentage('avg_p', 2) })
   
  output$leadsum2 = DT::renderDataTable({ 
      datatable(leadsumdf2, rownames=FALSE, options = list(dom = 't')) %>% formatCurrency(c('avg_comp', 'avg_tot_exp')) %>% formatPercentage('avg_p', 2) })
 

  # URLS
  url1 = a("Kaggle Dataset", href="https://www.kaggle.com/katyjqian/charity-navigator-scores-expenses-dataset/")
  url2 = a("Charity Navigator", href="https://www.charitynavigator.org/")
  
  output$kaggle_url <- renderUI({ url1})
  output$cn_url <- renderUI({ url2 })
  
})

  