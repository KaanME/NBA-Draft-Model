# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 17:00:48 2018

@author: Kaan
"""

import numpy as np
import pandas as pd
import os
import re

#%%

directory = os.fsencode('draft_toolkit')
csv_names = ['pbp','sports247','pbp_extra','gl','logs','netRtg','intl','jhoy_measures',
        'luck_netRtg','measures','nba','ncaa','plyr_info','rgm_bpm','rsci','spref_bpm','sl']

csv_dict = {}
for file, name in zip(os.listdir(directory),csv_names):
    print(file,name)
    filename = os.fsdecode(file)
    csv_dict[name] = pd.read_csv('draft_toolkit/' + filename)

#%%
        
logs = csv_dict['logs']
plyr_info = csv_dict['plyr_info']
measures = csv_dict['measures']
intl = csv_dict['intl']
ncaa = csv_dict['ncaa']
sl = csv_dict['sl']
gl = csv_dict['gl']
nba = csv_dict['nba']


#%%
def ff_score(efg_pct, tov_pct, oreb_pct, ftr):
    ff = .4*efg_pct + .25*tov_pct + .20*oreb_pct + .15* ftr
    return ff



def remove_null_rows(data):
    for i in data:
        data[i] = [np.nan if x == '-' else x for x in data[i]]
    return data
    
remove_null_rows(ncaa)
ncaa = ncaa.dropna(thresh = 15)


ncaa.isnull().sum()
def to_num(data):
    for i in data:
        try:
            data[i] = pd.to_numeric(data[i])
        except:
            print(i)
    return data

to_num(ncaa)

data_list = [intl, ncaa, sl, gl,nba]
for d in data_list:
    remove_null_rows(d)
    to_num(d)
    d['ff'] = [ff_score(efg_pct, tov_pct, oreb_pct, ftr) for efg_pct, tov_pct, oreb_pct, ftr in zip(d.efg_pct, d.tov_pct, d.oreb_pct, d.ft_fga)]
#%%#%%
nba['year'] = [int(x[:4]) for x in nba.season]
ncaa['year'] = [int(x[:4]) for x in ncaa.season]
nba['season_count'] = nba.groupby(['realgm_summary_page']).cumcount()+1
ncaa['season_count'] = ncaa.groupby(['realgm_summary_page']).cumcount()+1
#%%
mismatched = []
matched = []

for p in ncaa.loc[ncaa.highest_level_reached == 'NBA'].realgm_summary_page.unique():
    if p not in list(nba.realgm_summary_page):
        mismatched.append(p)
    else:
        matched.append(p)
     
ncaa_stats_info = ncaa.merge(plyr_info, left_on = 'realgm_summary_page', right_on = 'realgm_link')
nba_stats_info = nba.merge(plyr_info, how = 'inner', left_on = 'realgm_summary_page', right_on = 'realgm_link')

ncaa_to_nba_stats_info = ncaa_stats_info.loc[ncaa_stats_info.name.isin(matched)]

nba_stats_info.to_csv('nba_stats_info.csv')
ncaa_to_nba_stats_info.to_csv('ncaa_to_nba_stats.csv')

#%%
draft = pd.read_csv('NBA_Draft_1980_2017.tsv', sep ='\t')

draft_03_17 = draft.loc[(draft.year >= 2003) & (draft.year<2018)]


draft_names = []
for x in draft_03_17.player:
        try:
            draft_names.append(x.split(', ')[1] + ' ' + x.split(', ')[0])
        except:
            draft_names.append(x)
#%%
mismatched = []
matched = []

for p in nba_stats_info.name.unique():
    if p not in draft_names:
        mismatched.append(p)
    else:
        matched.append(p)
            

#%%
import unidecode

nba_pl = sorted(nba_stats_info.name.unique())
clean_names = sorted(draft_names)
#strips all punctuation from a name
def alpha(name):
    return ("".join(re.findall("[a-zA-Z]+", name)))

#list of nba players with only alphanumeric characters
alphanba = [alpha(x) for x in nba_pl]

#given a name, return name in the nba player list if all alpha numeric characters match in order
def matchalpha(name):
    #uses stipped nba list, the list of unique names, an the alpha function
    global alphanba, nba_pl, alpha
    
    #if stripped version of name is in nba list, return the formatting from the nba list
    if alpha(name) in alphanba:
        return nba_pl[alphanba.index(alpha(name))]   
    
    #if no match just return the name as is
    return name

#strip suffixes from the nba names and put them into a list
nosuffixnba = [x.strip(' II') for x in nba_pl]
nosuffixnba = [x.strip(' III') for x in nosuffixnba]
nosuffixnba = [x.strip(' Jr.') for x in nosuffixnba]

#function that returns NBA formatted player name if all but the suffix match
def matchnosuffix(name):
    #uses a list of nba names stripped of their suffixes
    global nosuffixnba
    nosuffix = name.strip(' II')
    nosuffix = nosuffix.strip(' III')
    nosuffix = nosuffix.strip(' Jr.')
    if nosuffix in nosuffixnba:
        return nba_pl[nosuffixnba.index(nosuffix)]
    return name

clean_names = [unidecode.unidecode(x) for x in clean_names]
clean_names = [matchalpha(name) for name in clean_names]
clean_names = [matchnosuffix(name) for name in clean_names]
#clean_names = [new_names[name] if name in new_names else name for name in plyr_info.name]
  


#%%
mismatched = []
matched = []

for p in nba_stats_info.name.unique():
    if p not in clean_names:
        mismatched.append(p)
    else:
        matched.append(p)
            

new_names = {'Rafael Araujo':'Babby Araujo','Domantas Sabonis':'Domas Sabonis',
             'Michael Sweetney':'Mike Sweetney',
             'OG Anunoby':'Ogugua Anunoby', 'Jr. Ewing':'Pat Ewing','Poeltl':'Jakob Poeltl',
             'Javale McGee':'JaVale McGee.','Wes Iwundu':'Wesley Iwundu','Zhou Qi,':'Zhou Qi'}


clean_names = [new_names[name] if name in new_names else name for name in clean_names]

draft_names = [unidecode.unidecode(x) for x in draft_names]
draft_names = [matchalpha(name) for name in draft_names]
draft_names = [matchnosuffix(name) for name in draft_names]
draft_names = [new_names[name] if name in new_names else name for name in draft_names]

draft_03_17.player = draft_names
#%%

#%%
ncaa_stats_info2 = ncaa_stats_info.merge(draft_03_17[['year','pick','player']], how = 'left', left_on = 'name', right_on = 'player')
ncaa_stats_info2.drop('player',1, inplace = True)
ncaa_stats_info2.rename(columns={'year_x':'year', 'year_y':'draft_year'}, inplace = True)
ncaa_stats_info2.pick.fillna(99, inplace = True)

nba_stats_info2 = nba_stats_info.merge(draft_03_17[['year','pick','player']],  how = 'left',left_on = 'name', right_on = 'player')
nba_stats_info2.drop('player',1, inplace = True)
nba_stats_info2.rename(columns={'year_x':'year', 'year_y':'draft_year'}, inplace = True)
nba_stats_info2.pick.fillna(99, inplace = True)


#%%

pd.to_datetime(nba_stats_info2.bday[0])
timed = (pd.to_datetime(str(int(nba_stats_info2.year[0])) + '-10-01') - pd.to_datetime(nba_stats_info2.bday[0]))
timed.days / 365.0


def calculate_age(born, year):
    try:    
        szn_start = str(int(year))+'-10-01'
        age_days = pd.to_datetime(szn_start) - pd.to_datetime(born)
        age_years = age_days.days/365.0
    except:
        return np.nan
    return age_years

nba_stats_info2['age'] = [calculate_age(born, year) for born,year in zip(nba_stats_info2.bday,nba_stats_info2.year)]
ncaa_stats_info2['age'] = [calculate_age(born, year) for born,year in zip(ncaa_stats_info2.bday,ncaa_stats_info2.year)]

nba_stats_info2['draft_age'] = [calculate_age(born, year) for born,year in zip(nba_stats_info2.bday,nba_stats_info2.draft_year)]
ncaa_stats_info2['draft_age'] = [calculate_age(born, year) for born,year in zip(ncaa_stats_info2.bday,ncaa_stats_info2.draft_year)]
#%%
cols_w_nulls = []
for col in nba_stats_info2:
    if nba_stats_info2[col].isnull().sum() > 0:
        cols_w_nulls.append(col)
cols_w_nulls

stats_w_nulls = [ 'ows','dws', 'ws', 'oreb_pct', 'dreb_pct', 'reb_pct', 'ast_pct', 
                 'tov_pct', 'stl_pct', 'blk_pct', 'usg_pct', 'ppr', 'ortg', 'per', 'ff']

for s in stats_w_nulls:
    nba_stats_info2[s].fillna(0,inplace=True)
    ncaa_stats_info2[s].fillna(0, inplace=True)
    
#%%
nba_stats_info2.to_csv('nba_stats_info2.csv')
ncaa_stats_info2.to_csv('ncaa_stats_info2.csv')
#%%
#%%
#%%
#%%
#%%

plyr_logs = pd.read_csv('player_logs_corrected.csv', index_col=0)


ncaa.columns

plyr_logs.columns

avg_cols = ['mp','fgm', 'fga', 'fg_pct', 'fg3m', 'fg3a', 'fg3_pct', 'ftm', 'fta',
       'ft_pct', 'oreb', 'dreb', 'reb', 'ast', 'stl', 'blk', 'pf', 'tov', 'pts',]

tot_cols = ['mp_tot', 'fgm_tot', 'fga_tot', 'fg3m_tot', 'fg3a_tot',
       'ftm_tot', 'fta_tot', 'oreb_tot', 'dreb_tot', 'reb_tot', 'ast_tot',
       'stl_tot', 'blk_tot', 'pf_tot', 'tov_tot', 'pts_tot']

adv_cols = ['ts_pct', 'efg_pct', 'oreb_pct', 'dreb_pct', 'reb_pct', 'ast_pct', 'tov_pct',
            'stl_pct', 'blk_pct', 'usg_pct']

nba = pd.DataFrame()
 

plyr_avgs = plyr_logs.groupby(['player_name','season']).mean().reset_index()
plyr_tot = plyr_logs.groupby(['player_name','season']).sum().reset_index()

nba['name'] = plyr_avgs.player_name
nba['season'] = plyr_avgs.season
nba['gp'] = plyr_logs.groupby(['player_name','season']).game_count.max().reset_index().game_count
for col in avg_cols:
    nba[col] = plyr_avgs[col]

for col in tot_cols:
    nba[col] = plyr_tot[col[:-4]]
    
for col in adv_cols:
    nba[col] = plyr_avgs[col]
    
def dblcount(pts,reb,ast,stl,blk):
    #counts the number of core stats that are greater than 10
    dbls = sum(x>=10 for x in [pts,ast,reb,stl,blk])
    
    #if double double, ad 1.5pts
    if dbls == 2:
        return 1
    #if triple double or more, 4.5pts
    elif dbls >= 3:
        return 2
    else:
        return 0

dblcnt = np.array([dblcount(p,a,r,s,b) for p,a,r,s,b in zip(plyr_logs.pts, plyr_logs.ast, plyr_logs.reb, plyr_logs.stl, plyr_logs.blk)])
plyr_logs['dbl_dbl'] = [1 if i>0 else 0 for i in dblcnt]
plyr_logs['tpl_dbl'] = [1 if i==2 else 0 for i in dblcnt]
plyr_logs['pts40'] = [1 if i >= 40 else 0 for i in plyr_logs.pts]
plyr_logs['pts20'] = [1 if i >= 20 else 0 for i in plyr_logs.pts]
plyr_logs['ast20'] = [1 if i >= 20 else 0 for i in plyr_logs.pts]

nba['dbl_dbl'] = plyr_logs.groupby(['player_name','season']).sum().reset_index().dbl_dbl
nba['tpl_dbl'] = plyr_logs.groupby(['player_name','season']).sum().reset_index().tpl_dbl
nba['pts40'] = plyr_logs.groupby(['player_name','season']).sum().reset_index().pts40
nba['pts20'] = plyr_logs.groupby(['player_name','season']).sum().reset_index().pts20
nba['ast20'] = plyr_logs.groupby(['player_name','season']).sum().reset_index().ast20
nba['ast_to'] = nba.ast_tot / nba.tov_tot
nba['stl_to'] = nba.stl_tot / nba.tov_tot
nba['ft_fga'] = nba.fta_tot / nba.fga_tot
nba['ff'] = [ff_score(efg_pct, tov_pct, oreb_pct, ftr) for efg_pct, tov_pct, oreb_pct, ftr in zip(nba.efg_pct, nba.tov_pct, nba.oreb_pct, nba.ft_fga)]
nba['season_count'] = nba.groupby(['name']).cumcount()+1

   

#%%

ncaa_to_nba =  plyr_info.loc[(plyr_info.highest_level =='NBA')] 

#sorted list of all unique players in each dataset
nba_pl = sorted([x for x in nba.name.unique()])
ncaa_pl = sorted([x for x in ncaa_to_nba.name.unique()])

#create a 2 column dataframe from the unique players
mismatch = pd.DataFrame([[p for p in nba_pl if p not in ncaa_pl],[p for p in ncaa_pl if p not in nba_pl]]).T
#name the columns
mismatch.columns = ['nba','ncaa']


#Print the number of NBA players that arent matched with dk players
print(len([x for x in mismatch.ncaa if x != None]))


#strips all punctuation from a name
def alpha(name):
    return ("".join(re.findall("[a-zA-Z]+", name)))

#list of nba players with only alphanumeric characters
alphanba = [alpha(x) for x in nba_pl]

#given a name, return name in the nba player list if all alpha numeric characters match in order
def matchalpha(name):
    #uses stipped nba list, the list of unique names, an the alpha function
    global alphanba, nba_pl, alpha
    
    #if stripped version of name is in nba list, return the formatting from the nba list
    if alpha(name) in alphanba:
        return nba_pl[alphanba.index(alpha(name))]   
    
    #if no match just return the name as is
    return name

#strip suffixes from the nba names and put them into a list
nosuffixnba = [x.strip(' II') for x in nba_pl]
nosuffixnba = [x.strip(' III') for x in nosuffixnba]
nosuffixnba = [x.strip(' Jr.') for x in nosuffixnba]

#function that returns NBA formatted player name if all but the suffix match
def matchnosuffix(name):
    #uses a list of nba names stripped of their suffixes
    global nosuffixnba
    nosuffix = name.strip(' II')
    nosuffix = nosuffix.strip(' III')
    nosuffix = nosuffix.strip(' Jr.')
    if nosuffix in nosuffixnba:
        return nba_pl[nosuffixnba.index(nosuffix)]
    return name


#%%
    #use match alpha function to replace some of the mismatching names
ncaa_pl = [matchalpha(name) for name in ncaa_pl]

#see differences in the player lists after replacing
mismatch = pd.DataFrame([[p for p in nba_pl if p not in ncaa_pl],[p for p in ncaa_pl if p not in nba_pl]]).T
mismatch.columns = ['nba','ncaa']
print('# unmatched NBA names', len([x for x in mismatch.ncaa if x != None]))
#%%
ncaa_pl = [matchnosuffix(name) for name in ncaa_pl]

mismatch = pd.DataFrame([[p for p in nba_pl if p not in ncaa_pl],[p for p in ncaa_pl if p not in nba_pl]]).T
mismatch.columns = ['nba','ncaa']
print('# unmatched NBA names', len([x for x in mismatch.ncaa if x != None]))
#%%
new_names = {'Babby Araujo':'Rafael Araujo','Domas Sabonis':'Domantas Sabonis','Jake Wiley':'Jacob Wiley',
             'James McAdoo':'James Michael McAdoo','Joshia Gray':'Josh Gray','Matt Dellavedova':'Matthew Dellavedova','Mike Sweetney':'Michael Sweetney',
             'Naz Long':'Naz Mitrou-Long','Ogugua Anunoby':'OG Anunoby', 'Pat Ewing':'Patrick Ewing','Squeaky Johnson':'Carldell Johnson',
             'Vince Hunter':'Vincent Hunter','Walt Lemon, Jr.':'Walter Lemon Jr.','Wesley Iwundu':'Wes Iwundu'}
ncaa_pl = [new_names[name] if name in new_names else name for name in ncaa_pl]
mismatch = pd.DataFrame([[p for p in nba_pl if p not in ncaa_pl],[p for p in ncaa_pl if p not in nba_pl]]).T
mismatch.columns = ['nba','ncaa']
print('# unmatched NBA names', len([x for x in mismatch.ncaa if x != None]))
#%%
plyr_info.name = [matchalpha(name) for name in plyr_info.name]
plyr_info.name = [matchnosuffix(name) for name in plyr_info.name]
plyr_info.name = [new_names[name] if name in new_names else name for name in plyr_info.name]
ncaa_to_nba_info =  plyr_info.loc[(plyr_info.highest_level =='NBA')]    
#%%
mismatched = []
matched = []

for p in ncaa_to_nba.name.unique():
    if p not in list(plyr_info.name):
        mismatched.append(p)
    else:
        matched.append(p)
     
nba_matched = nba.loc[nba.name.isin(matched)]
ncaa_to_nba_info = ncaa_to_nba.loc[ncaa_to_nba.name.isin(matched)]


#ncaa_to_nba.to_csv('ncaa_to_nba_info.csv')
#nba_matched.to_csv('nba_matched.csv') 
#%%
ncaa_stats_info = ncaa.merge(plyr_info, left_on = 'realgm_summary_page', right_on = 'realgm_link')
nba_stats_info = nba_matched.merge(ncaa_to_nba_info, how = 'inner', on = 'name')
len(nba_stats_info.drop_duplicates())
nba_stats_info.isnull().sum()
ncaa_to_nba_stats_info = ncaa_stats_info.loc[ncaa_stats_info.name.isin(matched)]
len(ncaa_to_nba_stats.name.unique())
#nba_stats_info.to_csv('nba_stats_info.csv')
#ncaa_to_nba_stats_info.to_csv('ncaa_to_nba_stats.csv')

#%%
temp = nba_stats_info[nba_stats_info[['name','season']].duplicated(keep = False)]
temp = nba_stats_info[['name']].merge(nba_matched[['name']],on='name')

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
#%%
#%%
#%%
#%%
#%%
#%%
#%%
