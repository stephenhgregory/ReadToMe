import PySimpleGUI as sg
import os.path
from typing import List
from utils import gui_creation, gui_logic


if __name__ == "__main__":
    
    # Create the layout for the main window, ready to be rendered
    main_window_layout = gui_creation.create_main_window_layout()

    # Render that layout onto the window
    main_window = sg.Window("Audio File Player (fix this shitty name)", main_window_layout)

    # Run the Event Loop
    while True:
        gui_logic.run_main_event_loop(main_window)
