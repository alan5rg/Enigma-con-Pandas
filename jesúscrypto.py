"""
    La libreria jesúscrypto provee funciones omnicientes y todopoderosas para EnigmaConPandas
    y otras aplicaciones que puedan y quieran escuchar a cristo Jesús y salvar sus almas!!!
"""
import cryptocode, pickle #run pip install cryptocode

def encryConkey(eldato, llave):
    """
        Encripta un string con la llave indicada por medio de la libreria crytptocode
        y lo devuelve encriptado
    
        Uso:
            encryConkey('string', 'llave')
    """
    #print('Encriptando...')
    return (cryptocode.encrypt(eldato, llave))

def decryConkey(eldato, llave):
    """
        Desencripta un string encriptado solo con la llave correcta indicada 
        utilizando la libreria crytptocode y lo devuelve desencriptado
    
        Uso:
            decryConkey('string', 'llave')
    """
    #print('Desencriptando...')
    return (cryptocode.decrypt(eldato, llave))

def encriptaDixy(dixy, llave):
    """
        Encripta un diccionario con la llave indicada por medio de la libreria crytptocode
        y lo devuelve encriptado
    
        Uso:
            encriptaDixy('diccionario', 'llave')
    """
    print('Encriptando...')
    for clave in dixy:
        for i in range (len(dixy[clave])):
            valorencriptado=encryConkey((dixy[clave][i]),llave)
            #print(valorencriptado) #para debug
            dixy[clave][i]=valorencriptado
    dixycrypto=dixy
    print('Encriptado!')
    return dixycrypto

def desencriptaDixy(dixy, llave):
    """
        Desencripta un diccionario solo con la llave correcta indicada utilizando
        la libreria crytptocode y lo devuelve desencriptado
    
        Uso:
            desencriptaDixy('diccionario', 'llave')
    """
    print('Desencriptando...')
    for clave in dixy:
        for i in range (len(dixy[clave])):
            valordesencriptado=decryConkey((dixy[clave][i]),llave)
            #print(valordesencriptado) #para debug
            dixy[clave][i]=valordesencriptado
    dixydecrypto=dixy
    print('Desencriptado!')    
    return dixydecrypto

def guardarArchivo(archivo, lo_que_sea):
    """
        Guarda en el archivo indicado lo que sea que se le envie de forma serializada
        mediante la libreria pickle

        Uso:
            guardarArchivo('nombre_archivo', 'lo que sea')
    """
    with open(archivo, 'wb') as archivoguardar:
        print('Guardando', archivo, '...')
        pickle.dump(lo_que_sea, archivoguardar)
    print(archivo, 'Guardado!')
    archivoguardar.close

def cargarArchivo(archivo):
    """
        Carga el archivo serializado indicado mediante la libreria pickle
        y devuelve su contenido

        Uso:
            cargarArchivo('nombre_archivo')
    """    
    with open(archivo, 'rb') as archivocargar:
        print('Cargando', archivo, '...')
        lo_cargado = pickle.load(archivocargar)
    print(archivo, 'Cargado!')
    archivocargar.close
    return lo_cargado

def agregarCuenta(dixy,clave,valor):
    """
        Agrega un valor a la clave indicada del diccinario indicado

        Uso:
            agregarCuenta('diccionario', 'clave', 'valor')
    """
    print('Agregando en dixy(ram)...')
    dixy[clave].append(valor)
    print('Agregado en dixy(ram)!')