#!UTC.Monkey.Python.Coddebuging.Circus by Alan.R.G.Systemas c.2023¡#
"""
Funciones_Guardame provee la capacidad de guardar configuraciones para luego utilizarlas 

save_settings guarda en:
    Nombre de Empresa indicada
        Nombre Aplicación indicado
            nombre de diccionario indicado
                clave indicada
                    valor indicado

get_settings  lee el valor guardadp en:
    Nombre de Empresa indicada
        Nombre Aplicación indicado
            nombre de diccionario indicado
                clave indicada

(17.03.2023_Alan.rg.)
"""
from PyQt5 import QtCore

def get_settings(Empresa,NombreApp,dicsetname,clave):
    """
    Lee seteo guardado y lo retorna

    Modo de uso:
        get_settings(Empresa,set,dicsetname,clave)
    
    ante cualquier error retorna False
    """
    settings = QtCore.QSettings(Empresa,NombreApp)
    valuedicset = settings.value(dicsetname)
    print("get_settings read:", valuedicset) 
    try:
        print('read value of: '+str(clave)+' is: '+str(valuedicset[clave]))
        print('read ok')
        return(valuedicset[clave])
    except:
        print('some error raise on get')
        return False
    
def save_settings(Empresa,NombreApp,dicsetname,clave,valor):
    """
    Guarda Seteos

    Modo de uso:
        save_settings(Empresa,set,dicsetname,clave,valor)

    ante cualquier error retorna False
    """
    settings = QtCore.QSettings(Empresa,NombreApp)
    valuedicsets = settings.value(dicsetname) 
    valuedicdef = valuedicsets
    try:
        valuedicsets[clave] = valor
        settings.setValue(dicsetname, valuedicsets)
        print('save ok')
    except:
        print('some error raise on save')
        valuedicdef = {}
        valuedicdef[clave] = valor
        settings.setValue(dicsetname, valuedicdef)
        print('saved new value of: '+str(clave)+' is: '+str(valuedicdef[clave]))
        return 'save new value'
    else:
        #print('esto se ejecuta de todas formas')
        valuedicsets = valuedicdef
    settings.setValue(dicsetname, valuedicdef)
    return(valuedicdef[clave])

'''
#prueba de usabilidad
print('get before command:')
print('on get: ',get_settings('Empresa','NombreApp','dic1','clave1'))
print('on save command:')
print('on save: ',save_settings('Empresa','NombreApp','dic1','clave1','valor1'))
print('get after command:')
print('on get: ',get_settings('Empresa','NombreApp','dic1','clave1'))
'''