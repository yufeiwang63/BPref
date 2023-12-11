from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

def extract_and_save_frames(gif_path):
    # Open the GIF file
    with Image.open(gif_path) as img:
        # Loop over each frame in the GIF
        num_frames = 5
        interval = img.n_frames // num_frames
        image_frames = []
        for idx in range(num_frames):
            # Select the frame
            img.seek(idx * interval + 1)

            # Save the frame as an individual image
            img_to_save = np.array(img.copy())
            # import pdb; pdb.set_trace()
            image_frames.append(img_to_save)

    return np.array(image_frames)
    

# Usage
gif_path = 'exp/metaworld_sweep-into-v2/vlm0bard_H256_L3_lr0.0003/teacher_b-1_g1_m0_s0_e0/label_smooth_0.0/schedule_0/PEBBLE_init1000_unsup9000_inter2000_maxfeed20000_seg2_acttanh_Rlr0.0003_Rbatch40_Rupdate10_en3_sample0_large_batch10_seed0/eval_gifs/step0990000_episode09.gif'
image1 = extract_and_save_frames(gif_path)
gif_path = "exp/metaworld_sweep-into-v2/vlm0bard_H256_L3_lr0.0003/teacher_b-1_g1_m0_s0_e0/label_smooth_0.0/schedule_0/PEBBLE_init1000_unsup9000_inter2000_maxfeed20000_seg2_acttanh_Rlr0.0003_Rbatch40_Rupdate10_en3_sample0_large_batch10_seed0/eval_gifs/step0010000_episode00.gif"
image2 = extract_and_save_frames(gif_path)

prompt = "The green cube is approaching the white sphere."

import pdb; pdb.set_trace()
compared_images = np.concatenate([image1[None, :, :, :, :], image2[None, :, :, :, :]], axis=0)

new_images1 = np.array([np.concatenate(x, axis=1) for x in compared_images])

batch_size, horizon, image_height, image_width, _ = compared_images.shape
transposed_images = np.transpose(compared_images, (0, 2, 1, 3, 4))
# Reshape to shape: batch_size x image_height x (time_horizon * image_width) x 3
new_images = transposed_images.reshape(batch_size, image_height, horizon * image_width, 3)

assert np.all(new_images1 == new_images)



plt.imshow(new_images[1])
plt.show()
