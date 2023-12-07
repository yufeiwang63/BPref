from lavis.models import load_model_and_preprocess
import torch
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model, vis_processors, txt_processors = load_model_and_preprocess(name="blip2_feature_extractor", model_type="pretrain_vitL", is_eval=True, device=device)


def blip2_infer(rgb1, rgb2, text):

    with torch.no_grad():
        text_input = txt_processors["eval"](text)
    
    similarities = []
    for rgb in [rgb1, rgb2]:
        raw_image = Image.fromarray(rgb).convert('RGB')
        
        with torch.no_grad():
            image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)
            sample = {"image": image, "text_input": [text_input]}

            features_image = model.extract_features(sample, mode="image")
            features_text = model.extract_features(sample, mode="text")
            similarity = features_image.image_embeds_proj[:,0,:] @ features_text.text_embeds_proj[:,0,:].t()

        similarities.append(similarity.item())
        
    print(similarities)
    img = np.concatenate([rgb1, rgb2], axis=1)
    plt.imshow(img)
    plt.show()
    
    if similarities[0] > similarities[1]:
        return 0
    else:
        return 1
        
    