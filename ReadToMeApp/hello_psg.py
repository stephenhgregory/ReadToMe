import PySimpleGUI as sg

# Create the list which will hold all items in the GUI
layout = []

# Create a piece of text
text_piece = sg.Text("Hello and welcome to ReadToMe")

# Create a button
button = sg.Button("OK")

# Add the text and button to the layout
layout.append([text_piece])
layout.append([button])

# Create the window
window = sg.Window("Demo", layout)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "OK" or event == sg.WIN_CLOSED:
        break

window.close()