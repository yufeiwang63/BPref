
from PIL import Image

def extract_and_save_frames(gif_path, output_folder):
    # Open the GIF file
    with Image.open(gif_path) as img:
        # Loop over each frame in the GIF
        num_frames = 5
        interval = img.n_frames // num_frames
        for idx in range(num_frames):
            # Select the frame
            img.seek(idx * interval)

            # Save the frame as an individual image
            frame_path = f"{output_folder}_frame_{idx * interval}.png"
            img.save(frame_path)

# Usage
gif_path = 'exp/metaworld_sweep-into-v2/vlm0bard_H256_L3_lr0.0003/teacher_b-1_g1_m0_s0_e0/label_smooth_0.0/schedule_0/PEBBLE_init1000_unsup9000_inter2000_maxfeed20000_seg2_acttanh_Rlr0.0003_Rbatch40_Rupdate10_en3_sample0_large_batch10_seed0/eval_gifs/step0990000_episode09.gif'
gif_path = "exp/metaworld_sweep-into-v2/vlm0bard_H256_L3_lr0.0003/teacher_b-1_g1_m0_s0_e0/label_smooth_0.0/schedule_0/PEBBLE_init1000_unsup9000_inter2000_maxfeed20000_seg2_acttanh_Rlr0.0003_Rbatch40_Rupdate10_en3_sample0_large_batch10_seed0/eval_gifs/step0010000_episode00.gif"
output_folder = gif_path[:-4]
extract_and_save_frames(gif_path, output_folder)
