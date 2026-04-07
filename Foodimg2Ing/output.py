import torch
import torch.nn as nn
import numpy as np
import os
import pickle
import time
from PIL import Image
from torchvision import transforms
from Foodimg2Ing.args import get_parser
from Foodimg2Ing.model import get_model
from Foodimg2Ing.utils.output_utils import prepare_output
from Foodimg2Ing import app

# --- GLOBAL SETUP (Runs only once on startup) ---
data_dir = os.path.join(app.root_path, 'data')
use_gpu = True
device = torch.device('cuda' if torch.cuda.is_available() and use_gpu else 'cpu')
map_loc = None if torch.cuda.is_available() and use_gpu else 'cpu'

# Load Vocabularies
ingrs_vocab = pickle.load(open(os.path.join(data_dir, 'ingr_vocab.pkl'), 'rb'))
vocab = pickle.load(open(os.path.join(data_dir, 'instr_vocab.pkl'), 'rb'))

ingr_vocab_size = len(ingrs_vocab)
instrs_vocab_size = len(vocab)

# Initialize Model Architecture
import sys; sys.argv=['']; del sys
args = get_parser()
args.maxseqlen = 15
args.ingrs_only = False
model = get_model(args, ingr_vocab_size, instrs_vocab_size)

# Load Pre-trained Weights into RAM
model_path = os.path.join(data_dir, 'modelbest.ckpt')
model.load_state_dict(torch.load(model_path, map_location=map_loc, weights_only=False))
model.to(device)
model.eval()

# Pre-define Image Transforms
to_input_transf = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
])

img_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224)
])

def output(uploadedfile):
    # SPEED HACK: Only one greedy pass (True) instead of a list of two
    greedy = [True] 
    beam = [-1]
    temperature = 1.0
    show_anyways = True 

    # Load and process image
    img = Image.open(uploadedfile).convert('RGB')
    image_transf = img_transform(img)
    image_tensor = to_input_transf(image_transf).unsqueeze(0).to(device)

    title, ingredients, recipe = [], [], []

    # Single pass loop for maximum speed
    for i in range(len(greedy)):
        with torch.no_grad():
            outputs = model.sample(image_tensor, greedy=greedy[i], 
                                 temperature=temperature, beam=beam[i], true_ingrs=None)
                
        ingr_ids = outputs['ingr_ids'].cpu().numpy()
        recipe_ids = outputs['recipe_ids'].cpu().numpy()
                
        outs, valid = prepare_output(recipe_ids[0], ingr_ids[0], ingrs_vocab, vocab)
            
        if valid['is_valid'] or show_anyways:
            title.append(outs['title'])
            ingredients.append(outs['ingrs'])
            recipe.append(outs['recipe'])
            
    return title, ingredients, recipe