"""
    La libreria jesúscrypto provee funciones omnicientes y todopoderosas para EnigmaConPandas
    y otras aplicaciones que puedan y quieran escuchar a cristo Jesús y salvar sus almas!!!
    11/03/2023 Se depuró un poquito con el poder de la gracia divina gloria stefan...
    Thanks for https://pypi.org/project/cryptocode/
"""
import cryptocode, pickle

def encryConkey(eldato, llave):
    """
        Encrypta un string con la llave indicada por medio de la libreria crytptocode
        y lo devuelve encryptado
    
        Uso:
            encryConkey('string', 'llave')
    """
    #print('Encryptando...')
    return (cryptocode.encrypt(eldato, llave))

def decryConkey(eldato, llave):
    """
        Desencrypta un string encryptado solo con la llave correcta indicada 
        utilizando la libreria crytptocode y lo devuelve desencryptado
    
        Uso:
            decryConkey('string', 'llave')
        retorna el valor 'False' si la llave es erronea
    """
    #print('Desencryptando...')
    return (cryptocode.decrypt(eldato, llave))

def encryptaDixy(dixy, llave):
    """
        Encrypta un diccionario con la llave indicada por medio de la libreria crytptocode
        y lo devuelve encryptado
    
        Uso:
            encryptaDixy('diccionario', 'llave')
    """
    print('Encryptando...')
    for clave in dixy:
        for i in range (len(dixy[clave])):
            dixy[clave][i]=encryConkey((dixy[clave][i]),llave)
    print('Encryptado!')
    return dixy

def desencryptaDixy(dixy, llave):
    """
        Desencrypta un diccionario solo con la llave correcta indicada utilizando
        la libreria crytptocode y lo devuelve desencryptado
    
        Uso:
            desencryptaDixy('diccionario', 'llave')

        retorna 'Error_al_desencriptar' si la llave es erronea
    """
    print('Desencryptando...')
    try:
        for clave in dixy:
            for i in range (len(dixy[clave])):
                if decryConkey((dixy[clave][i]),llave) == False:
                    print('Jesús dice: Error de Clave')
                    raise StopIteration
                elif decryConkey((dixy[clave][i]),llave) != False:
                    print("desencryptando y desencryptando... gracias a Jesús")
                    dixy[clave][i]=decryConkey((dixy[clave][i]),llave)
            print('for clave in dixy')
    except StopIteration:
        print('se detuvo la desencryptación y se llamará al 911, al FBI, a la CIA, al Papa y a un Exorcista...')
        return 'Error_al_desencriptar'
    except:
        print("""   Something went wrong
                el for2 tiro una fucking excepción
                y la voy a manejar como un campeón
                    ...vamos renolito carajo!!!            """)
        return 'Error_al_desencriptar'
    else:
        print('for2 sin errores')
        return dixy    

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