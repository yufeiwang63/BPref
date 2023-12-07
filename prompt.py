env_prompts = {
    "metaworld_sweep-into-v2": 
#         """
# There are two sub-images in the image, one on the left, and one on the right.
# They are both about a sawyer robot performing the task of "sweep cube into hole", where the robot needs to sweep the small brown cube into the hole (location indicated by a small blue sphere). The closer the cube is to the hole, the better the task is considered to be achieved.
# Please reply which of the two sub-images you think better achieves the goal.
# Think step by step.
# Please first reply with your reasoning, and then followed by a single line with "output: left" or "output: right".

# Example output format:
# I think the left sub-image is better because the cube is very close to the hole, while in the rigt sub-image the cube if further away from the hole. [More reasoning here]
# output: left

# Another example output format:
# I think the right sub-image is better because the cube closer to the hole compared to the left image. [More reasoning here]
# output: right
# """,
"""
Is the green cube in closer position to the white sphere in the left or right sub-image?
""",

    "metaworld_button-press-v2":
"""
Is the button fully pressed in the left or right sub-image?
""",

"metaworld_drawer-close-v2": "Is the green drawer fully closed in the left or right sub-image?",

    # use multiple prompts which change slightly from each other for the same env to avoid being banned by bard
    "CartPole-v1": ["""
There are two cartpoles in the image, one on the left, and one on the right.
They are both about the task of cartpole, where a pole (represented as the brown stick) is attached to a cart (represented as the black rectangle), and the goal is to balance the pole upright on the cart without falling down. The task is considered to be better achieved if the tilt angle of the pole is small from being upright vertical.
Please reply which of the two cartpoles you think better achieves the goal.
Think step by step.
Please first reply with your reasoning, and then followed by a single line with "output: left" or "output: right".

Example:
Input: [image where the right pole is downwards], There are two cartpoles ...

Output:
I think the left cartpole is better because it has a smaller tilt angle. [More reasoning here]
output: left
""",

"""
There are two cartpoles in the image, one cartpole is on the left, and another is on the right.
They are both about the task of "balancing the cartpole", where a pole (represented as the brown stick) is attached to a cart (represented as the black rectangle), and the goal is to balance the pole upright on the cart without falling down. The task is considered to be better achieved if the tilt angle of the pole is small from being upright vertical.
Please response which of the two cartpoles you think better achieves the goal.
Please Think step by step.
Please first reply with your reasoning, and then followed by a single line with "output: left" or "output: right".

Example:
Input: [image where the right pole is downwards], There are two cartpoles ...

Output:
I think the left cartpole is better because it has a smaller tilt angle. [More reasoning here]
output: left
""",

"""
There are two cartpoles in the image, one cartpole is on the left, and another is on the right.
They are both about the task of "balancing the cartpole", where a pole (represented as the brown stick) is attached to a cart (represented as the black rectangle), and the goal is to balance the pole upright on the cart without falling down. The task is considered to be better achieved if the tilt angle of the pole is small from being upright vertical.
Please response which of the two cartpoles you think better achieves the goal.
Please Think step by step.
Please first reply with your reasoning, and then followed by a single line with "output: left" or "output: right".

Example:
Input: [image where the left pole is tilting towards left], There are two cartpoles ...

Output:
I think the right cartpole is better because it is more upright compared to the left one, which is tileting towards left. [More reasoning here]
output: right
""",
    ]
}


clip_env_prompts = {
    "CartPole-v1": "The brown stick is vertically upright on the black rectangle.",
    # "metaworld_sweep-into-v2": "The green cube is very close to the hole (indicated by the white sphere) on the table.",
    # "metaworld_sweep-into-v2": "The position of the green cube is very close to the position of the white sphere.",
    "metaworld_sweep-into-v2": "The green cube is close to the white sphere.",
    "metaworld_button-press-v2": "The red button is fully pressed.",
    "metaworld_drawer-close-v2": "The green drawer is fully closed.",
}