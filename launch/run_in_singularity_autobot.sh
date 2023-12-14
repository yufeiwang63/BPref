#!/bin/bash

cd /mnt/BPref
export PATH=/opt/miniconda3/bin:$PATH
source /opt/miniconda3/etc/profile.d/conda.sh
conda activate vlm-reward
# cd MetaWorld
# pip install -e .
# cd ..

for i in {22..99}; do
    if ! [ -e /tmp/.X${i}-lock ]; then
        DISPLAY_NUM=$i
        break
    fi
done

# Start Xvfb on the found display number
echo "Starting Xvfb on display ${DISPLAY_NUM}"
Xvfb :${DISPLAY_NUM} -screen 0 1024x768x24 &

# Xvfb -screen 0 1024x768x24 &
# DISPLAY_NUM=$!

# DISPLAY_NUM=22
# mkdir -p /tmp/xvfb-temp-${DISPLAY_NUM}
# Xvfb :${DISPLAY_NUM} -screen 0 1024x768x24 -fp /tmp/xvfb-temp-${DISPLAY_NUM} &


# Export the DISPLAY variable for your jobs
export DISPLAY=:${DISPLAY_NUM}.0

echo "env: $1"
echo "vlm_label: $2"
echo "vlm: $3"
echo "flip_vlm_label: $4"
echo "teacher_eps_mistake: $5"
echo "seed: $6"
echo "reward: $7"
echo "exp_name: $8"


export CUDA_VISIBLE_DEVICES="$9"
python train_PEBBLE.py env="$1" vlm_label="$2" vlm="$3" flip_vlm_label="$4" teacher_eps_mistake="$5" seed="$6" reward="$7" exp_name="$8" segment=2 agent.params.actor_lr=0.0003 agent.params.critic_lr=0.0003 gradient_update=1 activation=tanh num_unsup_steps=9000 num_train_steps=1000000 agent.params.batch_size=512 double_q_critic.params.hidden_dim=256 double_q_critic.params.hidden_depth=3 diag_gaussian_actor.params.hidden_dim=256 diag_gaussian_actor.params.hidden_depth=3 reward_update=10  num_interact=2000 max_feedback=20000 reward_batch=40 reward_update=10 feed_type=0 teacher_beta=-1 teacher_gamma=1 teacher_eps_skip=0 teacher_eps_equal=0