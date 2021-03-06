import numpy as np
from random import shuffle
import json

t0 = 1
t1 = 5
t2 = 25

time_exposures = np.array([
    [t0, t0, t0, t0, t1, t1, t1, t1, t2, t2, t2, t2],
    [t0, t0, t0, t1, t1, t1, t1, t2, t2, t2, t2, t0],
    [t0, t0, t1, t1, t1, t1, t2, t2, t2, t2, t0, t0],
    [t0, t1, t1, t1, t1, t2, t2, t2, t2, t0, t0, t0],
    [t1, t1, t1, t1, t2, t2, t2, t2, t0, t0, t0, t0],

    [t1, t1, t1, t2, t2, t2, t2, t0, t0, t0, t0, t1],
    [t1, t1, t2, t2, t2, t2, t0, t0, t0, t0, t1, t1],
    [t1, t2, t2, t2, t2, t0, t0, t0, t0, t1, t1, t1],
    [t2, t2, t2, t2, t0, t0, t0, t0, t1, t1, t1, t1],
    [t2, t2, t2, t0, t0, t0, t0, t1, t1, t1, t1, t2],

    [t2, t2, t0, t0, t0, t0, t1, t1, t1, t1, t2, t2],
    [t2, t0, t0, t0, t0, t1, t1, t1, t1, t2, t2, t2],

    [t0, t1, t2, t0, t1, t2, t0, t1, t2, t0, t1, t2],
    [t1, t2, t0, t1, t2, t0, t1, t2, t0, t1, t2, t0],
    [t2, t0, t1, t2, t0, t1, t2, t0, t1, t2, t0, t1],
])

urls = {}
for person_id, person_row in enumerate(time_exposures):
    person_urls = []
    for i, exposure in enumerate(person_row):
        person_urls.append(f'http://cocosci-study.herokuapp.com/?im_id={i}&n_s={exposure}&subj_id={person_id+16+15+15+15}&tag=valid')
    shuffle(person_urls)
    urls[person_id] = person_urls

print(urls)
json.dump(urls, open('urls_round5.json', 'w'))

'''
result:
[
    [
        (infographic_id, time)
    ],
    person_id: [
        (infographic_id, time)
    ]

    ...
    person_15
]

'''
