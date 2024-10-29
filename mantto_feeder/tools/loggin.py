import PySimpleGUI as sg

def login():
    sg.theme('Reddit')
    
    usuarios = {
    "Francisco": 15310,
    "Efrain": 15311,
    "Yamcha": 15312
    }
    # Definir la interfaz de inicio de sesión
    layout = [
        [],
        [sg.Image(r'mantto_feeder\img\loggin.png')],
        [sg.VPush()],
        [sg.Text(' Usuario\t'), sg.Input(key='-USER-',size=(20,1))],
        [sg.Text('Contraseña'), sg.Input(key='-PASSWORD-', password_char='*',size=(20,1))],
        [sg.Button('Iniciar sesión')],
        [sg.VPush()]
    ]

    window = sg.Window('Inicio de sesión', layout,element_justification='center',size=(300,400),return_keyboard_events=True,icon=r"mantto_feeder\img\mantto.ico")

    # Bucle principal para procesar eventos e interactuar con la interfaz
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Cancelar':
            break
        
        if event == '\r':
            # Verificar el usuario y contraseña ingresados
            if values['-USER-'] in usuarios and str(values['-PASSWORD-']) == str(usuarios[values['-USER-']]):
                #sg.popup('Inicio de sesión exitoso')
                inicio_exitoso = True
                popup = sg.popup_ok('Inicio de sesión exitoso')
                break
            else:
                sg.popup_error('Usuario o contraseña incorrectos')
    window.close()

if __name__ == '__main__':
    login()