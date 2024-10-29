import time as t
import PySimpleGUI as sg

def progress_bar():
    sg.theme('Reddit')
    layout = [[sg.Text('Loading...')],
            [sg.ProgressBar(200, orientation='h', size=(20, 20), key='-PROGBAR-')]],
    window = sg.Window('Working...', layout,no_titlebar=True, grab_anywhere=True)
    for i in range(200):
        event, values = window.read(timeout=1)
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        window['-PROGBAR-'].update_bar(i + 1)
    window.close()
    
if __name__ == '__main__':
    progress_bar()