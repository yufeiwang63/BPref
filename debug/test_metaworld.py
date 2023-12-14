import metaworld
import metaworld.envs.mujoco.env_dict as _env_dict
# from metaworld.envs.mujoco import env_dict as _env_dict
from matplotlib import pyplot as plt

# env_name = "sweep-into-v2"
# # env_name = "button-press-v2"
# # env_name = "drawer-close-v2"
# env_name = "drawer-open-v2"
# env_name = "door-close-v2"
env_name = "door-open-v2"
# env_name = "soccer-v2"
# env_name = "handle-press-v2"
# env_name = "drawer-open-v2"

# for env_name in _env_dict.ALL_V2_ENVIRONMENTS.keys():
# env_name = "basketball-v2"
if env_name in _env_dict.ALL_V2_ENVIRONMENTS:
    env_cls = _env_dict.ALL_V2_ENVIRONMENTS[env_name]
else:
    env_cls = _env_dict.ALL_V1_ENVIRONMENTS[env_name]

env_rgb = None
camera_names = ["topview", "corner", "corner2", "corner3", "behindGripper", "gripperPOV", env_name]
env = env_cls(render_mode='rgb_array')
for _ in range(1):
    rgbs = []
    for camera_name in camera_names:
        env.camera_name = camera_name
        env._freeze_rand_vec = False
        env._set_task_called = True

        env.reset()
        rgb = env.render()
        # if "handle" in env_name:
        #     rgb = rgb[100:400, 100:400, :]
        rgbs.append(rgb)

        if camera_name == env_name:
            env_rgb = rgb
        
        
    fig, axes = plt.subplots(1, len(rgbs), figsize=(70, 10))
    for i, rgb in enumerate(rgbs):
        axes[i].imshow(rgb[::-1, :, :])
        axes[i].set_title(camera_names[i])
        
    # plt.title(env_name)
    # plt.show()


# import torch
# from PIL import Image
# import requests
# from lavis.models import load_model_and_preprocess

# raw_image = Image.fromarray(env_rgb[::-1, :, :]).convert("RGB")
# device = torch.device("cuda") if torch.cuda.is_available() else "cpu"
# model, vis_processors, _ = load_model_and_preprocess(
#     name="blip2_t5", model_type="pretrain_flant5xl", is_eval=True, device=device
# )

# image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)
# caption = model.generate({"image": image})
# print(caption)
# plt.imshow(env_rgb[::-1, :, :])
# plt.title(caption)
# plt.show()
