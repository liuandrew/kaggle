# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 12:07:06 2018

@author: Andy
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
import codecs

#%%
with codecs.open('title_ratings.tsv', 'r', 'utf-8') as f:
  num_lines = 0
  for line in f:
    num_lines += 1
  
  print(num_lines)
#%%
title_basics_file = codecs.open('title_basics.tsv', 'r', 'utf-8')
title_ratings_file = codecs.open('title_ratings.tsv', 'r', 'utf-8')
condensed_file = codecs.open('title_combined.tsv', 'w', 'utf-8')
condensed_file.write('tconst\ttitleType\tstartYear\taverageRating\tnumVotes\n')
line_count = 0

while(line_count < 4894381):
  #write head
  if(line_count % 50000 == 0):
    print(line_count)
    
  line_count += 1
  try:
    basics_line = title_basics_file.readline()
    ratings_line = title_ratings_file.readline()
    basics = basics_line.split('\t')
    ratings = ratings_line.split('\t')
    #basicsc: 0: tconst, 1: titleType, 2: primaryTitle, 3: originalTitle, 4:isAdult
    #         5: startYear, 6: endYear, 7: runtimeMinutes, 8: genres
    #ratings: 0: tconst, 1: averageRating, 2: numVotes
    write_line = ''
    if(basics[1] == 'movie' and int(basics[5]) > 1969):
      write_line += basics[0] + '\t' + basics[2] + '\t' + basics[5] + '\t' + ratings[1] + '\t' + ratings[2]
      condensed_file.write(write_line)
  except Exception as e:
    pass
#    print(e)
#    print(basics)
    
title_basics_file.close()
title_ratings_file.close()
condensed_file.close()

#%%
title_basics = pd.read_csv('title_basics.tsv', sep='\t')
title_ratings = pd.read_csv('title_ratings.tsv', sep='\t')
#%%
#generate list of movies with over 1000 votes
limit_ratings = title_ratings[title_ratings.numVotes > 999]
limit_basics = title_basics[title_basics.titleType == 'movie']
movies = limit_ratings.merge(limit_basics, 'inner', on='tconst')
for col in ['titleType', 'endYear', 'isAdult', 'originalTitle']:
  movies = movies.drop(col, axis=1)

#%%
principals = pd.read_csv('title_principals.tsv', sep='\t')
#%%
#get number of unique crew members to track
for col in ['ordering', 'category', 'job', 'characters']:
  principals = principals.drop(col, axis=1)
principals_merged = movies.merge(principals, on='tconst')

