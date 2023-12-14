import os
# os.system("export PYTHONPATH=${PWD}:PYTHONPATH")

import time
import datetime
import json
from launch.utils import check_available_nodes, AUTOBOT_NODELIST, vv_to_params
from chester.run_exp import VariantGenerator

def run_task(vv, available_nodes):
    exp_name = vv['exp_name']
    ts = time.time()
    time_string = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
    log_dir = os.path.join("/project_data/held/yufeiw2/BPref/", "data/local", exp_name + "_" + time_string)
    out_log = os.path.join(log_dir, 'stdout.log')
    err_out = os.path.join(log_dir, 'stdout.err')

    os.makedirs(log_dir, exist_ok=True)
    with open(os.path.join(log_dir, 'variant.json'), 'w') as f:
        json.dump(vv, f, indent=4, sort_keys=True)

    # TODO: generate params, and grab a gpu
    print("available nodes: ", available_nodes)
    print("vv: ", vv)
    # import pdb; pdb.set_trace()
    
    
    for node in available_nodes:
        if node in AUTOBOT_NODELIST:
            gpu_ids = available_nodes[node]
            if len(gpu_ids) > 0:
                vv['cuda_id'] = gpu_ids[0]
                params = vv_to_params(vv, add_cuda_id=True)
                real_node = "autobot-" + node
                command = "ssh -q {} \'{} & nohup singularity exec --bind /project_data/held/yufeiw2/BPref:/mnt/BPref/ --nv /project_data/held/yufeiw2/vlm-reward.sif /mnt/BPref/launch/run_in_singularity_autobot.sh {} > {} 2> {} &\'".format(
                    real_node, "export CUDA_VISIBLE_DEVICES={}".format(gpu_ids[0]),
                    params, out_log, err_out)
                gpu_ids.pop(0)
                print(command)
                # import pdb; pdb.set_trace()
                os.system(command)
                time.sleep(2)
                break

# generate all parameter combinations you want to test
vg = VariantGenerator()
vg.add("env", ['metaworld_button-press-v2', 'metaworld_drawer-close-v2', 'metaworld_handle-press-v2', 'metaworld_door-close-v2', 'metaworld_drawer-open-v2', "metaworld_door-open-v2"])
# vg.add("env", [, 'metaworld_door-open-v2'])
# vg.add("env", ['metaworld_drawer-open-v2'])
vg.add("vlm_label", [0])
vg.add("vlm", ["blip_image_text_matching"])
vg.add("flip_vlm_label", [0])
vg.add("teacher_eps_mistake", [0.3])
vg.add("seed", [1, 2])
# vg.add("reward", ["image_text_matching"])
vg.add("reward", ["learn_from_preference"])
# vg.add("exp_name", ["1215-autobot-gt-preference"])
vg.add("exp_name", ["1215-autobot-gt-preference-0.3-error"])
vg.add("cuda_id", [0])

# for each parameter combination, run the epxeriment
all_vvs = vg.variants()

success = False
while not success:
    # try:
    available_nodes = check_available_nodes()
    success = True
    # except:
    #     print("pickle error, keep trying")
    #     time.sleep(5)
    

for vv in all_vvs:
    run_task(vv, available_nodes)