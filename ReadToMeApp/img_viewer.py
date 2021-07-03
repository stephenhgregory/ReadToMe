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
        # Add a seperator for *visual flare*
        sg.VSeperator(),
        sg.Column(image_viewer_column),
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


# First the window layout in 2 columns

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

# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text("Choose an audio file from list on left:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-AUDIOFILE-")],
]

# Create the full layout
layout = [
    [
        sg.Column(file_list_column),
        # sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]


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
            and f.lower().endswith((".png", ".gif"))
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



if __name__ == "__main__":
    # Create the layout for the main window, ready to be rendered
    main_window_layout = create_main_window_layout()

    # Render that layout onto the window
    main_window = sg.Window("Audio File Player (fix this shitty name)", main_window_layout)

    # Run the Event Loop
    while True:

        run_main_event_loop(main_window)

        # TODO: Delete all of this ##################################################
        # event, values = main_window.read()
        # if event == "Exit" or event == sg.WIN_CLOSED:
        #     break
        # # Folder name was filled in, make a list of files in the folder
        # if event == "-FOLDER-":
        #     folder = values["-FOLDER-"]
        #     try:
        #         # Get list of files in folder
        #         file_list = os.listdir(folder)
        #     except:
        #         file_list = []

        #     fnames = [
        #         f
        #         for f in file_list
        #         if os.path.isfile(os.path.join(folder, f))
        #         and f.lower().endswith((".png", ".gif"))
        #     ]
        #     main_window["-FILE LIST-"].update(fnames)
        # elif event == "-FILE LIST-":  # A file was chosen from the listbox
        #     try:
        #         filename = os.path.join(
        #             values["-FOLDER-"], values["-FILE LIST-"][0]
        #         )
        #         main_window["-TOUT-"].update(filename)
        #         main_window["-AUDIOFILE-"].update(filename=filename)

        #     except:
        #         pass
        #############################################################################

    # main_window.close()


