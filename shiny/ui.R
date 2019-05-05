# ui.R #
# Katy's Charity Webscraping Project # May 2019 # NYCDSA

# Define UI for application that draws a histogram
shinyUI(fluidPage(
  
  # Application title
  titlePanel("Charity Navigator - Webscrape Data Analysis"),
    
    # Show a plot of the generated distribution
    mainPanel(
      
      # Output: Tabset w/ plot, summary, and table ----
      tabsetPanel(type = "tabs",
                  tabPanel("About", 
                           print(img(src = "CharityNavigatorLogo.PNG", height = "200")),
                           hr(), 
                           h3("Content"),
                           print(h5("Charity Navigator is a major charity assessment organization that evaluates charitable organizations in the United States, operating as a free 501(c)(3) organization that accepts no advertising or donations from the organizations it evaluates.
The data is a public service of Charity Navigator, but the data is likely owned by individual charities. Charity Navigator collects this data. This data was webscraped in May 2019 but uses rating details mostly from 2017. For the most updated information, read about the Charity Navigator
Search API HERE and learn how to apply for access.")),
                           h3("Questions Explored"),
                           print(h5("
                              - Which states have the most rated charities, the least?", tags$br(),
                              "- Do larger or smaller charities spend more on fundraising efforts?",tags$br(),
                              "- Which categories tend to compensate their leaders the most?",tags$br(),
                              "- Is there any correlation between financial score & accountability score?",tags$br())),
                           h3("Links"),
                           uiOutput("kaggle_url"),
                           uiOutput("cn_url")
                           ),
                  
                  tabPanel("State Map", leafletOutput("statemap", width = "150%", height = 800)),
                  tabPanel("Size vs Spending", plotOutput("ssplot", height = 250), plotOutput("catplot", height = 625)),
                  tabPanel("Score Correlation", plotOutput("scorecorr", height = 800)),
                  tabPanel("Leader List",
                  fluidRow( column(6, DT::dataTableOutput("leadsum1")),
                            column(6, DT::dataTableOutput("leadsum2"))),
                            hr(),
                  fluidRow(DT::dataTableOutput("leadlist")))
                
                  #fluidRow(box(DT::dataTableOutput("leadlist"), width = 12)))
    ))
  )
)
