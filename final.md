# NBA Draft Model
## Introduction

As data becomes more and more an integral part of how decisions are made throughout a variety of industries, sports teams have also come around to the idea of data science as a tool. Several NBA teams have shifted their focus more and more towards being analytics driven organizations. There are many different ways that data can be collected, analyzed, and applied within the basketball world. Box score statistics have been around since the game itself started, which led the way to more advanced statistics such as looking at efficiency ratings by looking at the stats on a per minute or per possession basis. More recently, companies like Second Spectrum and Synergy have started player tracking, where the datasets contain x, y, and z coordinates for each player and the ball. The amount of insights that can be obtained through all this data has created an exciting period in the world of basketball.
For the purposes of this paper, advance statistics of College and NBA players will be used in order to create a model that ranks college prospects trying to get drafted into the NBA. By looking at historical data about how statistical profiles in college translate to the NBA, as well as physical measurement, an exclusively numbers based model can help in the crucial decision process that is the NBA draft. As player tracking companies start moving into college arenas, this process will also continue to improve in its sophistication.

## Data Acquisition and Cleaning
I initially wanted to scrape the NCAA website and combine it with the NBA game log data set I had created for my NBA fantasy score model. I found the [NCAAB Stats Scraper](https://github.com/rodzam/ncaab-stats-scraper) repository on Github and started digging through it.  Some of the links and python functions were out dated, so I cleaned it up and made sure it walked through every game box score for each NCAA season dating back to 2003-04. I successfully scraped the data and now face the task of matching up all the players by name to the NBA data set I had.
Around this time, I found about Will Schreefer's "draft-toolkit". It contains box score stats, advanced stats, and physical measurements  for all college, NBA, G-League, Summer League, and International players dating back to the 2003-04 season. Most of the data was pulled from RealGM.com, and I decided to use this database instead because the players were already linked by a player key. However, to build a draft model, I also needed historical draft data. I found a dataset on Kaggle, [NBA Draft Data](https://www.kaggle.com/pmp5kh/nba-draft-19802017), where it gives me the players name, the draft year, and what pick they were drafted. From there I cleaned up the names to make them match with the draft toolkit. The following [Data Cleaning](https://github.com/KaanME/NBA-Draft-Model/blob/master/data_cleaning.py) notebook shows the process by which I did that.

## Data Exploration
In order to understand which variables perform the best at predicting future NBA success and draft position, I split the data into 2 sets. The first set contains the final college season stats of all NCAA players that went on to be drafted. The second dataset contains the rookie season stats of every NBA players. From there, I compared the college averages of certain stats to the stats of the same player in there rookie season. I also looked at how age playes a role in where a player gets selected. 

### Where AreCollege Players Going After Graduation?

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




## Limitations 

This analysis only takes into consideration players who played in the NCAA and went on to play professionally elsewhere. Any college player who ended there career there was not included. International player were also not included in this analysis. The statistical profiles of players who were drafted before 2003 were not used for this analysis either. 

## Next Steps

A few steps will follow as the project moves towards the modelling stage. I will create more features, such as per 36 minutes statistics, as well as features that are just 2 stats multiplied together. The best scorers, rebounders, and playmakers will be projected, as well as a few all encompassing statistics. Rookie year and third year stats will be modelled.
