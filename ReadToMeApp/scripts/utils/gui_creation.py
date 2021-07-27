''' Contains functions for drawing out components of the ReadToMe GUI '''

import PySimpleGUI as sg
import os.path
from typing import List
from . import gui_logic


def create_main_window_layout() -> List[List]:
    '''
    Creates the layout for the main window of the application
    '''
    # Create the first column 
    ## 1. (the list of voice files)
    voice_file_list_column = create_voice_file_list_column()
    ## 2. (the list of text files)
    text_file_list_column = create_text_file_list_column()
    # Create the second column (just the name of the selected file for now)
    file_viewer_column = create_file_viewer_column()
    
    # Arrange the columns together to create the full layout
    main_window_layout = [
        [
        sg.Column(voice_file_list_column),
        sg.Column(text_file_list_column)
        ],
        # Add a separator for *visual flare*
        sg.VSeperator(),
        [
        sg.Column(file_viewer_column),
        ]
    ]

    return main_window_layout


def create_voice_file_list_column() -> List[List]:
    '''
    Creates the layout for the file list column

    TODO: Totally redo this function and add better docs
    '''

    file_list_column = [
        [
            sg.Text("Voice Folder", justification='center'),
        ],
        [
            sg.Listbox(
                values=gui_logic.filter_voice_sample_file_names('./voice_samples/'), enable_events=True, size=(40, 20), key="-VOICE FILE LIST-"
            ),
            sg.ReadButton('Create New Voice')
        ],
    ]

    return file_list_column

def create_text_file_list_column() -> List[List]:
    '''
    Creates the layout for the file list column

    TODO: Totally redo this function and add better docs
    '''

    file_list_column = [
        [
            sg.Text("Text Folder", justification='center'),
        ],
        [
            sg.Listbox(
                values=gui_logic.filter_text_sample_file_names('./text_samples/'), enable_events=True, size=(40, 20), key="-TEXT FILE LIST-"
            ),
            sg.ReadButton('Create New Voice')
        ],
    ]

    return file_list_column


def create_file_viewer_column() -> List[List]:
    '''
    Creates the layout for the file viewer column

    TODO: Totally redo this function and add better docs
    '''
    # For now, just show the name of the file
    file_viewer_column = [
        [sg.Text("Choose an speaker from list to speak with:")],
        [sg.Text(size=(40, 1), key="-TOUT-")],
        [sg.Image(key="-IMAGE-")],
    ]

    return file_viewer_column