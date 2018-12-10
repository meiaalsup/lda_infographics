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

urls = []
for person_id, person_row in enumerate(time_exposures):
    person_urls = []
    for i, exposure in enumerate(person_row):
        person_urls.append(f'?im_id={i}&n_s={exposure}&subj_id={person_id}&tag=valid')
    shuffle(person_urls)
    urls.append(person_urls)

print(len(urls))
print(len(urls[0]))
print(urls[0])
print('\n')
print(urls)


json.dump(urls, open('urls.json', 'w'))

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
