import numpy as np
from matplotlib import pyplot as plt
import os
import os.path as osp
import pandas
import json
import argparse
from plot_utils.plot_util import read_and_group_data

def tolerant_mean(arrs):
    lens = [len(i) for i in arrs]
    arr = np.ma.empty((np.max(lens),len(arrs)))
    arr.mask = True
    for idx, l in enumerate(arrs):
        arr[:len(l),idx] = l
    return arr.mean(axis = -1), arr.std(axis=-1)

parser = argparse.ArgumentParser()
parser.add_argument("data_paths", type=str, nargs='*')
parser.add_argument("--combine", type=int, default=1)
parser.add_argument("--save_name", type=str, default="plot")
parser.add_argument("--max_x", type=int, default=10000000)
parser.add_argument("--kernel_size", type=int, default=10)
parser.add_argument("--read_train", type=int, default=0)
parser.add_argument("--plot_key", type=str, default="None")
args = parser.parse_args()

data_dirs = args.data_paths
print(data_dirs)


if args.plot_key == "None":
    plot_keys = [
       "vlm_acc",
       "true_episode_reward",
       "success_rate"
    ]
else:
    plot_keys = [args.plot_key]

ylim_up = [
    500,
    500,
    40
]

ylim_low = [
    -100,-2,-50
]

colors = {}

idx_colors = {
    0: '#1f77b4',
    1: '#d62728',
    2: '#ff7f0e',
    3: '#9467bd',
    4: '#2ca02c',
    5: 'black',
    6: '#e377c2',
    7: 'red',
    8: 'blue'
}

num_keys = len(plot_keys)
fig, axes = plt.subplots(1, num_keys, figsize=(8 * num_keys, 6))
if num_keys == 1:
    axes = [axes]

def filter_func(x):
    return False

def label_func(x):
    return str(x['vlm_label']) + "_" + str(x['teacher_eps_mistake']) + "_" + x['vlm']

for key_idx, key in enumerate(plot_keys):
    ax = axes[key_idx]
    ax.set_title(key)
    all_res, eval_freq_dict = read_and_group_data(data_dirs, key, filter_function=filter_func, label_function=label_func, 
        kernel_size=args.kernel_size,
        max_x=args.max_x, return_eval_freq=True,
        read_train=args.read_train)

    print("plotting key_idx {} key {}".format(key_idx, key))
    print("all_res", all_res)

    min_values = []
    max_values = []
    for l_idx, label in enumerate(all_res):
        print(label)
        values = all_res[label]
        eval_freq = eval_freq_dict[label]

        # for value in values:
        #     sorted_idx = np.argsort(value)
        #     # print("label: ", label)
        #     # print("values: ", value)
        #     # print("sorted_idx: ", sorted_idx)
        #     print("label {} top 5 values: {}".format(label, value[sorted_idx[-5:]]))
        #     print("label {} top 5 idx: {}".format(label, sorted_idx[-5:]))

        if args.combine:
            values, error = tolerant_mean(values)
            sorted_idx = np.argsort(values)
            print("label {} top values: {} top idx {} error at top idx {}".format(label, 
                values[sorted_idx[-1:]], sorted_idx[-1:], error[sorted_idx[-1:]]
            ))

            print("eval_freq is: ", eval_freq)
            x = np.arange(len(values)) * eval_freq[0]
            if len(values) > 1:
                if label in colors.keys():
                    ax.plot(x, values, label=label, color=colors[label])
                elif l_idx in idx_colors.keys():
                    ax.plot(x, values, label=label, color=idx_colors[l_idx])
                else:
                    ax.plot(x, values, label=label)
            else:
                if label in colors.keys():
                    ax.axhline(values[0], label=label, color=colors[label])
                elif l_idx in idx_colors.keys():
                    ax.axhline(values[0], label=label, color=idx_colors[l_idx])
                else:
                    ax.axhline(values[0], label=label)

            color = colors['label'] if label in colors.keys() else idx_colors[l_idx]
            ax.fill_between(x, values-error, values+error, alpha=0.2, color=color)
            ax.legend()
            min_values.append(np.min(values))
            max_values.append(np.max(values))

        ax.legend()

    v_min, v_max = np.min(min_values), np.max(max_values)
    ax.set_ylim(v_min - np.abs(v_min * 0.1), v_max + np.abs(v_max * 0.1))
    # ax.set_ylim(ylim_low[key_idx], ylim_up[key_idx])
    ax.grid(True)

# plt.grid(True)
plt.tight_layout()
plt.savefig(osp.join("data/plots/", "{}.png".format(args.save_name)))
meta_info = {}
meta_info['data_dir'] = args.data_paths
meta_info['plot_keys'] = plot_keys
with open(osp.join("data/plots/", "{}_plot.json".format(args.save_name)), 'w') as f:
    json.dump(meta_info, f, indent=2, sort_keys=True)
print("saving to", "plot_script.png")
plt.savefig('plot_script.png')
plt.show()