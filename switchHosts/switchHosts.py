import PySimpleGUI as sg
import os.path

hosts_folder = r"C:\Windows\System32\drivers\etc"


def get_file_list(folder):
    try:
        # Get list of files in folder
        file_list = os.listdir(folder)
    except:
        file_list = []
    file_names = [
        f
        for f in file_list
        if os.path.isfile(os.path.join(folder, f))
    ]
    return file_names


def get_file_content(file_path):
    try:
        with open(file_path, mode='r') as f:
            lines = f.readlines()
    except:
        lines = []
    text = ''
    for line in lines:
        text = f'{text}{line}'
    return text


file_list_column = [
    [
        sg.Text("Folder: "),
        sg.In(size=(30, 1), default_text=hosts_folder, enable_events=True, key="-FOLDER-"),
    ],
    [
        sg.Listbox(
            values=get_file_list(hosts_folder), enable_events=True, size=(40, 21), key="-FILE LIST-"
        )
    ],
]

file_viewer_column = [
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Multiline(size=(40, 22), disabled=True, key="-IMAGE-")],
]

# ----- Full layout -----

layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(file_viewer_column),
    ]
]

window = sg.Window("Hosts switch", layout)

# Create an event loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        file_names = get_file_list(folder)
        window["-FILE LIST-"].update(file_names)
    if event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(get_file_content(filename))
        except:
            pass





