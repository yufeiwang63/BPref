# The scheduler sweeps over available GPUs for the nodes  in the CHESTER_QUEUE_DIR
import os
import glob
import pickle
import time
from chester import config
from chester.utils_logger import timelog
import sys
import psutil

check_interval = 10  # Check every 10 seconds for available GPUs
user_name = 'yufeiw2'


def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower() and user_name == proc.username():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def check_available_nodes():
    all_stats_path = glob.glob(config.GPU_STATE_DIR + '/*.pkl')
    stats_names = [p.split('/')[-1][:-4] for p in all_stats_path]
    all_stats = [pickle.load(open(p, 'rb')) for p in all_stats_path]
    available_nodes = {}
    for name, (sys_data, gpu_data) in zip(stats_names, all_stats):
        gpu_ids = []
        for i, data in enumerate(gpu_data):
            if len(data['procs']) == 0:  # GPU is available if no user process is found on the GPU
                # if data['mem_usage'] < 20:
                gpu_ids.append(i)
        if len(gpu_ids) > 0:
            available_nodes[name] = gpu_ids
    return available_nodes


if checkIfProcessRunning('remote_scheduler'):
    exit()

if __name__ == '__main__':
    while 1:
        timelog('Scheduler checking available GPUs...')
        # check jobs in the queue
        tasks = glob.glob(os.path.join(config.CHESTER_QUEUE_DIR, '*'))
        tasks_with_time = [(os.path.getmtime(t), t) for t in tasks if os.path.isfile(t)]
        sorted_tasks = sorted(tasks_with_time)
        # check if any GPUs are available
        # available_GPUs = check_available_nodes()  # Dictionary: {node_name, [available_gpu_id])...]
        # # available_GPUs = {'autobot-0-11': [0, 1, 2, 3]}  # Temporary
        # # available_GPUs = {'autobot-0-9': [0, 1, 2, 3],
        # #                   'autobot-0-17': [0, 1, 2, 3]}  # Temporary
        # timelog('Available GPUs: ' + str(available_GPUs))

        success = False
        while not success:
            try:
                available_GPUs = check_available_nodes()  # Dictionary: {node_name, [available_gpu_id])...]
                success = True
            except:
                print("pickle error, keep trying")
                time.sleep(5)

        succ_tasks = 0
        for _, script in sorted_tasks:
            with open(script) as f:
                while True:  # Read header files
                    line = f.readline()
                    if line[0] != '#':
                        break
                    header = line.split(' ')[0][1:]
                    if header == 'CHESTERNODE':
                        node_list = line.rstrip()[13:].split(',')
                    elif header == 'CHESTEROUT':
                        stdout_file = line.rstrip().split(' ')[1]
                    elif header == 'CHESTERERR':
                        stderr_file = line.rstrip().split(' ')[1]
                    elif header == 'CHESTERSCRIPT':
                        script_file = line.rstrip().split(' ')[1]
            for node in node_list:
                real_node = 'autobot-' + node
                # TODO: add gpu num
                if real_node in available_GPUs:
                    gpu_ids = available_GPUs[real_node]
                    if len(gpu_ids) > 0:
                        env_command = f'CUDA_VISIBLE_DEVICES={gpu_ids[0]} '
                        command = f"ssh -q {real_node} \'{env_command} bash {script_file} </dev/null >{stdout_file} 2>{stderr_file} &\'"
                        # command = f"ssh -q {real_node} \'{env_command} python /home/xlin3/test.py </dev/null >{stdout_file} 2>{stderr_file} &\'"
                        rm_command = f'rm {script}'
                        timelog(f"Job launched on node {real_node}, GPU {gpu_ids[0]}, {script_file}")
                        os.system(command)
                        os.system(rm_command)
                        gpu_ids.pop(0)
                        succ_tasks += 1
                        break
                    else:
                        del available_GPUs[real_node]
        if succ_tasks == len(sorted_tasks):
            timelog(f'All {succ_tasks} jobs done!')
            break
        sys.stdout.flush()
        time.sleep(check_interval)
