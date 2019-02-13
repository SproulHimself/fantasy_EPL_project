
### EPL Fantasy League Optimal Team Generator

My friend and I have been playing the **Official English Premier League Fantasy** for many years, and despite our firm belief that we know everything about English soccer, we somehow get "unlucky" each year and don't win anything. So, we decided to download the player and team data from a few open `APIs` and do a deep dive into all the stats and try to find out if we were really getting unlucky each year or if we were, in fact, a bit delusional about our team-picking skills and were not spending our team budget wisely.

#### Our analysis will aim to answer the key questions below:

- Is there a correlation between individual player Fantasy League stats and their team's total points in the English Premier League EPL and their corresponding table position?

- Can we identify the teams that have a lot of underperforming overpriced players and those that have a very solid undervalued squad?

- Can we approach the **Official English Premier League Fantasy** game as an equivalent of the stock market and look at individual players as financial assets and try to find the underpriced and overpriced players?

>*Individual Player ROI = Player Fantasy points / Player Cost or in other words our total point return per 1MM Fantasy-dollar spent.*

- Our theory is that this can help spend our limited Fantasy League budget of **100MM** on players that will generate the maximum number of points possible for that given budget.

- If that turns out to be true, can we then use `python` to build an algorithm that optimizes the use our budget by picking as many of the high ROI players as possible?

- How does our Algorithm stack against the average person who plays the EPL Fantasy? Did our team return more points and did they beat the average player by a significant margin?

### Procedure:

**1.** Start with the EPL standings table and arrange teams by table position and look at the aggregate squad points for all their players and see if that correlates directly to the team's table standing.

<img src="https://github.com/Botafogo1894/Project1/blob/master/Images/TeamTotalpointsROI.png"/>


>**Questions to answer:**  Are there any surprises and outliers? How can that guide our further investigations?

**2.** Look at each Team's cumulative player ROI and plot that against the number of players that the coach uses on a regular basis **(players who have played at least 350 minutes during the season)** to try to find the teams that have too many expensive and underperforming players and the teams that have a solid core of consistent players that generate a high aggregate ROI.

<img src="https://github.com/Botafogo1894/Project1/blob/master/Images/Teamnumplayers.png"/>

>**Questions to answer:** Are there any surprises and outliers? How can that guide our further investigations?  What teams do the "hidden gem" players belong to? Which teams should we try to avoid buying players from?

**3.** After identifying which teams provide a cumulative ROI, it is time to zoom in on the individual players. We can think of the team as the stock sector and the players as individual stocks. The plan is to isolate a list of players with the highest ROI and write our algorithm logic for picking the most optimal combination of individual players.

<img src="https://github.com/Botafogo1894/Project1/blob/master/Images/PlayerTotalpointsCost.png"/>

 Looking at the scatter plot of Player Cost vs. Player total fantasy points above, we would want our AI to pick players who appear as west-north as possible on the plot. Note, that we would also want to include some of the top players from the east-north corner of the plot since these would be some of the star league players who generate a lot of points, and even though they are a bit expensive, they still end up with a good ROI.

>**Questions to answer:** Does the team data agree with our player data? Do we find a lot of undervalued, high ROI players in those teams that had a good cumulative ROI? Which teams do some of the more overpriced players belong to?

**4.** Next we want to zoom in on the top 50 and bottom 50 players in terms of ROI and compare that to the AVG ROI for all players in the league to get a nice visual idea of what *over-performing* and *underperforming* looks like.



>In the Pie Charts below we can see a distribution of the teams with the most overpriced players versus the teams with the most undervalued players.

<img src="https://github.com/Botafogo1894/Project1/blob/master/Images/Top50Piechart.png"/>

<img src="https://github.com/Botafogo1894/Project1/blob/master/Images/Bottom50Pie.png"/>

**5.** Now it's time for the most fun part - writing the actual `python algorithm` and **comparing the results of the AI picks to what an average person might pick** as their team.  

>**Note** We also asked a classmate to pick a random team of his own so we can compare his picks and verify that our random team picker function is somewhat accurate.

##### To understand the logic of our Algorithm one must first understand the rules of the EPL Fantasy Game. Each player in the game is bound by the constraints below:

* Each fantasy player starts with a limited budget of **100MM** and has to buy at **least 11 players and at most 15 players** in order to compete each round.
* You need to have at least 1 goalkeeper, 4 defenders, 4 midfielders and 2 strikers and at most **2 goalkeepers, 4 defenders, 5 midfielders, and 3 strikers.**
* You **cannot have more than 3 players** from the same team.

