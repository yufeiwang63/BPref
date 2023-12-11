import torch
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np

from lavis.models import load_model_and_preprocess
from lavis.processors import load_processor

device = torch.device("cuda") if torch.cuda.is_available() else "cpu"
model, vis_processors, text_processors = load_model_and_preprocess("blip2_image_text_matching", "pretrain_vitL", device=device, is_eval=True)


def blip2_infer_image_text_matching(rgb1, rgb2, text, use_prob=False, return_scores=False):

    caption = text
    with torch.no_grad():
        txt = text_processors["eval"](caption)

    matching_probabilities = []
    matching_cosine_scores = []
    for rgb in [rgb1, rgb2]:
        raw_image = Image.fromarray(rgb).convert("RGB")
        img = vis_processors["eval"](raw_image).unsqueeze(0).to(device)

        itm_output = model({"image": img, "text_input": txt}, match_head="itm")
        itm_scores = torch.nn.functional.softmax(itm_output, dim=1)
        itm_score = itm_scores[:, 1].item()
        # print(f'The image and text are matched with a probability of {itm_score:.3%}')
        matching_probabilities.append(itm_score)

        itc_score = model({"image": img, "text_input": txt}, match_head='itc')
        # print('The image feature and text feature has a cosine similarity of %.4f'%itc_score)
        matching_cosine_scores.append(itc_score)
        
    # print("matching probalities:", matching_probabilities)
    # print("matching cosine scores: ", matching_cosine_scores)
    # img = np.concatenate([rgb1, rgb2], axis=1)
    # plt.imshow(img)
    # plt.show()
    
    if not return_scores:
        if use_prob:
            if matching_probabilities[0] > matching_probabilities[1]:
                return 0
            elif matching_probabilities[0] < matching_probabilities[1]:
                return 1
            else:
                return -1
        else:
            if matching_cosine_scores[0] > matching_cosine_scores[1]:
                return 0
            elif matching_cosine_scores[0] < matching_cosine_scores[1]:
                return 1
            else:
                return -1
    else:
        return matching_probabilities, matching_cosine_scores
    