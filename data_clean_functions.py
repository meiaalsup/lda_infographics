import copy
import math
import random
import json
import boto3
import os

CLIENT = None
S3 = None

def sort_by_annotations(data):
    labels = {}
    for path, ann in data.items():
        for label, label_data in ann.items(): 
            label_type = label_data["type"]
            if not labels.get(label_type, False): 
                labels[label_type] = {}
            # add the annotation to the appropriate bucket
            labels[label_type][label] = labels[label_type].get(label, [])
            labels[label_type][label].append(path)
    return labels;

def print_sorted_annotations(labels):
    print("Label types: ", labels.keys())
    print("\n")
    for label_type, ann in labels.items(): 
        print("Label type %s: %d subcategories" % (label_type, len(ann)))

    print("\n")
    for label_type, ann in labels.items():
        print("Label type %s" % label_type)
        for ann_type, paths in ann.items():
            print("\t%s: %d examples" % (ann_type, len(paths)))

def filter_data(data, filter_func): 
    # filter_func is a function that will be applied to each annotation 
    filtered = {}
    for path, ann in data.items():
        is_valid = True;
        for label, label_data in ann.items(): 
            if not filter_func(label, label_data): 
                is_valid = False
                break
        if is_valid: filtered[path] = ann
    return filtered

def filter_concensus(label, label_data):
    return label_data['neg'] == 0

def filter_data_by_concensus(data): 
    return filter_data(data, filter_concensus)

# Try to pick things roughly in proportion to the original 
def get_proportional_coverage(sorted_data, n): 
    # n is the approximate number of things you want to pull 
    key_val_tuples = [(key, val) for key, val in sorted_data.items()]
    print(key_val_tuples[0][0])
    random.shuffle(key_val_tuples)
    
    # Figure out about how many you want of each 
    ratio = n/len(key_val_tuples)
    target_cat_nums = copy.deepcopy(sorted_data)
    tot = 0
    num_subcats = 0
    for category, subcats in target_cat_nums.items(): 
        for subcat, paths in subcats.items(): 
            num_subcats += 1
            desired_num = max(math.floor(ratio*len(paths)), 1)
            target_cat_nums[category][subcat] = desired_num
            tot += desired_num
    
    # do keep adding until you hit your limit on each 
    coverage = {}
    ret = set()
    for path, ann in key_val_tuples: 
        should_add = False
            
        for label, label_data in ann.items(): 
            print(label_data)
            label_type = label_data["type"]
            if label_type not in coverage: 
                coverage[label_type] = {}
            if label not in coverage[label_type]: 
                coverage[label_type][label] = 0
            # Here's where we actually check whether to add 
            if coverage[label_type][label] < target_cat_nums[label_type][label]: 
                should_add = True
                
        # loop through again to update 
        if should_add: 
            ret.add(path)
            for label, label_data in ann.items(): 
                label_type = label_data["type"]
                coverage[label_type][label] += 1
                
    return ret
    

def divy_up(paths, subjects, max_len_task=100): 
    portions = {} 
    paths_pp = math.floor(len(paths)/len(subjects))
    end_ptr = paths_pp
    start_ptr = 0
    for i in range(len(subjects)): 
        portions[subjects[i]] = paths[i*paths_pp : (i+1)*paths_pp]
        # if it's the last person, given them the rest of the list too 
        if (i==len(subjects) -1):
            portions[subjects[i]].extend(paths[(i+1)*paths_pp:])
    
    # now chunk the portions into size 100 
    for person, _ in portions.items(): 
        portions[person] = chunks(portions[person], 99)
    return portions
    

def chunks(l, n):    
    return list((l[i: min(i+n, len(l))] for i in range(0, len(l), n)))
        
def print_portions(portions): 
    for person in portions: 
        print("%s has %d chunks" % (person, len(portions[person])))
        print("\t", [len(elt) for elt in portions[person]])

    total = 0
    paths = set()
    for person, chunks in portions.items(): 
        for chunk in chunks: 
            total += len(chunk)
            for path in chunk: 
                if path in paths: 
                    raise RuntimeException()
                paths.add(path)

def s3_connect(profile_name='personal-heroku'):
    global CLIENT
    global S3
    session = boto3.session.Session(profile_name=profile_name)
    CLIENT = session.client('s3')
    S3 = session.resource('s3')

# grabbing data from s3
def get_all_keys(bucket): 
    req = {
        'Bucket': bucket,
    }
    r = CLIENT.list_objects(**req)
    items = [elt['Key'] for elt in r['Contents']]
    while r['IsTruncated']: 
        req['Marker'] = r['NextMarker']
        r = CLIENT.list_objects(**req)
        items.extend(elt['Key'] for elt in r['Contents'])
    return items
        
def get_safe_temp_file(): 
    temp_file_base = "tmp%s.txt"
    i = 0
    temp_filename = temp_file_base % 0
    while (os.path.isfile(temp_filename)):
        if (i > 20):
            raise RuntimeException("Could not find a valid temp filename")
        i += 1
        temp_filename = temp_file_base % i
    return temp_filename

def download_data(bucket_name, saveto=""): 
    keys = get_all_keys(bucket_name)
    bucket = S3.Bucket(bucket_name)
    data = {}
    # check that the temp file does not already exist
    temp_filename = get_safe_temp_file()
    for key in keys: 
        with open(temp_filename, 'wb') as tmpfile: 
            bucket.download_fileobj(key, tmpfile)
        with open(temp_filename, 'r') as tmpfile: 
            data[key] = json.load(tmpfile)
    os.remove(temp_filename)
    if (saveto): 
        with open(saveto, 'w') as outfile: 
            json.dump(data, outfile)
    return data

def save_tasks(portions, base_path, base_url="https://video-cleaning.herokuapp.com/?data="): 
    # Let's save this data 
    for person, chunks in portions.items(): 
        for i, chunk in enumerate(chunks): 
            empty_dict = dict([(elt, 0) for elt in chunk])
            pathname = "%s_%d.json" % (person, i)
            print("\t" + base_url + pathname.replace(".json", ""))
            with open(base_path + pathname, 'w') as outfile: 
                json.dump(empty_dict, outfile)