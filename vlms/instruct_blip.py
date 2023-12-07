import torch
from PIL import Image
from matplotlib import pyplot as plt
from lavis.models import load_model_and_preprocess

# setup device to use
device = torch.device("cuda") if torch.cuda.is_available() else "cpu"
model, vis_processors, _ = load_model_and_preprocess(name="blip2_vicuna_instruct", model_type="vicuna7b", is_eval=True, device=device)


def instructblip_infer(combined_image, prompt):
    # loads InstructBLIP model
    # prepare the image
    
    combined_image = Image.fromarray(combined_image).convert("RGB")
    image = vis_processors["eval"](combined_image).unsqueeze(0).to(device)

    res = model.generate({"image": image, "prompt": prompt})

    # plt.imshow(combined_image)
    # plt.show()
    # print(res)
    
    if "left" in res:
        return 0
    else:
        return 1