import PySimpleGUI as sg
import pandas as pd


def user(id_tech:str):
    user = pd.read_csv(r'H:\Ingenieria\Ensamble PCB\Documentacion ISO-9001\TEC.csv',encoding='ISO-8859-1',usecols=['EMPLEADO','NOMBRE'])
    df_user = pd.DataFrame(user)
    #renmbrar columnas
    df_user.rename(columns={'EMPLEADO':'ID_Tecnico'},inplace=True)
    df_user.rename(columns={'NOMBRE':'Tecnico'},inplace=True)
    #print(df_user)
    if id_tech in df_user['ID_Tecnico'].values:
        #print('Técnico encontrado')
        busqueda = df_user.loc[df_user['ID_Tecnico'] == id_tech].to_string(index = False)
        busqueda_s = busqueda.split()[3:]
        resultado = ""
        for item in busqueda_s:
            resultado += item + " "
        return resultado

#print(user("015310A"))