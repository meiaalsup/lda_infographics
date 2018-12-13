import numpy as np
import matplotlib.pyplot as plt
import json

from sklearn.metrics import mean_squared_error
from scipy.stats import entropy
import scipy

from util import Distribution as Dist


HUMAN_PATH = 'study_data.json'
IMAGE_PATH = 'sravya_hand_icon_labels.txt'
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
# Alpha calculation from loss minimization (divergence and MSE)
###################################################################################################

def get_alpha(text, image, human, loss_fn):
    def fun(a):
        return loss(text, image, human, a, list(range(NUM_IMAGES)), loss_fn)
    return scipy.optimize.minimize(fun, .5, bounds=[(0.01,.99)])


def loss(text, image, human, alpha, include_in_divergence, loss_fn):
    total_div = 0
    for id_ in include_in_divergence:
        total_div += loss_fn(text[id_], image[id_], human[id_], alpha)
    return total_div


def divergence(text, image, human, alpha):
    # D(human | image + text)
    # Calculates divergence between the distributions for a given image
    pred = {cat: alpha*text[cat] + (1-alpha)*image[cat] for cat in categories}
    x, y = [], []
    for cat in categories:
        x.append(pred[cat])
        y.append(human[cat])
    return entropy(y,x, base=2)
    #return np.sum(ent)

def mse(text, image, human, alpha):
    pred = {cat: alpha*text[cat] + (1-alpha)*image[cat] for cat in categories}
    x, y = [], []
    for cat in categories:
        x.append(pred[cat])
        y.append(human[cat])
    return mean_squared_error(x, y)


##################################################################################################
# Get the distributions
##################################################################################################

def get_human(num_seconds):
    data = json.load(open(HUMAN_PATH))
    relevant = [entry for entry in data
                if entry['n_seconds'] == num_seconds and entry['tag'] == 'valid']
    counts = {image_id: 0 for image_id in range(NUM_IMAGES)}
    
    humans = {image_id: {int(cat):0 for cat in categories} for image_id in range(NUM_IMAGES)}
    for entry in relevant:
        id_ = int(entry['im_id'])
        total = sum([float(x) for x in entry['answers'].values() if len(x)>0 and len(x)<=2])
        if total > 0:
            counts[id_] +=1
            for category, weight in entry['answers'].items():
                p = 0
                if len(weight) > 0:
                    p = float(weight)/total*10
                humans[id_][int(category)] += p
    for im, dist in humans.items():
        humans[im] = Dist(dist)
        humans[im].renormalize()
    print(f'for {num_seconds} seconds we have the following counts: {counts}')
    return humans


def get_text():
    data = json.load(open(TEXT_PATH))
    dists = {}
    for image, input_dist in data.items(): 
        dist = make_dist({int(category_id): float(p) for category_id, p in input_dist.items()})  
        dists[int(image)] = dist
    return dists

    
def get_image():
    content = open(IMAGE_PATH).readlines()
    images = {image_id: {int(cat):0 for cat in info_to_cats[str(image_id)]}
              for image_id in range(NUM_IMAGES)}
    for line in content:
        stuff = line.split()
        if len(stuff) >=5:
            id_ = url_to_id[stuff[0]]
            cat1, cat2, cat3 = int(stuff[2]), int(stuff[3]), int(stuff[4])
            if cat1 in images[id_]:
                images[id_][cat1]+= 2
            if cat2 in images[id_]:
                images[id_][cat2]+= 1
            if cat3 in images[id_]:
                images[id_][cat3]+= 0
    for im, dist in images.items():
        images[im] = Dist(dist)
        images[im].renormalize()
        images[im] = make_dist({key: val for key, val in images[im].items() if val > 0.07})
        images[im].renormalize()
    return images

###################################################################################################
# Problem Setup: Loading the relevant information
###################################################################################################

