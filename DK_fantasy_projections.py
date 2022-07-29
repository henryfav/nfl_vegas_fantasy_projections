#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests as req
import numpy as np


# # Pass Yards

# In[2]:


pyards_url = 'https://sportsbook-us-co.draftkings.com//sites/US-CO-SB/api/v5/eventgroups/88808/categories/782/subcategories/7200?format=json'

response = req.get(pyards_url)
response.raise_for_status()
passyards = response.json()
rawdata = passyards['eventGroup']['offerCategories']
rawdata = rawdata[4]
rawdata = rawdata['offerSubcategoryDescriptors']
rawdata = rawdata[0]
rawdata = rawdata['offerSubcategory']
rawdata = rawdata['offers']
rawdata = rawdata[0]


# In[3]:


dfQB = pd.DataFrame()
pppassyard = 1/25

for total in rawdata: 
    player = ' '.join(total['label'].split(' ')[:2])
    dfQB.loc[player, 'Points'] = pppassyard * float(total['outcomes'][0]['label'].split()[1])
    dfQB.loc[player,'Has pass yards'] = True
    


# # Pass Touchdowns

# In[4]:


ptds_url = 'https://sportsbook-us-co.draftkings.com//sites/US-CO-SB/api/v5/eventgroups/88808/categories/782/subcategories/7199?format=json'


response = req.get(ptds_url)
response.raise_for_status()
passyards = response.json()
rawdata = passyards['eventGroup']['offerCategories']
rawdata = rawdata[4]
rawdata = rawdata['offerSubcategoryDescriptors']
rawdata = rawdata[1]
rawdata = rawdata['offerSubcategory']
rawdata = rawdata['offers']
rawdata = rawdata[0]


# In[5]:


pppasstd = 4

for total in rawdata:
    player = ' '.join(total['label'].split(' ')[:2])
    dfQB.loc[player, 'Points'] += pppasstd * float(total['outcomes'][0]['label'].split()[1])
    dfQB.loc[player,'Has pass TDs'] = True


# # Some RBs are offered rush + rec yards,
# # but not for individual categories

# In[6]:


rushrecyds_url = 'https://sportsbook-us-co.draftkings.com//sites/US-CO-SB/api/v5/eventgroups/88808/categories/782/subcategories/8415?format=json'

response = req.get(rushrecyds_url)
response.raise_for_status()
passyards = response.json()
rawdata = passyards['eventGroup']['offerCategories']
rawdata = rawdata[4]
rawdata = rawdata['offerSubcategoryDescriptors']
rawdata = rawdata[7]
rawdata = rawdata['offerSubcategory']
rawdata = rawdata['offers']
rawdata = rawdata[0]


# In[13]:


ppyd = .1

dfRB = pd.DataFrame()

for total in rawdata:
    player = ' '.join(total['label'].split(' ')[:2])
    dfRB.loc[player,'Points'] = ppyd * float(total['outcomes'][0]['label'].split()[1])
    dfRB.loc[player, 'Has Rush Yards'] = True
    dfRB.loc[player, 'Has Receiving Yards'] = True


# In[14]:


combined_rb = list(dfRB.index)


# # Rush yards

# In[15]:


rushyds_url = 'https://sportsbook-us-co.draftkings.com//sites/US-CO-SB/api/v5/eventgroups/88808/categories/782/subcategories/7277?format=json'

response = req.get(rushyds_url)
response.raise_for_status()
passyards = response.json()
rawdata = passyards['eventGroup']['offerCategories']
rawdata = rawdata[4]
rawdata = rawdata['offerSubcategoryDescriptors']
rawdata = rawdata[2]
rawdata = rawdata['offerSubcategory']
rawdata = rawdata['offers']
rawdata = rawdata[0]


# In[16]:


pprushyd = .1


for total in rawdata:
    player = ' '.join(total['label'].split(' ')[:2])
    if player in dfQB.index:
        dfQB.loc[player,'Points'] += pprushyd * float(total['outcomes'][0]['label'].split()[1])
        dfQB.loc[player, 'Has Rush Yards'] = True
    elif player not in combined_rb:
        dfRB.loc[player,'Points'] = pprushyd * float(total['outcomes'][0]['label'].split()[1])
        dfRB.loc[player, 'Has Rush Yards'] = True


# # Rush TDs

# In[17]:


rushtds_url = 'https://sportsbook-us-co.draftkings.com//sites/US-CO-SB/api/v5/eventgroups/88808/categories/782/subcategories/7694?format=json'


response = req.get(rushtds_url)
response.raise_for_status()
passyards = response.json()
rawdata = passyards['eventGroup']['offerCategories']
rawdata = rawdata[4]
rawdata = rawdata['offerSubcategoryDescriptors']
rawdata = rawdata[3]
rawdata = rawdata['offerSubcategory']
rawdata = rawdata['offers']
rawdata = rawdata[0]


# In[18]:


pprushtd = 6

