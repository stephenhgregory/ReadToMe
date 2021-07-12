''' Contains functions for the logic needed to run the GUI of the application '''

import PySimpleGUI as sg
import os.path
from typing import List
from playsound import playsound


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
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".wav", ".mp3", ".m4a"))
        ]
        main_window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            main_window["-TOUT-"].update(filename)
            main_window["-AUDIOFILE-"].update(filename=filename)

        except:
            pass