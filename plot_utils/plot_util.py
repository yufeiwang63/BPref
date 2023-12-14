import pandas
import os.path as osp
import os
import json
import numpy as np
from collections import defaultdict
import json
import glob
import yaml

def read_data(data_dirs, plot_key, filter_function=None, label_function=None, max_x=300, kernel_size=5, read_train=False):
    
    # Replace 'your_directory_path' with the path of your directory

    search_path = '/**/train.csv'

    all_train_csv_files = []
    for data_dir in data_dirs:
    # Use glob.glob with the recursive flag set to True
        train_csv_files = glob.glob(data_dir + search_path, recursive=True)
        all_train_csv_files.extend(train_csv_files)

    if type(plot_key) is not list:
        plot_key = [plot_key]

    res = defaultdict(list)
    for path in all_train_csv_files:
        dir = os.path.dirname(path)

        if read_train:
            progress_path = osp.join(dir, 'train.csv')
        else:
            progress_path = osp.join(dir, 'eval.csv')

        if not osp.exists(progress_path):
            continue
        try:
            progress = pandas.read_csv(progress_path)
        except pandas.errors.EmptyDataError:
            # print(progress_path + " empty")
            continue

        variant_path = osp.join(dir, '.hydra/overrides.yaml')
        if not osp.exists(variant_path):
            continue
        variant = yaml.safe_load(open(variant_path, 'r'))
        variant_keys = [line.split('=')[0].strip() for line in variant]
        variant_values = [line.split('=')[1].strip() for line in variant]
        variant = dict(zip(variant_keys, variant_values))
        
        default_variant_path = osp.join(dir, '.hydra/config.yaml')
        default_variant = yaml.safe_load(open(default_variant_path, 'r'))
        eval_freq = default_variant['eval_frequency']
        variant.update(default_variant)

        if filter_function is not None:
            if filter_function(variant):
                continue

        for key in plot_key:
            all_keys = progress.keys() 
            label = label_function(variant)
            if key not in all_keys:
                print("Key {} not in progress keys: {}".format(key, all_keys))
                values = np.zeros(1)
                res[key].append((values, eval_freq, label))
                continue

            values = progress[key].values
            values = values[~np.isnan(values)]
            # values = values[values != 0]

            if kernel_size > 0:
                kernel = np.ones(kernel_size) / kernel_size
                len_of_values = len(values)
                values = list(values) + [values[-1]] * (kernel_size - 1)
                values = np.convolve(values, kernel, mode='same')
                values = values[:len_of_values]
                
            values = values[:max_x]

            if label_function is None:
                res[key].append(values)
            else:
                print(label)
                res[key].append((values, eval_freq, label))

    # result is a two level dict, first key is plot key, second key is group key
    if len(plot_key) == 1:
        return res[plot_key[0]]
    else:
        return res

def group_data(results, return_eval_freq=False):
    if type(results) == list: # sinlge plot key
        result_dict = defaultdict(list)
        eval_freq_dict = defaultdict(list)
        for res in results:
            res_values, eval_freq, group_key = res
            result_dict[group_key].append(res_values)
            if return_eval_freq:
                eval_freq_dict[group_key].append(eval_freq)
        if return_eval_freq:
            return result_dict, eval_freq_dict
        return result_dict
    else: # multiple plot keys
        all_result_dict = {} 
        all_eval_freq_dict = {}
        for plot_key, result in results.items():
            result_dict = defaultdict(list)
            eval_dict = defaultdict(list)
            for res in result:
                res_values, eval_freq, group_key = res
                result_dict[group_key].append(res_values)
                eval_dict[group_key].append(eval_freq)
            all_result_dict[plot_key] = result_dict
            all_eval_freq_dict[plot_key] = eval_dict
        if return_eval_freq:
            return all_result_dict, all_eval_freq_dict
        return all_result_dict


def read_and_group_data(data_dirs, plot_key, filter_function=None, label_function=None, max_x=300, kernel_size=5, return_eval_freq=False, read_train=False):

    results = read_data(data_dirs, plot_key, filter_function, label_function, max_x, kernel_size, read_train=read_train)
    if not return_eval_freq:
        result_dict = group_data(results, return_eval_freq=False)
        return result_dict
    else:
        result_dict, eval_freq_dict = group_data(results, return_eval_freq=True)
        return result_dict, eval_freq_dict

def tolerant_mean(arrs):
    lens = [len(i) for i in arrs]
    arr = np.ma.empty((np.max(lens),len(arrs)))
    arr.mask = True
    for idx, l in enumerate(arrs):
        arr[:len(l),idx] = l
    return arr.mean(axis = -1), arr.std(axis=-1)

def read_json_log(path):
    filtered_data = []
    with open(path, 'r') as handle:
        json_data = [json.loads(line) for line in handle]
        for dict in json_data:
            if len(dict.keys()) > 1:
                filtered_data.append(dict)

    return filtered_data