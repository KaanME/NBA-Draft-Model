# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 16:46:01 2018

@author: kerel
"""
#%%
#Import packages
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
import matplotlib.style as style
pd.set_option('display.max_columns', 500)
%matplotlib inline
style.use('fivethirtyeight')


nba = pd.read_csv('nba_stats_info2.csv', index_col = 0)
ncaa = pd.read_csv('ncaa_stats_info.csv', index_col = 0)

grades = []
for x in ncaa_to_nba_stats_info.grade:
    if x in ('Fr','RS-Fr'):
        grades.append(1)
    elif x in ('So','RS-So'):
        grades.append(2)
    elif x in ('Jr','RS-Jr'):
        grades.append(3)
    else:
        grades.append(4)
        
ncaa_to_nba_stats_info.grade = grades

#filter nba data for players who played at least 15 games in a season
nba_played = nba_stats_info.loc[nba_stats_info.gp >= 0]

#filter college data for players who played at least 10 games in a season
ncaa_played = ncaa_to_nba_stats_info.loc[ncaa_to_nba_stats_info.gp >= 0]

#get rookie nba seasons
rookie_stats = nba_played.loc[nba_played.season_count == 1]

#get last college season
last_college_stats = ncaa_played.groupby('name').last()

print(len(rookie_stats),len(last_college_stats))

#%%

rook_pts = pd.merge(last_college_stats[['id','pts']], 
                    rookie_stats[['name','pts','id']], on = 'id')

plt.scatter(rook_pts.pts_x, rook_pts.pts_y)

def rook_stats(stat):
    stat = pd.merge(last_college_stats[['id',stat]], 
                    rookie_stats[['name',stat,'id']], on = 'id')
    return stat

rook_reb = rook_stats('reb')
plt.scatter(rook_reb.reb_x, rook_reb.reb_y)

def rook_plot(stat):
    stats = rook_stats(stat)
    plt.scatter(stats[stat+'_x'], stats[stat+'_y'])
    
rook_plot('ast')
rook_plot('blk_pct')

plt.hist(last_college_stats.reb, bins = 20)
plt.hist(rookie_stats.reb, bins = 20)

rookie_stats.pos.unique()

rook_ff = rookie_stats[['name','gp','ff','usg_pct']].loc[rookie_stats.gp>=20]

##FOUR FACTORS WITH ASSISTS AND USAGE
##DEFENSIVE ALL IN ONE
##BUILD FLEXIBLE MODEL FOR ALL INDIVIDUAL STATS,THEN COMBINE
#%%
#%%
#%%
#%%
#%%
#%%
#%%
#%%
#%%
#%%
#%%
#%%
#%%
#%%
#%%
#%%
#%%
#%%
#%%
#%%
#%%
