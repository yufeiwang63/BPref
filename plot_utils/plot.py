import pandas as pd

csvs = [
    # "./exp/CartPole-v1/vlm0_H256_L3_lr0.0003/teacher_b-1_g1_m0_s0_e0/label_smooth_0.0/schedule_0/PEBBLE_init1000_unsup1000_inter1000_maxfeed20000_seg1_acttanh_Rlr0.0003_Rbatch40_Rupdate10_en3_sample0_large_batch10_seed0/eval.csv",
    # "./exp/CartPole-v1/vlm0_H256_L3_lr0.0003/teacher_b-1_g1_m0.1_s0_e0/label_smooth_0.0/schedule_0/PEBBLE_init1000_unsup1000_inter1000_maxfeed20000_seg1_acttanh_Rlr0.0003_Rbatch40_Rupdate10_en3_sample0_large_batch10_seed0/eval.csv",
    # "./exp/CartPole-v1/vlm0_H256_L3_lr0.0003/teacher_b-1_g1_m0.2_s0_e0/label_smooth_0.0/schedule_0/PEBBLE_init1000_unsup1000_inter1000_maxfeed20000_seg1_acttanh_Rlr0.0003_Rbatch40_Rupdate10_en3_sample0_large_batch10_seed0/eval.csv",
    # "./exp/CartPole-v1/vlm0_H256_L3_lr0.0003/teacher_b-1_g1_m0.3_s0_e0/label_smooth_0.0/schedule_0/PEBBLE_init1000_unsup1000_inter1000_maxfeed20000_seg1_acttanh_Rlr0.0003_Rbatch40_Rupdate10_en3_sample0_large_batch10_seed0/eval.csv",
    # "./exp/CartPole-v1/vlm0_H256_L3_lr0.0003/teacher_b-1_g1_m0.4_s0_e0/label_smooth_0.0/schedule_0/PEBBLE_init1000_unsup1000_inter1000_maxfeed20000_seg1_acttanh_Rlr0.0003_Rbatch40_Rupdate10_en3_sample0_large_batch10_seed0/eval.csv",
    # "exp/metaworld_sweep-into-v2/vlm1blip_image_text_matching_H256_L3_lr0.0003/teacher_b-1_g1_m0_s0_e0/label_smooth_0.0/schedule_0/PEBBLE_init1000_unsup9000_inter2000_maxfeed20000_seg2_acttanh_Rlr0.0003_Rbatch40_Rupdate10_en3_sample0_large_batch10_seed0/train.csv"
"exp/metaworld_sweep-into-v2/vlm1blip_H256_L3_lr0.0003/teacher_b-1_g1_m0_s0_e0/label_smooth_0.0/schedule_0/PEBBLE_init1000_unsup9000_inter2000_maxfeed20000_seg2_acttanh_Rlr0.0003_Rbatch40_Rupdate10_en3_sample0_large_batch10_seed0/train.csv"
]

# labels = [
#     "error = 0",
#     "error = 0.1",
#     "error = 0.2",
#     "error = 0.3",
#     "error = 0.4",
# ]

import matplotlib.pyplot as plt
# plt.ylim(-200, 0)
for idx, csv in enumerate(csvs):
    df = pd.read_csv(csv)
    # get the column of "success_rate"
    success_rate = df["vlm_acc"].values
    success_rate = [x for x in success_rate if x != 0]
    print("average success rate: ", sum(success_rate) / len(success_rate))

    # plot the success rate
    
    # plt.plot(success_rate, label=labels[idx])
    plt.plot(success_rate)
    plt.axhline(y=0.5, color='r', linestyle='-')


plt.legend()
plt.xlabel("Number of training episodes")
plt.ylabel("true episode reward")    
plt.savefig("cartpole-error.png")
plt.show()  