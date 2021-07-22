''' Contains functions for the logic needed to run the GUI of the application '''

import PySimpleGUI as sg
import os
from typing import List, AnyStr
from playsound import playsound


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
    return os.path.splitext(wav_filename)[0] + ".jpeg"


def run_main_event_loop(main_window):
    '''
    Runs the main event loop for the application

    TODO: Better docs

    Parameters:
    main_window: The main window for the application

    Returns:
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
        main_window["-FILE LIST-"].update(file_list)

    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = get_image_file_name(os.path.join('./voice_samples/', values["-FILE LIST-"][0]))
            main_window["-TOUT-"].update(filename)
            main_window["-IMAGE-"].update(filename=filename)

        except:
            pass

    elif event == "Create New Voice":
        print('\'Create new voice\' button clicked!')