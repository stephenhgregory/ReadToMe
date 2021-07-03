''' Contains functions for drawing out components of the ReadToMe GUI '''

import PySimpleGUI as sg
import os.path
from typing import List


def create_main_window_layout() -> List[List]:
    '''
    Creates the layout for the main window of the application
    '''
    # Create the first column (the list of files)
    file_list_column = create_file_list_column()
    # Create the second column (just the name of the selected file for now)
    file_viewer_column = create_file_viewer_column()
    
    # Arrange the columns together to create the full layout
    main_window_layout = [
        [
        sg.Column(file_list_column),
        # Add a separator for *visual flare*
        sg.VSeperator(),
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
        sg.Text("Audio File Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
        ],
        [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
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
        [sg.Text("Choose an audio file from list on left:")],
        [sg.Text(size=(40, 1), key="-TOUT-")],
        [sg.Image(key="-AUDIOFILE-")],
    ]

    return file_viewer_column