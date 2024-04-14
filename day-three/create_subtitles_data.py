# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 11:54:00 2024

@author: dsca347
"""

import os
import glob
import re
from string import ascii_lowercase
import pandas as pd
import numpy as np
from names_dataset import NameDataset
from collections import Counter

## DIRECTORIES AND SETTINGS
movie_dir             = 'PUT THE PATH TO THE DIRECTORY CONTAINING THE SUBTITLES FILES HERE'
common_words_remove_n = 100  # Number of common words to exclude
normalise_by_group    = True # Whether frequencies should be normalised by movie or across all movies.

## FUNCTIONS
def clean_srt(filePath):
    
    # Read file
    try:
        file  = open(filePath, 'r', encoding="utf8")
        lines = file.readlines()
    except:
        file  = open(filePath, 'r', encoding="utf-8-sig")
        lines = file.readlines()
    finally:   
        file.close()
        
    lines.pop(0)
    
    # Clean up (from: https://stackoverflow.com/questions/51073045/parsing-transcript-srt-files-into-readable-text)
    text = ''
    for line in lines:
        if re.search('^[0-9]+$', line) is None and re.search('^[0-9]{2}:[0-9]{2}:[0-9]{2}', line) is None and re.search('^$', line) is None:
            text += ' ' + line.replace('<i>', '').replace('</i>', '').replace("'", " '").rstrip('\n')
        text = text.lstrip()
    text = re.sub(r"[^\w\s']+", '', text)
    text = re.sub(r"[\d']", '', text).lower().split()

    word_frequencies = dict(Counter(text))
    
    return word_frequencies, text

## CREATE DATASET
movie_files       = glob.glob(os.path.join(movie_dir, '*.srt'))
movie_files       = [iMovie for iMovie in movie_files if iMovie[-5] in ['c', 'w', 's']]
movie_word_counts = pd.DataFrame(columns=['word', 'frequency', 'title', 'category'])

for iMovie in movie_files:
    
    current_frequencies, _ = clean_srt(iMovie)
    
    current_df             = pd.DataFrame(current_frequencies.items(), columns=['word', 'frequency']).sort_values(by='frequency', ascending=False)
    current_df['title']    = np.repeat(os.path.basename(iMovie)[0:-6], len(current_df))
    current_df['category'] = np.repeat(os.path.basename(iMovie)[-5], len(current_frequencies))
    
    movie_word_counts      = pd.concat([movie_word_counts, current_df], ignore_index=True)

## CLEAN UP
# - Remove most common words (https://github.com/orgtre/top-open-subtitles-sentences/blob/main/bld/top_words/en_top_words.csv)
# - Also remove ramaining single letters (from 's, 'd, etc... or preprositions like a)
common_subtitles_tokens = pd.read_csv(os.path.join(movie_dir, 'top_english_words.csv'), nrows=common_words_remove_n)['word'].apply(lambda x: re.sub(r"'", '', x))

all_tokens_to_remove    = list(common_subtitles_tokens.str.lower()) + list(ascii_lowercase)
movie_word_counts       = movie_word_counts[-movie_word_counts['word'].isin(all_tokens_to_remove)].reset_index(drop=True)

# Remove names
names_set = NameDataset()
names_df  = pd.DataFrame(names_set.get_top_names(n=1000))

names_list = []
for iName, iColumn in names_df.items():
    names_list += iColumn[0] + iColumn[1]
names_list = [iName.lower() for iName in names_list]

movie_word_counts = movie_word_counts[-movie_word_counts['word'].isin(names_list)].reset_index(drop=True)

# Normalize

normalised_frequencies = movie_word_counts.groupby('title').apply(lambda x: x['frequency'] / sum(x['frequency'])).reset_index(drop=True)
movie_word_counts      = movie_word_counts.assign(normalised_frequency = normalised_frequencies)


# Ensure each movie has the same words. If a movie does not have a word, add 0
# to the normalise frequencies.
# From (https://stackoverflow.com/questions/47117982/insert-missing-category-for-each-group-in-pandas-dataframe)
words_all = movie_word_counts['word'].unique()
def f(x):
    return x.reindex(words_all, fill_value=0).assign(title=x['title'][0],
                                                          category=x['category'][0])
movie_word_counts = movie_word_counts.set_index('word').groupby('title', group_keys=False).apply(f).reset_index()

# Sum normalised frequencies across movies for each category
movie_word_count_by_category = movie_word_counts.groupby(['category', 'word'], as_index=False)['normalised_frequency'].sum()

# Save data
movie_word_counts.to_csv(os.path.join(movie_dir, 'subtitles_corpus_clean.csv'), encoding='utf-8-sig')
movie_word_count_by_category.to_csv(os.path.join(movie_dir, 'subtitles_frequencies.csv'), encoding='utf-8-sig')



















    