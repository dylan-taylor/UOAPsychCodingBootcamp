# UOAPsychCodingBootcamp

This project contains some material used during the Psychology Coding Bootcamp (2024) at the University of Auckland. We have included only the material necessary to recreate or expand on what was done during the bootcamp. We have not included material (eg. scripts or Psychopy files) that can be re-created from the slides or guides included on the official [bootcamp website](https://psychology-coding-bootcamp.netlify.app/)

## CONTENT
A brief description of the content of each folder included here. 

### day-one
*average_exercise.py*: Python script to compute the average of a list of numbers. It contains some errors that you should fix.
*error_exercise.py*: Python script containing errors that you should fix
### day-three
*identifiable_clusters.csv*: file containing a list of movies with their associated frequencies of *space*, *west* and *winter* words. The file is useful to verify the accuracy of the k-means algorithm run during the bootcamp. Fileds:
frequency_space: frequency of space-related words for each movie
frequency_west: frequency of west-related words for each movie
frequency_winter: frequency of winter-related words for each movie
clusters: categorical variable indicating which group a movie has been assigned to through k-means (note: this was obtained running `kmeans()` with `set.seed(27)` on data derived from the *subtitle_corpus.csv* file (see website material).
movie: anonymised movie title
title: original movie title
category: type of movie. c = Christmas, s = sci-fi, w = western
*subtitle_corpus.csv*: uncleaned dataset used during the bootcamp. It contains a list of words with the associated frequency indicating how often each word appears in a movie. Fields:
...1: Index (this is the first column. Technically, it corresponds to Pandas' row ` index`.
Word: word contained in  the subtitles
Frequency_Counts: number of times a word appears in the subtitles of a movie
normalised.Frequency: word count divided by the number of words in the movie
Movie: anonymous place-holder for the movie title
*word_list.txt*: list of words used to generate the space, west and winter frequencies. Used to facilitate the scripting in R without having to type all these words.
SPACE: words from *gravity* to *planet*
WEST: words from *drink* to *canyons*
WINTER: words from *christmas* to *chocolate*
*create_subtitle_data.py*: Python script used to generate `subtitle_corpus.csv`. To run the script, you need to first download the `subtitle_files` folder. Then, modify the script by changing the `movie_dir` variable, so it reflects the path to the downloaded `subtitle_corpus.csv`. For instance: `movie_dir = "C:/Users/YOURIDHERE/Downloads/subtitle_corpus.csv". Play around with the script to understand how it works.
*subtitle_files*: this folder contains the `srt` subtitle files for 72 movies. The files were obtained from [Opensubtitles.org](https://www.opensubtitles.org/en/search/subs). The file name contains the title of the movie followed by a letter indicating the type of movie:
*r*: romcom
*h*: horror
*s* scifi
*d*: documentary
*c*: Christmas
We have not used all these categories, but you can modify the `create_subtitle_data.py` script to obtain the frequencies of all the movies or a subset of categories you are interested in. 
