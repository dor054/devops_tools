import PySimpleGUI as sg
import os.path
import shutil

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


def replace_file(orig_file, new_file):
    if os.path.exists(orig_file) and os.path.exists(new_file):
        if os.path.samefile(orig_file, new_file):
            # Same file
            return
        else:
            os.remove(orig_file)
            shutil.copy(new_file, orig_file)


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
    [
        sg.Button("Replace hosts file", disabled=True, key="-REPLACE BUTTON-")
    ]
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
            window["-REPLACE BUTTON-"].update(disabled=False)
        except:
            pass
    if event == "-REPLACE BUTTON-":
        ch = sg.popup_yes_no(f'Are you sure you want to replace hosts by {values["-FILE LIST-"][0]}?', no_titlebar=True)
        if ch == "Yes":
            new_file = filename
            orig_file = os.path.join(values["-FOLDER-"], "hosts")
            replace_file(orig_file, new_file)
            file_names = get_file_list(values["-FOLDER-"])
            window["-FILE LIST-"].update(file_names)
        if ch == "No":
            pass