So, we start our python algorithm with and `if-else` statement for these conditions and **then we add our own conditions and logic on top of that**, so that each time that the algorithm loops through our list of players, it can **use smart logic to make a valid pick** guided by our conditions below:

* Check if a player is injured and if so, skip that player.
* Pick the top three star players with the most cumulative league points in the league first. (*We will test the outcome of this condition with different constraints and pick the number of star players that generates the biggest return on investment.*)
* Every time we pick a player and add it to our team, we subtract their cost from our 100MM budget and we add their position and team-name to a list, to make sure that we stop buying players for the positions and the teams that hit their constraint limit.
* Once the optimal number of expensive superstar players are picked, the Algorithm starts going through the list of players with the highest ROI and tries to get us as many of the top names as we can, until we get close to depleting our budget and filling all of the team positions.
* Algorithm prints a list of the players it picked at the end and gives us the remaining budget and the total fantasy points of the team.

Here is our `python code` and an explanation of our conditions:

```python
def build_team_by_roi(budget = 100, count_limit = 3, gk = 2, df = 5, md = 5, fwd = 3):
    money_team = []
    budget = budget
    injured = players_by_status('injured')
    positions = {'Goalkeeper': gk, 'Defender': df, 'Midfielder': md, 'Forward': fwd}
    for player in points_top_players():
            if len(money_team) < count_limit and player not in injured and budget >= player.cost and positions[player.position] > 0:
                money_team.append(player)
                budget -= player.cost
                positions[player.position] = positions[player.position] - 1
            else:
                for player in roi_top_players():
                    if player not in money_team and budget >= player.cost and positions[player.position] > 0:
                        money_team.append(player)
                        budget -= player.cost
                        positions[player.position] = positions[player.position] - 1
    final_team = [(item.name, item.position, item.cost) for item in money_team]
    total_points = sum([item.total_points for item in money_team])
    print('Remaining Budget: ' + str(round(budget, 2)))
    print('Your AI has picked the following team:')
    print('GK: '), print([(item[0], item[2]) for item in final_team if item[1] == "Goalkeeper"])
    print('DF: '), print([(item[0], item[2]) for item in final_team if item[1] == "Defender"])
    print('MD: '), print([(item[0], item[2])  for item in final_team if item[1] == "Midfielder"])
    print('FWD: '), print([(item[0], item[2])  for item in final_team if item[1] == "Forward"])
    print('Total Fantasy Points: ' + str(total_points))
    return money_team
```

>**Note** We wrote a similar algorithm for the AVG Joe team, which focuses more on star players and players from big teams, who are often overpriced and might not return the highest cumulative ROI for our limited budget of 100M.

**5.** Now that both algorithms are build and the code was executed, **let's compare the results of our AI Team vs. the AVG Joe team vs. a random Classmate team** to see which one performed best and by what margin. The bar-plot below demonstrates our results. Our team scored a total of **944 points vs only 812 total points for the AVG team**, which is a whoopping 132pt difference! **Success!**

<img src="https://github.com/Botafogo1894/Project1/blob/master/Images/AIsmartPickscomaprison.png"/>

>**Questions to answer:**  Did our Algorithm return the highest ROI team?  Did it beat the others by a significant margin? Did our Algorithm successfully pick players from some middle of the table teams, which we initially identified as undervalued? Did the AVG Joe pick more of the expensive overpriced players from the top teams?

Below we can see that our Algorithm picked a combination of players from most of the high ROI teams that we identified at the beginning of our project:

<img src="https://github.com/Botafogo1894/Project1/blob/master/Images/AITeamDistribution.png"/>

### Conclusion:

Removing team/player biases and favoritism and focusing on the actual player stats, allowed our Algorithm to get the most bang for our buck and **beat the AVG EPL player by a total of 132 pts or a whole 16.25%!** So, it turns out that my friend and I were feeling 'unlucky' and wodnering why we cannot win our Fantasy League each year. This deep dive into the player data allowed us to realize that we were allowing **team favoritism and a tendency to buy a lot of the overpriced players hurt our overall Fantasy League performance.**

>**Next Steps** We plan to keep monitoring the data and see if there are any drastic changes further in the season, when players start getting injured and the battle for points trophies gets more heated. We would also like to compare how the algorithm's team performs at the end of the season compared to most recreational players.
