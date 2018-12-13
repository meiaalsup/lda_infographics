# lda_infographics
LDA applied to Infographics - Final Project for 6.804

## LDA on Text
Preprocessing of textual components and LDA training / prediction [code here](https://github.com/meiaalsup/lda_infographics/blob/master/lda_text.ipynb)

## User study 
User study is located in [another repo](https://github.com/a-newman/cocosci-study) for ease of deploying.

## Model fitting
Alpha Optimization [code here](https://github.com/meiaalsup/lda_infographics/blob/master/calculate_optimal_alpha.py)


## Data set
Notes about improvements/confusions/comments about the data set and its use:- Some of the images in the dataset of scraped icons from Google do not work (cause errors when trying to load using pytorch's ImageFolder loader). TODO: make a list of thsese problem images 
- It was unclear to me where to find the links for some of the data files (those in `links_to_data_files.md`. Maybe there should be a brief description in the README of all data files, what they contain, their size, where they are located, etc. 
- I was confused between some of the data files. For instance, for some infographics, there are computer-generated icon proposals as well as human-labeled icons and originally I used the wrong data inadvertently. See above comment about an index of data files.



## Analysis
image 0: All the predictions and distributions line up very well. It is unclear if this is
statistically significant but the topics are immediately obvious in this image. The topic are
slightly better with 25 seconds than 5 than 1, which matches our hypothesis, but not by much.

image 1: everyone thought it was about the environment regardless of how long they looked at it. So
the distributions are all very close. The images were not environmental so the image distribution is
far off from human intuition. This is an example of the model failing b/c visual content was not
well represented by the icons, but likely the most important visual element here was the green
hills.

image 2: The two general categories are correct, but humans gravitate towards family more and more
whereas LDA on the text predicted a stronger health category than family. The text gave a lot of
meaning, but the images did not. However, LDA on the text was not a good predictor of human
cognition

image 3:  Hunter/Farmers and Marketing. Our textual andimage predictions are not good modelers of
human cognition in this case.

image 4: Words about food are more present than words about health, but the infographic is actually
trying to tell you about health. But both text LDA and the image categories say its about food.
People can extrapolate its actually about health with more time, so with more time the text-image
model does a worse job modeling the higher level of human cognition

image 5: Here our model does a good job predicting categories regardless of image and textual data.

image 6: This is an example where our hypothesis holds to a decent amount and we see the inflection
point and trade-off from image to text data quite clearly

image 7: Image prediction is monotic and doesn't add any information, so the textual data is a much
better model of human cognition in this case.

image 8: This one has a clear demonstration that the textual data is really important. The images
are quite misleading and so the match to the textual LDA preditions is significantly better with 25
seconds instead of 1 or 5 sec. This has interesting implications as a measurement of human
confusion.

image 9: Here our model matches human predictions really well. We see small error across the board.

image 10: This provides a tiny amount of info that perhap LDA on text matches short simple human
cognition when people don't have a ton of time to look at the image. Overall error is low so the
model matches human predictions well.

image 11: Unconfusing and unambiguous infographic: text and images don't diverge a lot and humans
can understand the main topics quickly without the need for more time. This one is understandable at a glance.
