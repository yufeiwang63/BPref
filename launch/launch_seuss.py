import os
import json
import time
import click
import socket
from chester.run_exp import run_experiment_lite, VariantGenerator
from launch.utils import vv_to_params

@click.command()
@click.argument('mode', type=str, default='local')
@click.option('--debug/--no-debug', default=True)
@click.option('--dry/--no-dry', default=False)
def main(mode, debug, dry):\
    

    exp_prefix = "1214-metaworld-tasks"
    vg = VariantGenerator()

    vg.add("env", ['metaworld_button-press-v2', 'metaworld_drawer-close-v2', 'metaworld_handle-press-v2', 'metaworld_door-close-v2'])
    # vg.add("env", ['metaworld_drawer-open-v2', 'metaworld_door-open-v2'])
    vg.add("vlm_label", [1])
    vg.add("vlm", ["blip_image_text_matching"])
    vg.add("flip_vlm_label", [0])
    vg.add("teacher_eps_mistake", [0])
    vg.add("seed", [1, 2])
    vg.add("reward", ["learn_from_preference"])
    vg.add("exp_name", ["1215-seuss_blip2_multiple_seeds"])
    
    print('Number of configurations: ', len(vg.variants()))
    print("exp_prefix: ", exp_prefix)

    variations = set(vg.variations())
    task_per_gpu = 1
    all_vvs = vg.variants()
    slurm_nums = len(all_vvs) // task_per_gpu
    if len(all_vvs) % task_per_gpu != 0:
        slurm_nums += 1

    sub_process_popens = []
    
    target_method = run_task if mode == 'seuss' else run_task_local
    for idx in range(slurm_nums):
        beg = idx * task_per_gpu
        end = min((idx+1) * task_per_gpu, len(all_vvs))
        vvs = all_vvs[beg:end]
    # for idx, vv in enumerate(vg.variants()):
        while len(sub_process_popens) >= 10:
            sub_process_popens = [x for x in sub_process_popens if x.poll() is None]
            time.sleep(10)
        compile_script = wait_compile = None
        env_var = None
        
        cur_popen = run_experiment_lite(
            stub_method_call=target_method,
            variants=vvs,
            # variant=vv,
            mode=mode,
            dry=dry,
            use_gpu=True,
            exp_prefix=exp_prefix,
            wait_subprocess=debug,
            compile_script=compile_script,
            wait_compile=wait_compile,
            env=env_var,
            variations=variations,
            task_per_gpu=task_per_gpu
        )
        if cur_popen is not None:
            sub_process_popens.append(cur_popen)
        if debug:
            break

        time.sleep(10)

def run_task(vv, log_dir=None, exp_name=None):
    os.makedirs(log_dir, exist_ok=True)
    with open(os.path.join(log_dir, 'variant.json'), 'w') as f:
        json.dump(vv, f, indent=2, sort_keys=True)
    
    params = vv_to_params(vv)
    command = "singularity exec --bind /data/yufeiw2/BPref:/mnt/BPref/ --nv /data/yufeiw2/vlm-reward.sif /mnt/BPref/launch/run_in_singularity.sh {}".format(params)
    os.system(command)
    
def run_task_local(vv, log_dir=None, exp_name=None):
    os.makedirs(log_dir, exist_ok=True)
    with open(os.path.join(log_dir, 'variant.json'), 'w') as f:
        json.dump(vv, f, indent=2, sort_keys=True)
    
    # rel_path = os.path.relpath(log_dir, os.getcwd())
    params = vv_to_params(vv)
    
    command = "singularity exec --bind ./:/mnt/BPref/ --nv /media/yufei/42b0d2d4-94e0-45f4-9930-4d8222ae63e51/yufei/projects/singularity_images/vlm-reward/vlm-reward.sif /mnt/BPref/launch/run_in_singularity.sh {}".format(params)
    # command = "singularity exec --bind ./:/mnt/BPref/ --nv /data/yufeiw2/vlm-reward.sif /mnt/BPref/launch/run_in_singularity.sh {}".format(params)
    print(command)
    os.system(command)

if __name__ == '__main__':
    # first rscyn code
    
    main()


