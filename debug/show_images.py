import os
import pickle as pkl
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

data_path = "exp/metaworld_sweep-into-v2/tune-prompt/2023-12-07-21-53-37/vlm_1blip_image_text_matching_H256_L3_lr0.0003/teacher_b-1_g1_m0_s0_e0/label_smooth_0.0/schedule_0/PEBBLE_init1000_unsup9000_inter2000_maxfeed20000_seg2_acttanh_Rlr0.0003_Rbatch40_Rupdate10_en3_sample0_large_batch10_seed0/vlm_label_set/2023-12-07-22-45-48.pkl"
with open(data_path, "rb") as f:
    data = pkl.load(f)
save_path = data_path.split("/")[1]
save_path = os.path.join("data", "images", save_path)
if not os.path.exists(save_path):
    os.makedirs(save_path)

images, gt_labels, stored_vlm_labels = data
gt_labels = gt_labels.flatten()
# print(gt_labels)
# exit()
# gt = [0 0 1 0 1 0 0 0 0 0 0 0 0 1 0 0 1 0 0 1]
# gpt4 [- - 1 - 1 - - - - -]

def get_masked_image(image):
    mask = (image[:, :, 0] == 129) & (image[:, :, 1] == 132) & (image[:, :, 2] == 203)
    center = np.argwhere(mask).mean(axis=0).astype(int)
    print(center)
    image = image[center[0]- 150:center[0] + 50, center[1]-100:center[1]+100, :]
    # plt.imshow(image)
    # plt.show()
    return image

correct = 0
for i in range(0, len(images)):
    print(i)
    h, w, c = images[i].shape
    image1 = images[i][:, :w//2, :]
    image2 = images[i][:, w//2:, :]
    combined_image = np.concatenate([image1, image2], axis=1)
    
    pil_image1 = Image.fromarray(image1)
    pil_image2 = Image.fromarray(image2)
    pil_image1.save(f"{save_path}/image_{i}_1.png")
    pil_image2.save(f"{save_path}/image_{i}_2.png")
    combined_image = Image.fromarray(combined_image)
    combined_image.save(f"{save_path}/image_{i}_combined.png")
    
    # plt.imshow(images[i])
    # plt.show()
    correct += (gt_labels[i] == stored_vlm_labels[i])

# print("stored vlm accuracy: ", correct / len(images))
# print("stored vlm accuracy: ", correct / len(images))
# print("stored vlm accuracy: ", correct / len(images))

# 129 132 203
# I will show you two images of the task of cartpole, where a pole is attached to a cart, and the goal is to balance the pole upright on the cart without falling down. The task is considered to be better achieved if the tilt angle of the pole is small from being vertical.
# Please reply which of the two images you think better achieves the goal. 
# In case you think the two images are equally good, please reply equal.
# In case you are not sure, reply with inconclusive. 
# Think step by step.
# Please first reply with your reasoning, and then followed by a single line with "output: first" or "output: second" or "output: equal" or "output: inconclusive".