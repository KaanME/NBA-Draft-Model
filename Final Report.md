# NBA Draft Model
## Introduction

As data becomes more and more an integral part of how decisions are made throughout a variety of industries, sports teams have also come around to the idea of data science as a tool. Several NBA teams have shifted their focus more and more towards being analytics driven organizations. There are many different ways that data can be collected, analyzed, and applied within the basketball world. Box score statistics have been around since the game itself started, which led the way to more advanced statistics such as looking at efficiency ratings by looking at the stats on a per minute or per possession basis. More recently, companies like Second Spectrum and Synergy have started player tracking, where the datasets contain x, y, and z coordinates for each player and the ball. The amount of insights that can be obtained through all this data has created an exciting period in the world of basketball.
For the purposes of this paper, advance statistics of College and NBA players will be used in order to create a model that ranks college prospects trying to get drafted into the NBA. By looking at historical data about how statistical profiles in college translate to the NBA, as well as physical measurement, an exclusively numbers based model can help in the crucial decision process that is the NBA draft. As player tracking companies start moving into college arenas, this process will also continue to improve in its sophistication.

## Data Acquisition and Cleaning
I initially wanted to scrape the NCAA website and combine it with the NBA game log data set I had created for my NBA fantasy score model. I found the [NCAAB Stats Scraper](https://github.com/rodzam/ncaab-stats-scraper) repository on Github and started digging through it.  Some of the links and python functions were out dated, so I cleaned it up and made sure it walked through every game box score for each NCAA season dating back to 2003-04. I successfully scraped the data and now face the task of matching up all the players by name to the NBA data set I had.
Around this time, I found about Will Schreefer's "draft-toolkit". It contains box score stats, advanced stats, and physical measurements  for all college, NBA, G-League, Summer League, and International players dating back to the 2003-04 season. Most of the data was pulled from RealGM.com, and I decided to use this database instead because the players were already linked by a player key. However, to build a draft model, I also needed historical draft data. I found a dataset on Kaggle, [NBA Draft Data](https://www.kaggle.com/pmp5kh/nba-draft-19802017), where it gives me the players name, the draft year, and what pick they were drafted. From there I cleaned up the names to make them match with the draft toolkit. The following [Data Cleaning](https://github.com/KaanME/NBA-Draft-Model/blob/master/data_cleaning.py) notebook shows the process by which I did that.

## Data Exploration
In order to understand which variables perform the best at predicting future NBA success and draft position, I split the data into 2 sets. The first set contains the final college season stats of all NCAA players that went on to be drafted. The second dataset contains the rookie season stats of every NBA players. From there, I compared the college averages of certain stats to the stats of the same player in there rookie season. I also looked at how age playes a role in where a player gets selected. 

### Where Are College Players Going After Graduation?

Before diving into the statistical profiles of the players, understanding the distribution of professional basketball players post college gives us an idea of where the sport is trending. In Figure 1 below, we see the percentage of where players who go on to play pro basketball actually play.The light grey line cutting through all the bars is the total number of players that went from NCAA to pro that  season. In the early 2000's international basketball didn't have the pul that it does today, and the G-Leaugue (D-League then) nor Summer League was as high quality as they are today. This is why there are less players that went pro, and more than 20% of players that did actually went to NBA. There are only 60 picks in the draft, plus the handful of players that actually get signed undrafted, so as the number of players that go pro at any level increase, the percentage that goes to the NBA decreases. There are a couple other trends to note here. As popularity of basketball grew around the world with players like Dirk Nowitzki and Yao Ming finding success, we can see that players went oversees more often to continue there careers (which probably corelated with the increased opppurtunity to play internationally as well). In more recent years, we see the percentage of college-to-pro players head to the D-League. The quality of the D-Leauge (now G-League) has been improving every year, and players like the idea of staying in there home country playing for an NBA affiliate team where there chances of being noticed post-college might be higher. This trend could continue, and taking a look at salary trends over the years for different places would be an informative next step, but that is out of the scope of this project.

<p align="center"> 
<img src="/assets/PctdPro.png">
<p align="center"><b> Figure 1: Percentage Distribution of College Players to Professional Leagues </b>
</p>


### Statistical Correlation
The first step in understanding which stats translate from college to the pros is to look at scatter plots with the college average on one axis and the rookie season average on the other. Figure 2 below shows 12 different statistics to see which ones can be predictive of future success.


<p align="center"> 
<img src="/assets/StatCorreletions.png">
<p align="center"><b> Figure 2: College to Rookie season stat correlations</b>
</p>

I chose the 5 main box score stats (Points, Assists, Rebounds, Steals, and Blocks), their related percentage stats, as well as 2 advanced stats in Player Efficiency Rating (PER) and Win Shares (WS) to see what carried over. Looking through each plot, the 2 stats that really stand out are Rebound Percentage and Block Percentage, which both had PEarson Correlation coefficents greater than .82. Rebound percentage is the percentage of available rebounds that a player grabbed while he was on the floor. On the other hand, block percentage is the percentage of opponent 2 point attempts blocked by the player while he was on the floor. These high correlation numbers tell us that if a player, presumeably a big man, grabs a high percentage of rebounds in college, he'll likely grab a high percentage of them in the NBA as well. The reason why the correlation is higher for the percentage stats, rather than the raw averages, is because the percentage stats look only at the time that the player sees the floor. Rookies tend to not get as many minutes in the pros than they are used to in college, so the overall numbers are far more likely to go down. 
Another statistic with a seemingly high colelge to rookie season correlation is Assist Percentage, with a pearson correlation cefficient of .793. Much like rebounding and blocks, assist percentage is defined as the percentage of field goals made by the team that the player assisted while he was in the game. This tells us the if a player is responsible for a large portion of his teams baskets in college, he will tend to have a similar effect in the game when he transitions to the pros. 

A couples stats that don't seeme to be strong indicators of NBA performance is average points per game, true shooting percentage, and PER. Raw points per game averages not translating can be justified by the fact that most nba players were the stars of their college squads. The ahd a lot more oppurtunity to score in college than they do in the NBA. However, unlike blocks, rebounds, and assists, the efficiency metric for shooting, true shooting percentage, doesn't correlate better. True shooting percentage takes into account 2 point, 3 point, and free throw shooting percentages and normalizes for 3 pointers being worth more points and free throws not being counted in traditional field goal percentage. 

### Age of Draftees

Besides statistical profiles, there are physical and qualities of players that are heavily considered by team in the drafting process. One trend that is evident in Figure 3 below that the average age of players being drafted has been going down since the early 2000's. In 2009, the NBA had a rule change that required players to play at least one year of college or professional ball before being eligible to enter the draft. The effect of this rule change can clearly be seen in the graph. In the following years until present day, the average age has gotten back down the same level as it reched in 2008, even with the high school-to-league path disallowed. The longer development time in the league has proven valuable overtime, plus the overall athleticism and popularity of the game has increase leading to higher quality facilities and competition at earlier ages. Now the NBA is considering removing the restriction around 2022, which will most likely cause a large dip in the curve that year. This will be a trend to monitor the years move along.

<p align="center"> 
<img src="/assets/draftAgeOverTime.png">
<p align="center"><b> Figure 3: Average Draftee Age Over Time </b>
</p>

In Figure 3 we saw the average age of each draft group ofver time, but the importance of age can also be tied to how high a player gets drafted. In Figure 4 below, the average age is plotted against draft position. Although the line is jagged, the trend is clear: older players are draft later in the draft. We know that overall the age of players drafted is on the decline year over year, and the youngest among them are the top picks in the draft. 

<p align="center"> 
<img src="/assets/AgeByDraftPick.png">
<p align="center"><b> Figure 4: Average Draftee Age by Pick </b>
</p>

## Machine Learning
This is no definitive or objective ranking that anyone that can say is the correct order in which college players should be drafted. Comparing your own rankings to where players were actually picked is a flawed process because that assumes all the picks made were the correct ones. We consistently see players like Kawhi Leanord, Giannis Antetokounmpo, and Rudy Gobert (drafted 15, 15, and 27, respectively) come out of the draft and highly outperform players that were taken ahead of them. A statistical model will also never capture the emotional intelligence, work ethic, and mental understanding of the game. Some things you just need an actual scout to go and watch the games. 
This process will attempt to predict the best performers in different areas of the game: shooting (true shooting percentage), playmaking (assist percentage), rebounding (rebound percentage), steals (steal percentage), and best shot blocker (block percentage). I will also be projecting an “all-encompassing” stat called Player Efficiency Rating (PER). Lastly, the target variable will be the draft pick itself. 
Rookie seasons are generally sporadic and don ‘t capture what the players can develop into in the future, but there is value in understanding who has the potential to become an immediate contributor. Generally, the best players end up being better from the get go.

### Models
Four different models were trained with the same feature for the two set of target statistics: ridge, lasso, stochastic gradient descent, and random forest. The features used are made up of NCAA counting stat averages (points, assists, rebounds, etc.), those same stats but normalized to per 36 minute figures, advanced percentage statistics (true shooting %, assist %, etc.), a few all-encompassing stats (‘per’, ‘win shares’,) several features that are just two counting stats multiplied together. For the rookie year projections, data from rookie seasons from the 2003-04 to the 2015-2016 seasons were used to train the data. The predictions were tested against rookies from the 2016-2017 season and then applied to predict the target variable for the 2018 draft class. 
I tuned each of the 4 models using a grid search on a few of their respective parameters. You can find the details in my [Models Notebook](https://github.com/KaanME/NBA-Draft-Model/blob/master/Models.ipynb). Figure 5 shows the r-squared value that each of the four models came up with for each of the statistics we were looking at. 
 
In Figure 5 we can see that the highest R-squared values came from rebound percentage, assist percentage, and block percentage. These results match up with the correlation we saw in the scatter plots in the Figure 2. The bolded numbers in Figure 5 show the model we will be using for each statistic.

<p align="center"> 
<img src="/assets/r-squared.png">
<p align="center"><b> Figure 5: R-squared values for Rookie Season Projections By Model by Stat</b>
</p>


#### True Shooting Percentage
True Shooting percentage had the lowest R-squared value among all the stats at .102, meaning the features we chose don’t do a good job of explaining the variance in this statistic. The mean squared error we see in the true shooting percentage for the test set is roughly 20%. A 20% swing in true shooting percentage can be quite a large improvement or a huge decline for any given player. Figure 6 shows the top 10 projected players in true shooting for last years draft class.

<p align="center"> 
<img src="/assets/ts_pctTest.png">
<p align="center"><b> Figure 6: Projected True Shooting Percentage 2017 Rookie Class</b>
</p>
 
We can see players like John Collins and Zach Collins, both big men who can shoot, appearing on the top of this list. The null values appear for players who didn’t play in their rookie years. Rim-bound big-men with lower usage like Jordan Bell and Bam Adebayo appear here as well since a large percentage of their shot are dunks and layups. This makes their true shooting higher than guards or wings whose shot profile can be more difficult. Applying this to this years draft class, we limited the player pool to players who averaged 5 or more  field goal attempts a game. If a big man shoots 70% on 2 attempts a game, he might rise to the top of this list even though he might not be a legitimate draft candidate. 

<p align="center"> 
<img src="/assets/ts_pctHold.png">
<p align="center"><b> Figure 7: Projected True Shooting Percentage 2018 Rookie Class</b>
</p>

We can see in Figure 6 the 2018 draft class true shooting percentage projections. The top 4 players on the list were drafted 4th, 1st, 7th, and 2nd, respectively. Jaren Jackson, Ayton, and Wendell Carter are all big men who can play near the basket and also knock down the occasional 3 pointer. It makes sense that they would project to be at the top of an scoring effiency projection.

#### Assist Percentage
Assist percentage was best estimated using a random forest regressor. The R-squared value for this metric was .415 and the average error came out to be 4.5%. The results for last years draft can be seen in Figure 8. We can see that when applied 2017 rookies, pass first point guards like Juwan Evans and Lonzo Ball jump to the top of the list. One thing to note on this list, 4 of the top 9 picks in the draft are all in the top 5 in projected rookie assist percentage (Lonzo Ball-2, Dennis Smith-9, De'Aaron Fox-5, Markell Fultz-1). Also, the lowest lever of play any of these guys reached is a 2-way contract with an NBA team, which shows that point guard play was a theme for success in that class.

<p align="center"> 
<img src="/assets/ast_pctTest.png">
<p align="center"><b> Figure 8: Projected Assist Percentage 2017 Rookie Class</b>
</p>

The 2018 class had one transendent passer throughout the season, and that was Trae Young. We can see in Figure 9that he has risen to the top of this list with a projected rookie assist percentage of 29.6. At the time of writing this, he is 8th in the entire NBA at 34.4% of his possessions ending in an assist. Jevon Carter and Devonte Graham are 2 other names that stick out in this top 10 as NBA players that are a bit lower in the rotation of their respective teams. 

<p align="center"> 
<img src="/assets/ast_pctHold.png">
<p align="center"><b> Figure 9: Projected Assist Percentage 2018 Rookie Class</b>
</p>


#### Rebound Percentage
Rebound percentage had the 3rd highest R-squared value of the statitics at .288 with an average error of 4%.  Looking at rebound percentage for both the 2017 and 2018 classes, we can start to see a contrast between the two years. We saw a mixture of stretch big men and gueards in the top 10 for true shooting percentage and an inceredibly strong top 10 in assist percentage for the 2017 draft class. The rebound percentage for that class is noticeably weaker. Looking at Figure 10, while players like Caleb Swanigan and John Collins are solid NBA players, they don't have the star potential that the 2018 rebound percentage leaders have. Even a wing like Josh Jackson snuck in the top 10, which shows that in terms of rebounding in the NBA, the 2017 class would not produce much. 

<p align="center"> 
<img src="/assets/reb_pctTest.png">
<p align="center"><b> Figure 10: Projected Rebound Percentage 2017 Rookie Class</b>
</p>

The 2018 class is a different story. Just looking at the projections, we can see that the 9th best guy in 2018 would rank 4th in 2017. The top 3 guys in Figure 11 all were drafted in the top 7 of the 2018 draft, and Mohamed Bamba was drafted 6th. These rankings tell us that the 2018 draft class was filled with great rebounder that were also great overall players, and we will see that even more when we look at the player efficiency projections.

<p align="center"> 
<img src="/assets/reb_pctHold.png">
<p align="center"><b> Figure 11: Projected Rebound Percentage 2018 Rookie Class</b>
</p>



#### PER Percentage
Player Efficiency Rating, or PER, is an all encompassing, per minute statistic that John Hollinger came up with in the early 2000's. The league average PER is alway at 15.0, the positive statistics add to the number while the negative statistics like turnovers subtract from it. The Lasso regression performed best in terms of the R-squared value for the rookie years of the 2017 draft class. In Figure 12 we see that The efficient shooting, high rebound percentage big men duo of John and Zach Collins appear at the top of the list. John Collins outperformed his projection which Zach underperformed, although he is currently having a nice start to his sophomore season through 7 games. We also see multifaceted, lengthy point guards like Lonzo Ball and Markelle Fultz project to be top 5 in PER for their class. 

<p align="center"> 
<img src="/assets/perTest.png">
<p align="center"><b> Figure 12: Projected Per Percentage 2017 Rookie Class</b>
</p>

figure 13 shows us how the 2018 class is projected to perform in PER. The top 4 spots are the same players that led the way in true shooting percentage. This time, Trae Young also slides into the top 10, as his playmaking abilities and long range shooting prowess work in favor of him having a high efficiency rating. There is more of a mix of big men and guards in this metric becuase there is more than one way to rack of stats. One thing to note overall however, is that none of the rookies in either class project to be an above average player in terms of PER. This tells us that even the best rookies struggle to make a positive impact for their teams right out of the college.

<p align="center"> 
<img src="/assets/perHold.png">
<p align="center"><b> Figure 13: Projected Per Percentage 2018 Rookie Class</b>
</p>

#### Projecting Pick
The final step in this process is to project where each player will be selected. The same process was used to project the pick as the other metrics, but the players actual draft pick was used as the target variable. The ridge regression model provided the highest R-squared value at .553, which was also the highest number among all the statistics we looked at. To understand what factors were most prominent in projecting drafting pick, take a look at Figure 14. This table shows the top 10 features with the highest regression coefficients when modeling draft pick. The top 3 factors are all related to how old the player is. This tells us that teams value the ability to train and develop players from a younger age, and supports the stories we explored in the Data Exploration section. As far as on the court statistics, getting to the line and hitting free throws are important as free throw percentage (ft_pct) and free throw rate (ft_fga) are both in the top 3 after age related features. Rebounding, 3 points attempted, and steal to turnover ration (stl_to) round out the top ten. There is a solid mix of big man and guard oriented skills in the table.

<p align="center"> 
<img src="/assets/pickfts.png">
<p align="center"><b> Figure 14: Top 10 Feaures for Projecting Draft Position</b>
</p>

Applying the model to the 2017 draft class, Lonzo Ball ranks as the number 1 prospect. Ball is an all around talent who can shoot, rebound, pass, and play defense. He pushed UCLA to a top ranked offense, was picked #2 in the real draft. A few surprises in the top 15 do stand out. Numbers 5 and 6 on this list are T.J. Leaf and Justin Patton. Both were picked just outside the lottery, and neither produced much in there rookie years. Justin Patton was sidelined with a foot injury, so who know what could've been, but T.J. Leaf is a three point shooting big man who doesn't do much else in the NBA. His athletic limitation didn't hurt him as much in college, which is most likely why he ranks so high in this model. Lauri Markkanen also fits the same player archetype as T.J. Leaf, but he has shown to be much more athletic and versatile in his rookie year. He was selected to the All-Rookie First Team, so it is encouraging that the model ranks him so highly. The biggest miss of the model has to be the exclusion of Donovan Mitchell in the top 15. He comes in at 25 in the model, but was quite easily a top 3 rookie last year. Being a Junior coming out of college really hurt his stock in the model, as well as his undeveloped shooting efficiency. There are always statistical anomalies, and that is where scouting and the "eye-test" come into play.

<p align="center"> 
<img src="/assets/pickTest.png">
<p align="center"><b> Figure 15: Projected Pick 2017 Rookie Class</b>
</p>

For the 2018 class, there is nothing to compare the ranking to besides where they were actually selected in the draft, and my own subjective evaluation of the players. The final results show the models first three picks align with who the Suns, Kings, and Hawks selected in the actual draft. The top rated rebounders and true shooting percentage leaders make up 5 of the top 6 projected picks here. Udoka Azubuike did not enter the draft and returned to college for another year, so keeping an eye on his performance this year and how he ranks against the new batch of college Freshman will be interesting. With age being so important in this model, staying for one more year could see him fall, same story applies to Jontay Porter (who incidentally tore his ACL and MCL before the start of the 18-19 season) and Ja Morant. A couple more noteworthy players in this top 15 are Zhaire Smith and Mikal Bridges. Mikal was selected 10th overall by Philadelphia, Zhaire fell to 16 to the Suns, but the Suns offered a 1st round pick and Zhaire to Philly for Mikal. In this model, Zhaire ranks higher than Mikal. These types of decision make or break careers, and if Zhaire Smith turns out to have a better first couple years than Mikal Bridges, the trade decision by the Suns will look awful, while Philly could come out with the better player AND an extra pick. 

<p align="center"> 
<img src="/assets/pickHold.png">
<p align="center"><b> Figure 16 : Projected Pick 2018 Rookie Class</b>
</p>


## Limitations 

This analysis only takes into consideration players who played in the NCAA and went on to play professionally elsewhere. Any college player who ended there career there was not included. International players were also not included in this analysis. The statistical profiles of players who were drafted before 2003 were not used for this analysis either. The college data for players that played before the 2017-18 season only included those who ended up playing professionally somewhere, while everyone who played in a Division 1 school last season was included. The accuracy of the projection for players from last year obviously could not be computed becuase they haven't played a season in the NBA yet. This limits our ability to understand how well the model is performing until long after the pick is actually made. This is the challenge for NBA Front Offices, and the same challenges apply here.

## Next Steps

The next steps to this analysis will come in a variety of methods. First, international players must be added to the pool of draftable players. Complications arise with international players because of the fact that the level of competition in professional leagues overseas is much higher than college basketball here in the U.S. Clustering players and then projecting there stats could make for more accurate predictions for each metric. Factoring in college seasons before there final year would provide more information about older players. If a guy improves every year, he's probably more likely to improve beyond college versus a guy with great stats but stays steady all 3 or 4 years. Model other all encompassing statistics like Real Plus Minus (RPM), Box Plus Minus (BOM), and combine them into one metric that ranks all players. Apply play by play data to the model to get more granular information about a plyayer and understand what kind of plays lead to more successful NBA players. All of these steps will be taken one by one.

## Conclusion

The unpredictability of a players emotional intelligence, his worth ethic, and off the court influences can play a huge role in how good a player can become. This model starts to tell part of the story, and maybe a significant portion of the story, through the statistical profile of NBA prospects. The entire story can not be told without in person scouting, interviews, and background checks. "Feel for the game" is also extremely hard to quantify, but can lead to a statistically average player to have a long and successful career. We did learn a few things about the historical nature of the draft. Younger players are more desirable to NBA teams because they have more time to develop within an NBA training program in NBA facilities. There are certain stats that carry over more successfully from college to the pros than others, such as rebounding and steals. This could be attributed to rebounding and stealing the ball being more effort oriented, and if you have a high motor in college, you will probably have a high motor in the NBA as well (or maybe in the case of rebounding, if your tall, your going to stay tall). Many follow up items will come from this project, but this gives us a solid base to understand who the best players in each class are. Nailing the second round picks is where things will get trickier.





