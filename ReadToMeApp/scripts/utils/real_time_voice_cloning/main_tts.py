from utils.real_time_voice_cloning.encoder.params_model import model_embedding_size as speaker_embedding_size
from utils.real_time_voice_cloning.utils.argutils import print_args
from utils.real_time_voice_cloning.utils.modelutils import check_model_paths
from utils.real_time_voice_cloning.synthesizer.inference import Synthesizer
from utils.real_time_voice_cloning.encoder import inference as encoder
from utils.real_time_voice_cloning.vocoder import inference as vocoder
from pathlib import Path
import numpy as np
import soundfile as sf
import librosa
import argparse
import torch
import sys
import os
from audioread.exceptions import NoBackendError
from typing import AnyStr
import pathlib

# Info and command-line args
parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-e", "--enc_model_fpath", type=Path, 
                    default="encoder/saved_models/pretrained.pt",
                    help="Path to a saved encoder")
parser.add_argument("-s", "--syn_model_fpath", type=Path, 
                    default="synthesizer/saved_models/pretrained/pretrained.pt",
                    help="Path to a saved synthesizer")
parser.add_argument("-v", "--voc_model_fpath", type=Path, 
                    default="vocoder/saved_models/pretrained/pretrained.pt",
                    help="Path to a saved vocoder")
parser.add_argument("--cpu", action="store_true", help=\
    "If True, processing is done on CPU, even when a GPU is available.")
parser.add_argument("--no_sound", action="store_false", help=\

    "If True, audio won't be played.")
parser.add_argument("--seed", type=int, default=None, help=\
    "Optional random number seed value to make toolbox deterministic.")
parser.add_argument("--no_mp3_support", action="store_true", help=\
    "If True, disallows loading mp3 files to prevent audioread errors when ffmpeg is not installed.")
args = parser.parse_args()
print_args(args, parser)

# Initialize global variables
synthesizer = None
runtime_configured = False

def test_and_load_models():
    '''
    Tests the paths to our models and loads them
    '''

    # Get current directory
    current_directory = pathlib.Path(__file__).parent.resolve()

    print('checking pretrained models...')

    # Check if pretrained models are downloaded
    # check_model_paths(encoder_path=f'{current_directory}/{args.enc_model_fpath}',
    #                   synthesizer_path=f'{current_directory}/{args.syn_model_fpath}',
    #                   vocoder_path=f'{current_directory}/{args.voc_model_fpath}')

    # Load the models one by one.
    print("Preparing the encoder, the synthesizer and the vocoder...")
    encoder.load_model(f'{current_directory}/{args.enc_model_fpath}')
    print('Encoder ready!')
    global synthesizer
    synthesizer = Synthesizer(f'{current_directory}/{args.syn_model_fpath}')
    print('Synthesizer ready!')
    vocoder.load_model(f'{current_directory}/{args.voc_model_fpath}')
    print('Vocoder ready!')


def configure_runtime():
    '''
    Configures the runtime based on command-line args
    '''

    if not args.no_sound:
        import sounddevice as sd
    if args.cpu:
        # Hide GPUs from Pytorch to force CPU processing
        os.environ["CUDA_VISIBLE_DEVICES"] = ""

    test_and_load_models()

    # Update the 'runtime_configured' global variable
    global runtime_configured
    runtime_configured = True

    print("All tests passed! You can now synthesize speech.\n\n")


def tts(input_string: AnyStr, speaker_path: AnyStr, content_name: AnyStr, save_file: bool = True) -> None:
    '''
    Main function used for text-to-speech (TTS)
    '''

    global synthesizer

    # 0. (Optionally) configure runtime
    if not runtime_configured:
        print('Configuring runtime...')
        configure_runtime()
        print('Runtime configured!')

    # 1. Compute the embedding
    print(f'embedding computing with speaker: {speaker_path}')
    preprocessed_wav = encoder.preprocess_wav(speaker_path)
    embed = encoder.embed_utterance(preprocessed_wav)
    print('embedding computed')

    # 2. Compute spectrogram
    # If seed is specified, reset torch seed and force synthesizer reload
    print('computing spectrogram')
    if args.seed is not None:
        print('args.seed isnt none')
        torch.manual_seed(args.seed)
        synthesizer = Synthesizer(args.syn_model_fpath)
    texts = [input_string]
    embeds = [embed]
    print(synthesizer)
    specs = synthesizer.synthesize_spectrograms(texts, embeds)
    spec = specs[0]
    print('spectrogram computed')


    # 3. Synthesize waveform
    # If seed is specified, reset torch seed and reload vocoder
    if args.seed is not None:
        torch.manual_seed(args.seed)
        vocoder.load_model(args.voc_model_fpath)
    generated_wav = vocoder.infer_waveform(spec)
    print('waveform computed')

    # 4. Post-process output
    generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")
    generated_wav = encoder.preprocess_wav(generated_wav)
    print('output post-processed')

    # (Optionally) save audio to disk
    if save_file:
        save_file_dir = "/Users/stephenhgregory/Desktop/ReadToMe/ReadToMeApp/saved_readings/"
        filename = save_file_dir + content_name + "(" + os.path.splitext(os.path.basename(speaker_path))[0] + ")"
        print(generated_wav.dtype)
        sf.write(filename, generated_wav.astype(np.float32), synthesizer.sample_rate)
        print(f"\nSaved output as {filename}\n\n")

    # 5. Play audio
    if not args.no_sound:
        try:
            sd.stop()
            sd.play(generated_wav, synthesizer.sample_rate)
        except sd.PortAudioError as e:
            print("\nCaught exception: %s" % repr(e))
            print("Continuing without audio playback. Suppress this message with the \"--no_sound\" flag.\n")
        except:
            raise

    return