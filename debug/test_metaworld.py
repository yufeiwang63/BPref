import metaworld
import metaworld.envs.mujoco.env_dict as _env_dict
# from metaworld.envs.mujoco import env_dict as _env_dict
from matplotlib import pyplot as plt

env_name = "sweep-into-v2"
env_name = "button-press-v2"
env_name = "drawer-close-v2"
if env_name in _env_dict.ALL_V2_ENVIRONMENTS:
    env_cls = _env_dict.ALL_V2_ENVIRONMENTS[env_name]
else:
    env_cls = _env_dict.ALL_V1_ENVIRONMENTS[env_name]

rgbs = []
camera_names = ["topview", "corner", "corner2", "corner3", "behindGripper", "gripperPOV", env_name]
for camera_name in camera_names:
    env = env_cls(render_mode='rgb_array')
    env.camera_name = camera_name
    env._freeze_rand_vec = False
    env._set_task_called = True

    env.reset()
    rgb = env.render()
    rgbs.append(rgb)
    
    
fig, axes = plt.subplots(1, len(rgbs), figsize=(70, 10))
for i, rgb in enumerate(rgbs):
    axes[i].imshow(rgb[::-1, :, :])
    axes[i].set_title(camera_names[i])
    
plt.show()