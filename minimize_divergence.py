import json

import scipy
import matplotlib.pyplot as plt

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
    for cat in categories:
        div += human[cat]*np.log(human[cat])
        div -= human[cat]*np.log(text[cat]*alpha+image[cat]*(1-alpha))
    return div


def get_human(num_seconds):
    data = json.load(open(HUMAN_PATH))
    relevant = [entry for entry in data
                if entry['n_seconds'] == num_seconds and entry['tag'] == 'valid']
    

    dist.renormalize()
    return dist


def get_text():
    data = json.load(open(TEXT_PATH))
    dists = {}
    for image, input_dist in data.items(): 
        dist = make_dist({int(category_id): float(p) for category_id, p in input_dist.items()})  
        dists[int(image)] = dist
    print(dists)
    return dists

    
def get_image():
    data = json.load(open(IMAGE_PATH))
    dist = Dist()  
    dist.renormalize()
    return dist



categories = json.load(open(CATEGORIES_PATH))

text_dist = get_text()
#image_dist = get_image()

#alphas = {time: get_alpha(text_dist, image_dist, get_human(time)) for time in INTERVALS}

#plt.scatter(alphas.keys(), alphas.values())

print(make_dist({}))
