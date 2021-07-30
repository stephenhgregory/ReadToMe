''' Contains functions for the logic needed to run the GUI of the application '''

import PySimpleGUI as sg
import os
from typing import List, AnyStr
from playsound import playsound
from utils.real_time_voice_cloning import main_tts


def filter_voice_sample_file_names(voice_sample_dir: AnyStr) -> List:
    '''
    Given a directory of voice sample files, returns a list of voice sample names
    with the file extension stripped.

    Parameters:
    -----------
    voice_sample_dir: The directory containing the voice samples

    Returns:
    --------
    A list of voice sample names with their file extensions stripped
    '''
    return [os.path.splitext(filename)[0] for filename in os.listdir(voice_sample_dir) if filename.endswith('.wav')]


def filter_text_sample_file_names(text_sample_dir: AnyStr) -> List:
    '''
    Given a directory of text sample files, returns a list of text sample names
    with the file extension stripped.

    Parameters:
    -----------
    text_sample_dir: The directory containing the text samples

    Returns:
    --------
    A list of text sample names with their file extensions stripped
    '''
    return [os.path.splitext(filename)[0] for filename in os.listdir(text_sample_dir) if filename.endswith('.txt')]


def filter_text_sample_file_name(text_sample_filename: AnyStr) -> AnyStr:
    '''
    Given a text sample file name, strips the file extension and returns the 
    name of a piece of text

    Parameters:
    -----------
    text_sample_filename: The filaneme of the text

    Returns:
    --------
    The name of the piece of text
    '''
    return os.path.splitext(os.path.basename(text_sample_filename))[0]


def filter_voice_sample_file_name(voice_sample_filename: AnyStr) -> AnyStr:
    '''
    Given a a voice sample file name, strips the file extension and returns a 
    speaker's name

    Parameters:
    -----------
    voice_sample_filename: The filanema of the speaker's voice

    Returns:
    --------
    A speaker's name
    '''
    return os.path.splitext(os.path.basename(voice_sample_filename))[0]


def get_image_file_name(wav_filename: AnyStr) -> List:
    '''
    Given a path to a voice sample file, returns the path to an image of the speaker

    Parameters:
    -----------
    wav_filename: The path to the wav file containing a sample voice

    Returns:
    --------
    A filepath to the image corresponding to an image of the speaker
    '''
    return os.path.splitext(wav_filename)[0] + ".png"


def get_text_file_name(text_filename: AnyStr) -> List:
    '''
    Given a path to a text file, returns the true path to the file (with extension)

    Parameters:
    -----------
    text_filename: The path to the text file

    Returns:
    --------
    A filepath to the text (including file extension)
    '''
    return os.path.splitext(text_filename)[0] + ".txt"


def read_text_file(filepath: AnyStr):
    '''
    Given a text file, reads the entire content of the file and returns that
    content as a single string.
    ''' 
    # Open the text file
    text_file = open(filepath, mode='r')
    # read all lines of the text file
    content = text_file.read()
    # close the file
    text_file.close()

    return content



def run_main_event_loop(main_window):
    '''
    Runs the main event loop for the application

    TODO: Better docs

    Parameters:
    -----------
    main_window: The main window for the application

    Returns:
    --------
    None
    '''
    event, values = main_window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        main_window.close()
        exit()
    # Folder name was filled in, so make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = filter_voice_sample_file_names(folder)
        except:
            file_list = []
        main_window["-VOICE FILE LIST-"].update(file_list)

    elif event == "-VOICE FILE LIST-":  # A voice file was chosen from the listbox
        try:
            filename = get_image_file_name(os.path.join('./voice_samples/', values["-VOICE FILE LIST-"][0]))
            main_window["-VOICE NAME-"].update(filter_voice_sample_file_name(filename))
            main_window["-IMAGE-"].update(filename=filename, size=(200, 200))

            # Update the TTS button
            if values["-VOICE FILE LIST-"][0] and values["-TEXT FILE LIST-"][0]:
                main_window["-TTS-"].update(disabled=False)
                print('TTS Button enabled!')

        except:
            pass

    elif event == "-TEXT FILE LIST-":  # A text file was chosen from the listbox
        try:
            filename = get_text_file_name(os.path.join('./text_samples/', values["-TEXT FILE LIST-"][0]))
            print(f'Text File: {filename}')
            print(f'Voice File: {values["-VOICE FILE LIST-"][0]}')
            main_window["-TEXT SCRIPT-"].update(read_text_file(filename))

            # Update the TTS button
            if values["-VOICE FILE LIST-"][0] and values["-TEXT FILE LIST-"][0]:
                main_window["-TTS-"].update(disabled=False)
                print('TTS Button enabled!')

        except: 
            pass

    elif event == "Create New Voice":
        print('\'Create New Voice\' button clicked!')

    elif event == "Create New Text":
        print('\'Create New Text\' button clicked!')
    

    elif event == "-TTS-":
        # Perform TTS
        try:
            # Get path to speaker file
            speaker_path = "./voice_samples/" + values["-VOICE FILE LIST-"][0] + ".wav"
            
            # Get text content for speaker to vocalize
            text_content = read_text_file(get_text_file_name(os.path.join('./text_samples/', values["-TEXT FILE LIST-"][0])))

            # Get content name (for saving the spoken file)
            content_name = values["-TEXT FILE LIST-"][0]

            # Perform TTS
            main_tts.tts(text_content, speaker_path, content_name)

            print("Pressed the Button for TTS!")
            print(main_window["-TEXT SCRIPT-"])
        except:
            pass

    