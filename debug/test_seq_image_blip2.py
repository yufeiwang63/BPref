from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from vlms.blip_infer_2 import blip2_infer_image_text_matching

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

    return np.concatenate(image_frames, axis=1)
    

# Usage
# gif_path = 'exp/metaworld_sweep-into-v2/vlm0bard_H256_L3_lr0.0003/teacher_b-1_g1_m0_s0_e0/label_smooth_0.0/schedule_0/PEBBLE_init1000_unsup9000_inter2000_maxfeed20000_seg2_acttanh_Rlr0.0003_Rbatch40_Rupdate10_en3_sample0_large_batch10_seed0/eval_gifs/step0990000_episode09.gif'
gif_path = "exp/metaworld_soccer-v2/tune-prompt/2023-12-09-16-54-43/vlm_0bard_H256_L3_lr0.0003/teacher_b-1_g1_m0.3_s0_e0/label_smooth_0.0/schedule_0/PEBBLE_init1000_unsup9000_inter2000_maxfeed20000_seg2_acttanh_Rlr0.0003_Rbatch40_Rupdate10_en3_sample0_large_batch10_seed0/eval_gifs/step0100000_episode05_1589.35.gif"
image1 = extract_and_save_frames(gif_path)
# gif_path = "exp/metaworld_sweep-into-v2/vlm0bard_H256_L3_lr0.0003/teacher_b-1_g1_m0_s0_e0/label_smooth_0.0/schedule_0/PEBBLE_init1000_unsup9000_inter2000_maxfeed20000_seg2_acttanh_Rlr0.0003_Rbatch40_Rupdate10_en3_sample0_large_batch10_seed0/eval_gifs/step0010000_episode00.gif"
gif_path = "exp/metaworld_soccer-v2/tune-prompt/2023-12-09-16-54-43/vlm_0bard_H256_L3_lr0.0003/teacher_b-1_g1_m0.3_s0_e0/label_smooth_0.0/schedule_0/PEBBLE_init1000_unsup9000_inter2000_maxfeed20000_seg2_acttanh_Rlr0.0003_Rbatch40_Rupdate10_en3_sample0_large_batch10_seed0/eval_gifs/step0010000_episode01_6.24.gif"
image2 = extract_and_save_frames(gif_path)

# prompt = "The green cube is approaching the white sphere."
prompt = "The soccer ball is entering the goal gate."

compared_images = np.concatenate([image1, image2], axis=0)
_, matching_cosine_scores = blip2_infer_image_text_matching(image1, image2, prompt, return_scores=True)
print("matching cosine scores: ", matching_cosine_scores)

plt.imshow(compared_images)
plt.show()
