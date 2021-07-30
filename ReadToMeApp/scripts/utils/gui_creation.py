''' Contains functions for drawing out components of the ReadToMe GUI '''

import PySimpleGUI as sg
import os.path
from typing import List
from . import gui_logic


def create_main_window_layout() -> List[List]:
    '''
    Creates the layout for the main window of the application
    '''
    # Create the first column containing voice files and text files
    file_list_column = create_file_list_column()
    # Create the second column (just the name of the selected file for now)
    file_viewer_column = create_file_viewer_column()
    
    # Arrange the columns together to create the full layout
    main_window_layout = [
        [
        sg.Column(file_list_column),
        # Add a separator for *visual flare*
        sg.VSeparator(),
        sg.Column(file_viewer_column),
        ]
    ]

    return main_window_layout


def create_file_list_column() -> List[List]:
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
        [
            sg.Text("Text Folder", justification='center'),
        ],
        [
            sg.Listbox(
                values=gui_logic.filter_text_sample_file_names('./text_samples/'), enable_events=True, size=(40, 20), key="-TEXT FILE LIST-"
            ),
            sg.ReadButton('Create New Text')
        ],
    ]

    return file_list_column

# def create_text_file_list_column() -> List[List]:
#     '''
#     Creates the layout for the file list column

#     TODO: Totally redo this function and add better docs
#     '''

#     file_list_column = [
#         [
#             sg.Text("Text Folder", justification='center'),
#         ],
#         [
#             sg.Listbox(
#                 values=gui_logic.filter_text_sample_file_names('./text_samples/'), enable_events=True, size=(40, 20), key="-TEXT FILE LIST-"
#             ),
#             sg.ReadButton('Create New Text')
#         ],
#     ]

#     return file_list_column


def create_file_viewer_column() -> List[List]:
    '''
    Creates the layout for the text and voice column
    '''
    file_viewer_column = [
        [sg.Text("Choose a speaker from list to speak with:")],
        [sg.Text(size=(40, 1), key="-VOICE NAME-")],
        [sg.Image(key="-IMAGE-")],
        [sg.Text("Choose a text from list to speak with:")],
        [sg.Text(key="-TEXT SCRIPT-", size=(50, 50), auto_size_text=True)],
        [sg.Button("Speak", key="-TTS-", disabled=True)],
    ]

    return file_viewer_column