import json

import scipy
import matplotlib.pyplot as plt
import numpy as np

from util import Distribution as Dist


HUMAN_PATH = 'study_data.json'
IMAGE_PATH = 'sravya_data.json'
TEXT_PATH = 'text_distribution.json'
CATEGORIES_PATH ='categories_edited.json' 
NUM_IMAGES = 12
INTERVALS = [1, 5, 25]


def make_dist(dist):
    start = Dist({int(cat):0 for cat in categories})
    for key, p in dist.items():
        start[key] = p
    start.renormalize()
    return start


###################################################################################################
# Divergence calculation
###################################################################################################

def get_alpha(text, image, human):
    # D(human | image + text)
    def fun(a):
        total_div = 0
        for i in range(12):
            total_div += divergence(text[i], image[i], human[i], a)
    return scipy.optimize.minimize(fun, .5)


def divergence(text, image, human, alpha):
    # Calculates divergence between the distributions for a given image
    div = 0
    print(human)
    for cat in categories:
        div += human[cat] * np.log(human[cat])
        div -= human[cat] * np.log(text[cat]*alpha+image[cat]*(1-alpha))
    return div

#def average_divergence(text, image, human, alpha):
#    for id_ in range(NUM_IMAGES):




###################################################################################################
# Get the distributions
###################################################################################################

def get_human(num_seconds):
    data = json.load(open(HUMAN_PATH))
    relevant = [entry for entry in data
                if entry['n_seconds'] == num_seconds and entry['tag'] == 'valid']
    

    humans = {image_id: make_dist({}) for image_id in range(NUM_IMAGES)}
    for entry in relevant:
        id_ = int(entry['im_id'])
        for category, weight in entry['answers'].items():
            p = 0
            if len(weight) > 0:
                p = int(weight)
            humans[id_][int(category)] += p
    for im, dist in humans.items():
        dist.renormalize()
    return humans


def get_text():
    data = json.load(open(TEXT_PATH))
    dists = {}
    for image, input_dist in data.items(): 
        dist = make_dist({int(category_id): float(p) for category_id, p in input_dist.items()})  
        dists[int(image)] = dist
    print(dists)
    return dists

    
def get_image():
    return {image_id: make_dist({}) for image_id in range(NUM_IMAGES)}



categories_edited = json.load(open(CATEGORIES_PATH))
categories = {int(cat):val for cat, val in categories_edited.items()}
print(categories)

text_dist = get_text()
image_dist = get_image()

#alphas = {time: get_alpha(text_dist, image_dist, get_human(time)) for time in INTERVALS}

alpha_values = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
alphas = {time: [divergence(text_dist, image_dist, get_human(time), alpha)
                 for alpha in alpha_values]
          for time in INTERVALS}

plt.plot(alpha_values, alphas[1])
plt.plot(alpha_values, alphas[5])
plt.plot(alpha_values, alphas[25])
#plt.scatter(alphas.keys(), alphas.values())

