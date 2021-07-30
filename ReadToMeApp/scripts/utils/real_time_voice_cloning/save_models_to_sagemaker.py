""" This file is used to save models to Amazon AWS sagemaker for deployment """

import argparse
import os
import torch

if __name__=='__main__':
    # default to the value in environment variable `SM_MODEL_DIR`. Using args makes the script more portable.
    parser.add_argument('--encoder_model_dir', type=str, default=os.environ['ENCODER_SM_MODEL_DIR'])
    parser.add_argument('--synthesizer_model_dir', type=str, default=os.environ['SYNTHESIZER_SM_MODEL_DIR'])
    parser.add_argument('--vocoder_model_dir', type=str, default=os.environ['VOCODER_SM_MODEL_DIR'])
    args, _ = parser.parse_known_args()

    # ... Save the trained encoder to 'encoder_model_dir'
    with open(os.path.join(args.encoder_model_dir, 'pretrained.pt'), 'wb') as f:
        torch.save(model.state_dict(), f)

    # ... Save the trained synthesizer to 'synthesizer_model_dir'
    with open(os.path.join(args.synthesizer_model_dir, 'pretrained.pt'), 'wb') as f:
        torch.save(model.state_dict(), f)

    # ... Save the trained vocoder to 'vocoder_model_dir'
    with open(os.path.join(args.vocoder_model_dir, 'pretrained.pt'), 'wb') as f:
        torch.save(model.state_dict(), f)