url_to_id = json.load(open('infographic_url_to_id_map.json'))
id_to_url = json.load(open('infographic_id_to_url_map.json'))
categories_edited = json.load(open(CATEGORIES_PATH))
categories = {int(cat):val for cat, val in categories_edited.items()}
info_to_cats = json.load(open('info_to_cats_dict.json'))

text_dist = get_text()
image_dist = get_image()
human = {time: get_human(time) for time in INTERVALS}

##################################################################################################
# Execute calculations and optimizations
##################################################################################################

alpha_values = [x*.1 for x in range(11)]
alphas_div = {time: [loss(text_dist, image_dist, human[time], alpha,
                     list(range(NUM_IMAGES)), divergence)
                    for alpha in alpha_values]
              for time in INTERVALS}

alphas_mse = {time: [loss(text_dist, image_dist, human[time], alpha, list(range(NUM_IMAGES)), mse)
                     for alpha in alpha_values]
              for time in INTERVALS}

alphas_i_div = {i: {time: [loss(text_dist, image_dist, human[time], alpha, [i], divergence)
                           for alpha in alpha_values]
                    for time in INTERVALS}
                for i in range(NUM_IMAGES)}

alphas_i_mse = {i: {time: [loss(text_dist, image_dist, human[time], alpha, [i], mse)
                           for alpha in alpha_values]
                    for time in INTERVALS}
                for i in range(NUM_IMAGES)}



##################################################################################################
# Plot results
##################################################################################################

grid_number = [i for i in categories.keys()]
width = .2
colors = ['red', 'green', 'blue', 'orange', 'gray', 'purple']
for im in range(NUM_IMAGES):
    w = 0
    for time, im_dist in human.items():
        #for im, dist_ in im_dist.items():
        dist_ = im_dist[im]
        plt.bar([g+w*width for g in grid_number], dist_.values(), width, color=colors[w],
                label=f'human for {time} seconds')
        w+=1
    plt.title(f'PDF of distributions for image number {im}')
    plt.xticks(grid_number, [categories[i] for i in grid_number], rotation='vertical')
    plt.bar([g+4*width for g in grid_number], image_dist[im].values(), width, color=colors[3],
            label=f'image')
    plt.bar([g+3*width for g in grid_number], text_dist[im].values(), width, color=colors[4],
            label=f'text from LDA')
    plt.legend()
    plt.tight_layout()
    plt.xlabel(f'categories')
    plt.ylabel(f'probability')
    plt.plot()
    plt.savefig(f'results/distribution_im{im}.png')
    plt.close()

    plt.title(f'MSE for image number {im}')
    plt.plot(alpha_values, alphas_i_mse[im][1], label='1 sec of human exposure', color='red')
    plt.plot(alpha_values, alphas_i_mse[im][5], label='5 sec of human exposure', color='green')
    plt.plot(alpha_values, alphas_i_mse[im][25], label='25 sec of human exposure', color='blue')
    plt.ylim(0, .04)
    plt.xlabel(f'alpha - proportion of text')
    plt.ylabel(f'Mean Squared Error')
    plt.tight_layout()
    plt.legend()
    plt.plot()
    plt.savefig(f'results/mse_im{im}.png')
    plt.close()

opt_alphas_mse = {time: get_alpha(text_dist, image_dist, human[time], mse).x
                  for time in INTERVALS}
for j, i in enumerate(INTERVALS):
    print(f'{opt_alphas_mse[i]} is optimal for {i} seconds with mse loss')
    print(f'mse: {loss(text_dist, image_dist, human[i], opt_alphas_mse[i], list(range(NUM_IMAGES)), mse)}')
    plt.plot(alpha_values, alphas_mse[i], label=f'{i} sec of human exposure', color=colors[j])
plt.title('Average Mean Squared Error across all 12 Images')
plt.xlabel(f'alpha value (proportion that is text)')
plt.ylabel(f'Mean Squared Error')
plt.legend()
plt.plot()
plt.savefig(f'results/loss_all_images_averaged.png')
plt.close()

