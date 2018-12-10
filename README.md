# lda_infographics
LDA applied to Infographics - Final Project for 6.804

## Image differences
### different size images
### 2 categories: images and text very different, and image and text very similar
### content of what they are talking about
### obvious titles or not
### ones with clear category, ones that are more multi-dimensional

## Variables to control for:
dimensions and orientation

## User study 
User study is located in another repo for ease of deploying. Find it here: https://github.com/a-newman/cocosci-study

## Data set
Notes about improvements/confusions/comments about the data set and its use:- Some of the images in the dataset of scraped icons from Google do not work (cause errors when trying to load using pytorch's ImageFolder loader). TODO: make a list of thsese problem images 
- It was unclear to me where to find the links for some of the data files (those in `links_to_data_files.md`. Maybe there should be a brief description in the README of all data files, what they contain, their size, where they are located, etc. 
- I was confused between some of the data files. For instance, for some infographics, there are computer-generated icon proposals as well as human-labeled icons and originally I used the wrong data inadvertently. See above comment about an index of data files.