for total in rawdata:
    player = ' '.join(total['label'].split(' ')[:2])
    if player in dfQB.index:
        dfQB.loc[player, 'Has Rush TD'] = True
        dfQB.loc[player,'Points'] += pprushtd * float(total['outcomes'][0]['label'].split()[1])
    elif player in dfRB.index:
        dfRB.loc[player, 'Has Rush TD'] = True
        dfRB.loc[player,'Points'] += pprushtd * float(total['outcomes'][0]['label'].split()[1])


# # Receiving Yards

# In[19]:


recyds_url = 'https://sportsbook-us-co.draftkings.com//sites/US-CO-SB/api/v5/eventgroups/88808/categories/782/subcategories/7276?format=json'

response = req.get(recyds_url)
response.raise_for_status()
passyards = response.json()
rawdata = passyards['eventGroup']['offerCategories']
rawdata = rawdata[4]
rawdata = rawdata['offerSubcategoryDescriptors']
rawdata = rawdata[4]
rawdata = rawdata['offerSubcategory']
rawdata = rawdata['offers']
rawdata = rawdata[0]


# In[20]:


pprecyd = .1

dfWR = pd.DataFrame()

for total in rawdata:
    player = ' '.join(total['label'].split(' ')[:2])
    if ((player in dfRB.index) and (player not in combined_rb)):
        dfRB.loc[player, 'Has Receiving Yards'] = True
        dfRB.loc[player,'Points'] += pprecyd * float(total['outcomes'][0]['label'].split()[1])    
    else:
        dfWR.loc[player, 'Has Receiving Yards'] = True
        dfWR.loc[player,'Points'] = pprecyd * float(total['outcomes'][0]['label'].split()[1])    


# # Receiving Touchdowns

# In[21]:


rectds_url = 'https://sportsbook-us-co.draftkings.com//sites/US-CO-SB/api/v5/eventgroups/88808/categories/782/subcategories/7239?format=json'

response = req.get(rectds_url)
response.raise_for_status()
passyards = response.json()
rawdata = passyards['eventGroup']['offerCategories']
rawdata = rawdata[4]
rawdata = rawdata['offerSubcategoryDescriptors']
rawdata = rawdata[5]
rawdata = rawdata['offerSubcategory']
rawdata = rawdata['offers']
rawdata = rawdata[0]


# In[22]:


pprectd = 6

for total in rawdata:
    player = ' '.join(total['label'].split(' ')[:2])
    if player in dfRB.index:
        dfRB.loc[player,'Points'] += pprectd * float(total['outcomes'][0]['label'].split()[1]) 
        dfRB.loc[player, 'Has Receiving TD'] = True
    elif player in dfWR:
        dfWR.loc[player, 'Has Receiving TD'] = True
        dfWR.loc[player,'Points'] += pprectd * float(total['outcomes'][0]['label'].split()[1])


# # Number of Receptions

# In[23]:


rec_url = 'https://sportsbook-us-co.draftkings.com//sites/US-CO-SB/api/v5/eventgroups/88808/categories/782/subcategories/8165?format=json'

response = req.get(rec_url)
response.raise_for_status()
passyards = response.json()
rawdata = passyards['eventGroup']['offerCategories']
rawdata = rawdata[4]
rawdata = rawdata['offerSubcategoryDescriptors']
rawdata = rawdata[6]
rawdata = rawdata['offerSubcategory']
rawdata = rawdata['offers']
rawdata = rawdata[0]


# In[25]:


pprec = .5

for total in rawdata:
    player = ' '.join(total['label'].split(' ')[:2])
    if player in dfRB.index:
        dfRB.loc[player,'Points'] += pprec * float(total['outcomes'][0]['label'].split()[1])
        dfRB.loc[player, 'Has Reception Count'] = True
    elif player in dfWR.index:
        dfWR.loc[player, 'Has Reception Count'] = True
        dfWR.loc[player,'Points'] += pprec * float(total['outcomes'][0]['label'].split()[1])


# # Seperate WRs and TEs

# In[27]:


TE = ['Travis Kelce','Mark Andrews','Darren Waller','Kyle Pitts',
      'George Kittle','Dalton Schultz','T.J. Hockenson','Dallas Goedert',
      'Zach Ertz','Dawson Knox','Mike Gesicki']


dfTE = dfWR[dfWR.index.isin(TE)]
dfWR = dfWR[~dfWR.index.isin(TE)]


# # Sort by highest scorers

# In[31]:


dfQB = dfQB.sort_values(by='Points', ascending=False)
dfRB = dfRB.sort_values(by='Points', ascending=False)
dfWR = dfWR.sort_values(by='Points', ascending=False)
dfTE = dfTE.sort_values(by='Points', ascending=False)


# In[39]:


dfQB.to_csv('Vegas_QB_Projections.csv')


# In[40]:


dfRB.to_csv('Vegas_RB_Projections.csv')
dfWR.to_csv('Vegas_WR_Projections.csv')
dfTE.to_csv('Vegas_TE_Projections.csv')


# In[ ]:




