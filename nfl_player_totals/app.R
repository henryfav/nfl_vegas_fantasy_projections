
library(shiny)

library(tidyverse)
library(tidyr)
library(dplyr)

# Read in data
QB <- read.csv("data/Vegas_QB_Projections.csv")
RB <- read.csv("data/Vegas_RB_Projections.csv")
WR <- read.csv("data/Vegas_WR_Projections.csv")
TE <- read.csv("data/Vegas_TE_Projections.csv")


# Define UI for application that draws a histogram
ui <- fluidPage(

    # Application title
    titlePanel("Vegas-Based Fantasy Projections"),

    # Sidebar with a slider input for number of bins 
    sidebarLayout(
        sidebarPanel(
            helpText("Las Vegas Sportsbooks are one of the strongest predictors of outcomes. 
                     Explore how many fantasy points players are projected to score. We include
                     how many points less than the top scorer a player is projected at the end
                     of their bar."),
            selectInput("pos",
                        label = h3("Choose a Position"),
                        choices = c("Quarterback", "Running Back",
                                    "Wide Receiver", "Tight End")),
            
            radioButtons("num", label = h3("How many players?"),
                         choices = c("3", "5", "8"))
        ),

        # Show a plot of the generated distribution
        mainPanel(
           plotOutput("distPlot")
        )
    )
)

# Define server logic required to draw a histogram
server <- function(input, output) {

    output$distPlot <- renderPlot({
        # select dataframe of current position
        db <- switch(input$pos,
                     "Quarterback" = QB,
                     "Running Back"= RB,
                     "Wide Receiver" = WR,
                     "Tight End" = TE)
        
        #Maintain graphing order by points, not alphabetical names
        db$Player <- factor(db$Player, levels = db$Player)
        
        #Query only top number of players requested
        dfviz <- switch(input$num,
                     "3" = head(db,3),
                     "5" = head(db,5),
                     "8" = head(db,8))
        
        #produce points from top player for visual
        #pptop = points from top
        dfviz <- dfviz %>%
          mutate(pptop = max(dfviz$Points)-Points)

        
        
        #subset for just expected points in dataset
        
        #Plotting
        ggplot(dfviz, aes(Points, Player)) +
          geom_col(aes(fill=Points)) +
          scale_fill_continuous( low='red',high='green') +
          theme_minimal() +
          scale_y_discrete(limits=rev) +
          xlab(element_text("Projected Points", size = 32)) +
          labs(x = element_text("Projected Points"),
               y = element_text(paste(input$pos,"s", sep=''))) +
          geom_segment(aes(xend=Points, x=max(Points), y=Player, yend=Player)) +
          geom_label(aes(x=Points, y=Player, label=pptop))
        

        
        #p2 <- ggplot(vizcopy, aes(Points Players)) +
         # geom_te
        
    })
}

# Run the application 
shinyApp(ui = ui, server = server)
