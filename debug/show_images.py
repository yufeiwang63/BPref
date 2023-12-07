import os
import pickle as pkl
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

data_path = "/media/yufei/42b0d2d4-94e0-45f4-9930-4d8222ae63e51/yufei/projects/vlm-reward/data/metaworld_sweep-into-v2-instruct_blip/2023-12-06-18-35-42.pkl"
with open(data_path, "rb") as f:
    data = pkl.load(f)

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
    pil_image1.save("data/image_{}_1.png".format(i))
    pil_image2.save("data/image_{}_2.png".format(i))
    combined_image = Image.fromarray(combined_image)
    combined_image.save("data/image_{}_combined.png".format(i))
    
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