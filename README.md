# NFL Fantasy Projections

  Vegas Sportsbooks have one of the best track records in predicting sports outcomes. If they weren't good, they would lose and be taken out of business. Although fantasy football is a peer to peer game, vegas provides player total projections for things like touchdowns, rushing yards, receptions and all statistics tracked in fantasy football. What would it look like if Vegas drafted a fantasy football team? What players would they pick? What players would they avoid?
  
### Draftkings API
    
    Draftkings is valued at over six billion dollars and has been successful at predicting sports outcomes since 2012. They offer bets through their website. The odds seen by the public are supplied through a public API which allows us to pull their projections directly. With the public API having simple structure, pandas and regex easily clean to a useable database. Simultaneously, applying basic fantasy football scoring functions to each statistic yields what Vegas projects a player to score.
    
### R Shiny Application

  The Shiny Application expresses the distribution of projected points scored by the top projected players. In fantasy football you have fill positions. One example: you must play one QB, two RBs, two WRs and a TE. I provide a widget to query only for the projections of a specific position. This allows the user to not only find the best available player to draft but also the best position. For example, you are drafting and do not have a QB or a TE. QBs are expected to score much more than TEs, so without the positional query the dashboard will recommend the best QB every time. Even when it is not advantageous. Assume the three top available quarterbacks with their repsective projections are Jalen Hurts: 359.57, Patrick Mahomes: 356.57, Kyler Murray: 355.57. Now also assume the top three available tightends with their respective projections are Travis Kelce: 155.3, Mark Andrews: 142.3, Kyle Pitts:	124.3. Jalen Hurts provides only a 3 and 4-point edge to the next best QBs while Travis Kelce holds a 13 and 31-point edge to the next best TEs. The positional query illuminates just how much of a better pick Kelce would be over Jalen Hurts.
  
