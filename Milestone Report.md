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


