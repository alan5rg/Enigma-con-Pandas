#!UTC/Encode to Python with Monkey Python Coddebuging Circus by Alan.R.G.Systemas
#     Jesús ayudame a programar en python, Amén!
#    No se maltrataron pandas creando este código!!!

# v.M16b4t (Beta Test) 21/03/2023 (tareas)
# depurar cerrar y guardar archivo para condiciones de len==0
# construir lista de reflexiones religiosas para mensajes aleatorios
# beta en chequeo de funcionamiento en general
# se sigue depurando el codigo evitando patrones repetitivos

# v.M16b4t se agregra opción de cancelar para consulta de guardardo de archivo vacío
# v.M16b4t se habilita guardar como al agregar o modificar un registro
# v.M16b4t ya no deja guardar un archivo vacío, deshabilita el boton guardar al eliminar el ultimo registro
# v.M16b4t se agrega opcion al cerrar archivo o app de consultar por archivo si se encuentra vacío
# v.M16b4t se pasan a upercase las variables solo en busquedas para lograr busquedas correctas y abarcativas
# v.M16b3t se agrega mensaje de registro existente si querer modificar un registro existiera otro igual (cuenta/usuario)
# v.M16b3t se agrega mensaje de registro repetido si exite el que se esta agregando (cuenta/usuario)
# v.M16b2t se implementa guardado de configuracion con Funciones_Guardame
# v.M16b2t se elimina clase customic en favor de utilizar Funciones_Guardame
# v.M16b0tct se agrega funcion de busqueda y localización de cuenta/usuario
# v.M16b0tct se agrega fondo de pandas
# v.M16b0tct se mueve foco de lista al final al agregar registro y al abrir archivo
# v.M16b0tc se agrega clase Funciones_Customic
# v.M16b0t se agrega confirmación de eliminación y de modificación
# v.M15b5t se acomodan los anchos de las columnas de forma automatica
# v.M15b5t el indice registro seleccionado label solo se muestra en modo debug
# v.M15b5t indice y flag en listado solo se muestran en modo debug
# v.M15b5t se ocultan columnas de indices y de flag 'encf'
# v.M15b4t no se deshabilita la opción modo enigma para archivos vacios de registros
# v.M15b4t indica solo el indice si hay un registro seleccionado en la tabla
# v.M15b4t ahora no se puden modificar registros con password encryptado
# v.M15b4t se ajustó tamaño de lista, indicador de indice y checkboxs en modo enigma
# v.M15b3t se agregan checkboxs para trabajar con todo el archivo o con registros individuales
# v.M15b3t se fija la posición de toolbars
# v.M15b2t se manejan archivos vacios al cerrarlos o cerrar la app mediante consulta, si se eliminan se registra en "self.archivoeliminado"
# v.M15b2t se corrigen errores al cancelar cuando se abren o crean archivos nuevos
# v.M15b2 (pre-beta) se implementa funcionalidad al encryptado/desencryptado de todo el archivo 
# v.M15b2 (pre-beta) se implementa verificacion de flags "encf" antes de el encryptado/desencryptado de todo el archivo 
# v.M15b2 (pre-beta) se depura codigo de armado de menu
# v.M15b2 (pre-beta) se agrega submenu de encryptado/desencryptado de todo el archivo 
# v.M15b pre-beta se corrigen errores de estado de clave privada y clave mostrada al cerrar el archivo y volver a abrilo
# v.M15b pre-beta se maneja el error que sobreescribia valor de pssw con "False" al introducir clave erronea!!!
# v.W15 pre-beta se agrega alerta iconografica de debug activado...
# v.W15 pre-beta se agrega menu debug en herramientas para salida por consola
# v.W15 pre-beta se agrega variable mododebug para imprimir estados y mensajes en consola
# v.W15 pre-beta (10/03/2023) Se eliminan prints de debug y otras anotaciones 

from jesúscrypto import encryConkey, decryConkey, guardarArchivo, cargarArchivo, agregarCuenta, encryptaDixy, desencryptaDixy
from Funciones_Guardame import get_settings, save_settings
import sys, os
#from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QToolBar, QGroupBox, QLineEdit, QGridLayout, QLabel
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.Qt import  *
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtWidgets import *
import pandas as pd
from PandasToTable import PandasModel5 #PandasModel, DataFrameModel, PandasModel3, PandasModel4
import qdarkstyle
from qdarkstyle import load_stylesheet, LightPalette, DarkPalette

class enigmaVentana(QMainWindow):
    cleanconsole = lambda: os.system('cls' if os.name=='nt' else 'clear')
    '''
    #para debug directorios y path
    # thanks to https://www.delftstack.com/es/howto/python/relative-path-in-python/
    scriptDir = os.path.dirname(os.path.realpath(__file__))
    print('      scriptDir: ', scriptDir)
    absolutepath = os.path.dirname(__file__)
    print('   absolutepath: ',absolutepath)
    fileDirectory = os.path.dirname(absolutepath)
    print('  filedirectory: ',fileDirectory)
    #Path of parent directory
    parentDirectory = os.path.dirname(fileDirectory)
    print('parentdirectory: ',parentDirectory)
    #Navigate to Strings directory
    newPath = os.path.join(scriptDir, 'icons')   
    print('        newpath: ',newPath)
    '''
    def __init__(self, parent=None):
        super(enigmaVentana, self).__init__()
        #self.mododebug = False #True para obtener salida por consola de estados y mensajes
        self.title = "Enigma con Pandas v.M16b4t (Beta Test)"
        self.shorttitle = "File:"
        self.top = 300
        self.left = 500
        self.width = 660
        self.height = 400
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.IconPath = os.path.join(scriptDir, 'icons')   
        self.setWindowIcon(QtGui.QIcon(self.IconPath + os.path.sep + 'cool.png'))
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMinimumSize(660,400)
        self.setFixedSize(660,400)
        self.setWindowTitle(self.title)
        self.setStyleSheet("QMainWindow{background-image: url(ecpclaro.png)}") #poner ecpclaro y ecposcuro en la misma carpeta del programa
        self.dixymyApp = {"cnt": [], "usr": [], "pssw": [], "encf": []}
        self.indiceFilaselec = ""
        self.clavePrivada = ""
        self.Archivo = "" #contenedor fisico de claves
        self.huboCambios = False
        self.cambiosGuardados = True
        self.archivoeliminado = True
        self.modoenigma = False
        #armado de pantalla
        self.CreateMenu()
        self.CreateContainers()

        #19/03/2023
        #para guardar configuraciones con Funciones_Recordame
        if get_settings('MonkeyPythonCodingCircus','EnigmaCP','Config','Valid') and get_settings('MonkeyPythonCodingCircus','EnigmaCP','Tema','Valid'):
            print('Registro de Configuraciónes Valido!!!')
        else:
            print('Registro de Configuraciónes Invalido!!!')
            #guarda acá configuración por defecto
            save_settings('MonkeyPythonCodingCircus','EnigmaCP','Config','Debug',False)
            save_settings('MonkeyPythonCodingCircus','EnigmaCP','Tema','Clasico',True)
            save_settings('MonkeyPythonCodingCircus','EnigmaCP','Tema','Claro',False)
            save_settings('MonkeyPythonCodingCircus','EnigmaCP','Tema','Oscuro',False)
            #guarda en registro la clave valida en True
            save_settings('MonkeyPythonCodingCircus','EnigmaCP','Config','Valid',True)
            save_settings('MonkeyPythonCodingCircus','EnigmaCP','Tema','Valid',True)
            print('Se Guardó Registro de Configuraciónes Por Defecto!!!')
        #ahora configuro según el registro de configuracion guardado
        if get_settings('MonkeyPythonCodingCircus','EnigmaCP','Config','Debug'):
            self.mododebug = True #True para obtener salida por consola de estados y mensajes
            self.AlertadeDebug.show()
        else:
            self.mododebug = False #True para obtener salida por consola de estados y mensajes
            self.AlertadeDebug.hide()
        if get_settings('MonkeyPythonCodingCircus','EnigmaCP','Tema','Clasico'):
            self.modoTemaClasico()
        elif get_settings('MonkeyPythonCodingCircus','EnigmaCP','Tema','Claro'):
            self.modoTemaClaro()
        elif get_settings('MonkeyPythonCodingCircus','EnigmaCP','Tema','Oscuro'):
            self.modoTemaOscuro()
        '''
        #para testeo de usabilidad
        print('get before command:')
        print('on get: ',get_settings('MonkeyPythonCodingCircus','EnigmaCP','Tema','Clasico'))
        print('on save command:')
        print('on save: ',save_settings('MonkeyPythonCodingCircus','EnigmaCP','Tema','Clasico',True))
        print('on save: ',save_settings('MonkeyPythonCodingCircus','EnigmaCP','Tema','Claro',False))
        print('on save: ',save_settings('MonkeyPythonCodingCircus','EnigmaCP','Tema','Oscuro',False))
        print('get after command:')
        print('on get: ',get_settings('MonkeyPythonCodingCircus','EnigmaCP','Tema','Clasico'))
        '''
        #19/03/2023

        self.correccioTemas() #porque según el tema se corren los tamaños y ubicaciones de las cosas

        #carpeta de iconos
        self.printDebug('       Iconpath: '+self.IconPath)

        #jehovah es la llave para desencriptar los misterios. Aleluya!!!
        self.jehovah = 'Hear, O Israel: The Lord our God, the Lord is one'
        self.texto = 'En el principio creó Dios los cielos y la tierra'
        #Prueba del poder de Jesúscripto
        self.textoencriptado = encryConkey(self.texto, self.jehovah)
        self.printDebug('   texto encriptado: '+ self.textoencriptado+ '\n')
        self.printDebug('texto desencriptado: '+ decryConkey(self.textoencriptado, self.jehovah)+ '\n')

        #para debug
        #enigmaVentana.cleanconsole()
        self.printDebug(pd.DataFrame(self.dixymyApp))

    #--------Crea el menú y las toolbars y algunas funciones básicas----------

    def CreateMenu(self):
        mainMenu = QMenuBar(self)   
        self.layout().setMenuBar(mainMenu)
        self.fileMenu = mainMenu.addMenu('&Archivo')
        self.enigmaMenu = mainMenu.addMenu('&Enigma')   #add 28/02/2023
        self.enigmaMenu.setEnabled(False) #hasta que no se cree o habra un archivo
        self.toolsMenu = mainMenu.addMenu('&Herramientas')        
        self.helpMenu = mainMenu.addMenu('Ayuda')
        
        nuevoButton = QAction(QIcon(self.IconPath + os.path.sep + 'new.png'), '&Nuevo', self)
        nuevoButton.setShortcut('Ctrl+N')
        nuevoButton.setStatusTip('Crear nuevo archivo Enigma (*.ef)')
        nuevoButton.triggered.connect(self.nuevoArchivo)
        self.fileMenu.addAction(nuevoButton)

        abrirButton = QAction(QIcon(self.IconPath + os.path.sep + 'abrirarchivo.png'), '&Abrir', self)
        abrirButton.setShortcut('Ctrl+A')
        abrirButton.setStatusTip('Abrir archivo Enigma (*.ef)')
        abrirButton.triggered.connect(self.abrirArchivo)
        self.fileMenu.addAction(abrirButton)
        
        self.guardarSubmenu = QAction(QIcon(self.IconPath + os.path.sep + 'save.png'), '&Guardar', self)
        self.guardarSubmenu.setShortcut('Ctrl+G')
        self.guardarSubmenu.setStatusTip('Guardar archivo Enigma (actual)')
        self.guardarSubmenu.triggered.connect(self.guardarArchivoef)
        self.fileMenu.addAction(self.guardarSubmenu)
        self.guardarSubmenu.setDisabled(True)
        
        self.guardarcomoSubmenu = QAction(QIcon(self.IconPath + os.path.sep + 'saveas.png'), 'Guardar Como', self)
        self.guardarcomoSubmenu.setShortcut('Ctrl+Shift+G')
        self.guardarcomoSubmenu.setStatusTip('Guardar archivo Enigma (nuevo archivo)')
        self.guardarcomoSubmenu.triggered.connect(self.guardarComo)
        self.fileMenu.addAction(self.guardarcomoSubmenu)
        self.guardarcomoSubmenu.setDisabled(True)

        self.cerrarArchivoSubmenu = QAction(QIcon(self.IconPath + os.path.sep + 'cerrararchivo.png'), '&Cerrar', self)
        self.cerrarArchivoSubmenu.setShortcut('Ctrl+C')
        self.cerrarArchivoSubmenu.setStatusTip('Cerrar archivo Enigma (*.ef)')
        self.cerrarArchivoSubmenu.triggered.connect(self.cerrarArchivo)
        self.fileMenu.addAction(self.cerrarArchivoSubmenu)
        self.cerrarArchivoSubmenu.setDisabled(True)

        self.fileMenu.addSeparator()
        exitButton = QAction(QIcon(self.IconPath + os.path.sep + 'cerrar.png'), 'Salir', self)
        exitButton.setShortcut('Ctrl+S')
        exitButton.setStatusTip('Salir de Enigma')
        exitButton.triggered.connect(self.appCerrar)
        self.fileMenu.addAction(exitButton)

        self.EnigmaEncrypt = QAction(QIcon(self.IconPath + os.path.sep + 'crypt.png'), 'Encryptar Registro', self)
        self.EnigmaEncrypt.setStatusTip('Encryptar Registro')
        self.EnigmaEncrypt.triggered.connect(self.encryptarRegistro)
        self.enigmaMenu.addAction(self.EnigmaEncrypt)

        self.EnigmaDecrypt = QAction(QIcon(self.IconPath + os.path.sep + 'decrypt.png'), 'Desencryptar Registro', self)
        self.EnigmaDecrypt.setStatusTip('Desencryptar Registro')
        self.EnigmaDecrypt.triggered.connect(self.desencryptarRegistro)
        self.enigmaMenu.addAction(self.EnigmaDecrypt)

        self.enigmaMenu.addSeparator()
        self.EnigmaEncryptAll = QAction(QIcon(self.IconPath + os.path.sep + 'encryall.png'), 'Encryptar Todo el Archivo', self)
        self.EnigmaEncryptAll.setStatusTip('Encryptar Todo el Archivo')
        self.EnigmaEncryptAll.triggered.connect(self.encryptarArchivo)
        self.enigmaMenu.addAction(self.EnigmaEncryptAll)

        self.EnigmaDecryptAll = QAction(QIcon(self.IconPath + os.path.sep + 'decryall.png'), 'Desencryptar Todo el Archivo', self)
        self.EnigmaDecryptAll.setStatusTip('Desencryptar Todo el Archivo')
        self.EnigmaDecryptAll.triggered.connect(self.desencryptarArchivo)
        self.enigmaMenu.addAction(self.EnigmaDecryptAll)
        
        self.esquemaSubmenu = self.toolsMenu.addMenu(QIcon(self.IconPath + os.path.sep + 'panda.png'),'Esquema de Colores')

        self.modonormalSubmenu = QAction(QIcon(self.IconPath + os.path.sep + 'panda.png'), 'Tema Clasico', self)
        self.modonormalSubmenu.setStatusTip('Esquema de colores Clasico')
        self.modonormalSubmenu.triggered.connect(self.modoTemaClasico)
        self.esquemaSubmenu.addAction(self.modonormalSubmenu)

        self.modoclaroSubmenu = QAction(QIcon(self.IconPath + os.path.sep + 'pandaclaro.png'), 'Tema Claro', self)
        self.modoclaroSubmenu.setStatusTip('Esquema de colores Claro')
        self.modoclaroSubmenu.triggered.connect(self.modoTemaClaro)
        self.esquemaSubmenu.addAction(self.modoclaroSubmenu)

        self.modooscuroSubmenu = QAction(QIcon(self.IconPath + os.path.sep + 'pandaoscuro.png'), 'Tema Oscuro', self)
        self.modooscuroSubmenu.setStatusTip('Esquema de colores Oscuro')
        self.modooscuroSubmenu.triggered.connect(self.modoTemaOscuro)
        self.esquemaSubmenu.addAction(self.modooscuroSubmenu)        
        
        self.modoSubmenu = self.toolsMenu.addMenu(QIcon(self.IconPath + os.path.sep + 'cool.png'),'Modos del Programa')

        self.EnigmaEnigma = QAction(QIcon(self.IconPath + os.path.sep + 'pkeyp.png'), 'Cambiar a Modo Enigma', self)
        self.EnigmaEnigma.setStatusTip('Cambiar a Modo Enigma')
        self.EnigmaEnigma.triggered.connect(self.modollavePrivada)
        self.modoSubmenu.addAction(self.EnigmaEnigma)
        self.EnigmaEnigma.setEnabled(False) #hasta que no se cree o habra un archivo

        self.EnigmaRegistros = QAction(QIcon(self.IconPath + os.path.sep + 'editar.png'), 'Cambiar a Modo Registros', self)
        self.EnigmaRegistros.setStatusTip('Cambiar a Modo Registros')
        self.EnigmaRegistros.triggered.connect(self.modoRegistros)
        self.modoSubmenu.addAction(self.EnigmaRegistros)

        self.toolsMenu.addSeparator()
        debugSubmenu =  QAction(QIcon(self.IconPath + os.path.sep + 'debug.png'), 'Modo &Debug Consola', self)
        debugSubmenu.setShortcut('Ctrl+D')
        debugSubmenu.setStatusTip('Modo Debug Consola')
        debugSubmenu.triggered.connect(self.debugConsola)
        self.toolsMenu.addAction(debugSubmenu)

        '''
        self.toolsMenu.addSeparator()
        customSubmenu =  QAction(QIcon(self.IconPath + os.path.sep + 'pandaoscuro.png'), 'Customic &qApp', self)
        customSubmenu.setShortcut('Ctrl+Q')
        customSubmenu.setStatusTip('Customic qApp')
        customSubmenu.triggered.connect(self.customize_window)
        self.toolsMenu.addAction(customSubmenu)
        '''

        acercadeSubmenu =  QAction(QIcon(self.IconPath + os.path.sep + 'acerca.png'), 'Acerca de', self)
        acercadeSubmenu.setStatusTip('Acerca de Enigma Con Pandas')
        acercadeSubmenu.triggered.connect(self.acercaDe)
        self.helpMenu.addAction(acercadeSubmenu)

        #toolbar personalizada
        self.tbf = QToolBar("File toolbar")
        self.tbf = self.addToolBar("Archivo")#, Qt.TopToolBarArea)
        #self.addToolBar(Qt.TopToolBarArea, self.tbf)
        self.tbf.setOrientation(Qt.Vertical)
        self.tbf.setFixedWidth(48)
        self.tbf.setFloatable(False)
        self.tbf.setMovable(False)
       
        self.addToolBarBreak()#Qt.TopToolBarArea) # or self.addToolBarBreak()

        self.tbe = QToolBar("Enigma toolbar")
        self.tbe = self.addToolBar('Enigma')#, Qt.TopToolBarArea)
        #self.addToolBar(Qt.TopToolBarArea, self.tbe)
        #self.insertToolBar(self.tbf, self.tbe)
        self.tbe.setOrientation(Qt.Vertical)
        self.tbe.setFixedWidth(48)
        self.tbe.setFloatable(False)
        self.tbe.setMovable(False)

        #para enigma toolbar
        self.mregs = QAction(QIcon(self.IconPath + os.path.sep + 'editar.png'),"Cambiar a Modo Registros",self)
        self.mregs.setStatusTip('Cambiar a Modo Registros')
        self.mregs.triggered.connect(self.modoRegistros)
        self.tbe.addAction(self.mregs)

        self.tbe.addSeparator()
        self.Encrypt = QAction(QIcon(self.IconPath + os.path.sep + 'crypt.png'), 'Encryptar Registro', self)
        self.Encrypt.setStatusTip('Encryptar Registro')
        self.Encrypt.triggered.connect(self.encryptarRegistro)
        self.tbe.addAction(self.Encrypt)

        self.Decrypt = QAction(QIcon(self.IconPath + os.path.sep + 'decrypt.png'), 'Desencryptar Registro', self)
        self.Decrypt.setStatusTip('Desencryptar Registro')
        self.Decrypt.triggered.connect(self.desencryptarRegistro)
        self.tbe.addAction(self.Decrypt)
        
        self.tbe.addSeparator()
        self.EncryptAll = QAction(QIcon(self.IconPath + os.path.sep + 'encryall.png'), 'Encryptar Todo el Archivo', self)
        self.EncryptAll.setStatusTip('Encryptar Todo el Archivo')
        self.EncryptAll.triggered.connect(self.encryptarArchivo)
        self.tbe.addAction(self.EncryptAll)

        self.DecryptAll = QAction(QIcon(self.IconPath + os.path.sep + 'decryall.png'), 'Desencryptar Todo el Archivo', self)
        self.DecryptAll.setStatusTip('Desencryptar Todo el Archivo')
        self.DecryptAll.triggered.connect(self.desencryptarArchivo)
        self.tbe.addAction(self.DecryptAll)

        self.tbe.setVisible(False)

        self.deshabilitaCrypto(True) # función para mantener deshabilitado hasta que se cree la clave
        self.deshabilitaCryptoAll(True) # función para mantener deshabilitado hasta que se cree la clave

        #para file toolbar
        newf = QAction(QIcon(self.IconPath + os.path.sep + 'new.png'),"Nuevo",self)
        newf.setStatusTip('Crear nuevo archivo Enigma (*.ef)')
        newf.triggered.connect(self.nuevoArchivo)
        self.tbf.addAction(newf)
        
        open = QAction(QIcon(self.IconPath + os.path.sep + 'abrirarchivo.png'),"Abrir",self)
        open.setStatusTip('Abrir archivo Enigma (*.ef)')
        open.triggered.connect(self.abrirArchivo)
        self.tbf.addAction(open)
        
        self.save = QAction(QIcon(self.IconPath + os.path.sep + 'save.png'),"Guardar",self)
        self.save.setStatusTip('Guardar archivo Enigma (actual)')
        self.save.triggered.connect(self.guardarArchivoef)
        self.tbf.addAction(self.save)
        self.save.setDisabled(True) #hasta que se cree o se habra un archivo
        
        self.saveas = QAction(QIcon(self.IconPath + os.path.sep + 'saveas.png'),"Guardar Como",self)
        self.saveas.setStatusTip('Guardar archivo Enigma (nuevo archivo)')
        self.saveas.triggered.connect(self.guardarComo)
        self.tbf.addAction(self.saveas)
        self.saveas.setDisabled(True) #hasta que se cree o se habra un archivo
        
        self.closea = QAction(QIcon(self.IconPath + os.path.sep + 'cerrararchivo.png'),"Cerrar",self)
        self.closea.setStatusTip('Cerrar archivo Enigma')
        self.closea.triggered.connect(self.cerrarArchivo)
        self.tbf.addAction(self.closea)
        self.closea.setDisabled(True) #hasta que se cree o se habra un archivo
        
        self.tbf.addSeparator()
        self.mEnigma = QAction(QIcon(self.IconPath + os.path.sep + 'pkeyp.png'),"Cambiar a Modo Enigma",self)
        self.mEnigma.setStatusTip('Cambiar a Modo Enigma')
        self.mEnigma.triggered.connect(self.modollavePrivada)
        self.mEnigma.setEnabled(False) #hasta que no se cree o habra un archivo
        self.tbf.addAction(self.mEnigma)
        
        panda = QAction(QIcon(self.IconPath + os.path.sep + 'cool.png'),"Acerda de Enigma Con Pandas",self)
        panda.setStatusTip('Acerca de Enigma Con Pandas')
        panda.triggered.connect(self.acercaDe)
        self.tbf.addAction(panda)

        #self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage('Listo para crear o abrir archivo enigma (*.ef)')
        self.statusBar().show()

        self.tbf.visibilityChanged.connect(self.cambiovisibilidadtbf)
        self.tbe.visibilityChanged.connect(self.cambiovisibilidadtbe)

    def cambiovisibilidadtbf(self):
        if self.tbf.isVisible() == True:
            self.tbe.setVisible(False)
    
    def cambiovisibilidadtbe(self):
        if self.tbe.isVisible() == True:
            self.tbf.setVisible(False)
    
    def debugConsola(self):
        if self.mododebug == False:
            self.mododebug = True
            save_settings('MonkeyPythonCodingCircus','EnigmaCP','Config','Debug',True)
            self.AlertadeDebug.show()
            self.tableView.setColumnHidden(3,False) #muestra la columa flag 'encf'
            self.tableView.verticalHeader().setVisible(True) #muestra columna de indices
            if self.indiceFilaselec != '':
                self.indicadorRegselec.setVisible(True) #muestra el label indice registro seleccionado
            self.printDebug('Modo Debug Consola Activado!')
        elif self.mododebug == True:
            self.mododebug = False
            save_settings('MonkeyPythonCodingCircus','EnigmaCP','Config','Debug',False)
            self.AlertadeDebug.hide()
            self.tableView.setColumnHidden(3,True) #oculta la columa flag 'encf'
            self.tableView.verticalHeader().setVisible(False) #oculta columna de indices
            self.indicadorRegselec.setVisible(False) #oculta el label indice registro seleccionado
            self.printDebug('Modo Debug Consola Desactivado... usted no debería leer esto')
        self.correccioTemas()

    def acercaDe(self):
        msg = QtWidgets.QMessageBox.about(self,'Acerca de '+self.title, """
                Enigma Con Pandas y Pickles es una aplicación
                desarrollada en Buenos Aires, Argentina por
                Monkey Python Coding Circus by Alan.R.G.Systemas.

                    Al igual que la maquina Enigma, esta aplicación
                permite crear o abrir un listado de contraseñas de
                cuentas varias y luego encriptar o desencriptar el
                mismo mediante el uso de una llave o clave privada
                sin la cual es imposible luego poder acceder a la
                informacion encriptada por JesúsCrypto, Amén!!!

                    No se maltrataron pandas ni monos creando ni
                modificando o depurando este código!!!

                            (El amor debe ser sincero.
                    Aborrezcan el mal; aférrense al bien.)
                """)

    #----------Control de Modos de Programa y generacion de Clave Privada----------

    def modollavePrivada(self):
        self.printDebug('Bienvenido al Modo Enigma...')
        self.printDebug('construye pantalla de generación de clave privada, encryptado y desencryptado')
        self.indicadorRegselec.setText(str(self.indiceFilaselec))
        if self.clavePrivada == '':
            self.llaveprivada.setText('ingrese aqui su llave privada')
            self.AlertadeLLavepc.hide()
            self.AlertadeLLavepnc.show()
        else:
            self.llaveprivada.setText(self.clavePrivada)
            self.AlertadeLLavepnc.hide()
            self.AlertadeLLavepc.show()
        self.regMode(False)
        self.correccioTemas()
        if self.chkregistro.isChecked() and (self.indiceFilaselec != '') and self.mododebug:
            self.indicadorRegselec.setVisible(True)
        if (not self.mododebug) or (self.indiceFilaselec == '') or (not self.chkregistro.isChecked()) or self.chkarchivo.isChecked():    
            self.indicadorRegselec.setVisible(False)
        self.pressEnter(self.llaveprivada) 

    def modoRegistros(self):
        self.printDebug('Bienvenido al Modo Registros...')
        self.printDebug('recontruye pantalla de modo registros; podrá agregar, modificar y eliminar registros')
        self.tableView.setEnabled(True)
        self.indicadorRegselec.setText(str(self.indiceFilaselec))
        self.AlertadeLLavepnc.hide()
        self.AlertadeLLavepc.hide()
        self.regMode(True)
        if (self.indiceFilaselec != '') and self.mododebug:
            self.indicadorRegselec.setVisible(True)
        self.correccioTemas()
        self.pressEnter(self.cuenta)

    def regMode(self,mode):
        self.chkregistro.setHidden(mode)
        self.chkarchivo.setHidden(mode)
        self.modoenigma = not mode
        self.enigmaMenu.setDisabled(mode)
        self.tbf.setVisible(mode) #toolbar file
        self.tbe.setHidden(mode) #toolbar enigma
        self.EntradaDatos.setVisible(mode) #groupbox
        self.BotonesDatos.setVisible(mode) #groupbox
        self.GenerarLlave.setHidden(mode) #groupbox
    
    def generarllaveBotonclick(self):
        #self.clavePrivada = self.llaveprivada.toPlainText() #para QTextEdit()
        self.clavePrivada = self.llaveprivada.text()
        self.llaveprivada.setText(self.clavePrivada)
        self.printDebug('se genero clave privada: "'+self.clavePrivada+'"')
        self.cambiochkregistro()
        self.cambiochkarchivo()
        self.llaveEstado(True)

    def eliminarllaveBotonclick(self):
        self.clavePrivada = ''
        self.llaveprivada.setText('ingrese aqui su llave privada')
        self.printDebug('se eliminó clave privada')
        self.deshabilitaCrypto(True)
        self.deshabilitaCryptoAll(True)
        self.llaveEstado(False)

    def llaveEstado(self,estado):
        self.llavecreada.setVisible(estado)
        self.llavenocreada.setHidden(estado)
        self.chkregistro.setEnabled(estado)
        self.chkarchivo.setEnabled(estado)
        if estado:
            self.AlertadeLLavepc.show()
            self.AlertadeLLavepnc.hide()
        else:
            self.AlertadeLLavepc.hide()
            self.AlertadeLLavepnc.show()
        '''
        if self.indiceFilaselec != '':
            self.deshabilitaCrypto(not estado)
            self.deshabilitaCryptoAll(not estado)
        '''

    def ocultarllaveBotonclick(self):
        self.printDebug('ocultar llave')
        if self.clavePrivada == '':
            self.llaveprivada.setText('ingrese aqui su llave privada')
        else:
            self.llaveprivada.setText(self.clavePrivada)
        self.llaveprivada.setEchoMode(QLineEdit.Password)

    def mostrarllaveBotonclick(self):
        self.printDebug('la llave privada es: "'+self.clavePrivada+'"')
        if self.clavePrivada == '':
            self.llaveprivada.setText('ingrese aqui su llave privada')
        else:
            self.llaveprivada.setText(self.clavePrivada)
        self.llaveprivada.setEchoMode(QLineEdit.Normal)

    #-------------Modo Enigma (Encryptado/Desencryptado)------------

    def encryptarRegistro(self):
        self.printDebug('Rutina Encryptado de Registro...')
        if self.dixymyApp['encf'][self.indiceFilaselec] == 'no':
            self.printDebug('Encrypta Registro')
            self.printDebug(str(self.indiceFilaselec))
            self.printDebug('con clave: "'+self.clavePrivada+'"')
            self.printDebug(self.dixymyApp['cnt'][self.indiceFilaselec])
            self.printDebug(self.dixymyApp['usr'][self.indiceFilaselec])
            self.printDebug(self.dixymyApp['pssw'][self.indiceFilaselec])
            self.printDebug(self.dixymyApp['encf'][self.indiceFilaselec])
            #ncrypta nomas cada clave segun el indice selecciona y la clave privada guardada
            #self.dixymyApp['cnt'][self.indiceFilaselec]=encryConkey(self.dixymyApp['cnt'][self.indiceFilaselec], self.clavePrivada)
            #self.dixymyApp['usr'][self.indiceFilaselec]=encryConkey(self.dixymyApp['usr'][self.indiceFilaselec], self.clavePrivada)
            self.dixymyApp['pssw'][self.indiceFilaselec]=encryConkey(self.dixymyApp['pssw'][self.indiceFilaselec], self.clavePrivada)
            self.dixymyApp['encf'][self.indiceFilaselec]='si'
            self.printDebug('Password Encryptado!')
            #self.printDebug(self.dixymyApp['cnt'][self.indiceFilaselec])
            #self.printDebug(self.dixymyApp['usr'][self.indiceFilaselec])
            self.printDebug(self.dixymyApp['pssw'][self.indiceFilaselec])
            self.printDebug(self.dixymyApp['encf'][self.indiceFilaselec])
            self.siagregomodificooElimino()
        else:
            self.printDebug('ojo al piojo que la cuenta ya está encryptada Barnie!!!')
            msg = QtWidgets.QMessageBox.warning(self,"Alerta de Encryptado!","""
            Usted está intentado encryptar un registro
            previamente encryptado, recapacite, tomese su
            tiempo y revea su actitud. Gracias Totales!

                (Todo lo que Dios hace es bueno,
            Todo lo que Dios permite es necesario.)
            """)

    def desencryptarRegistro(self):
        self.printDebug('Rutina Desencryptado de Registro...')
        if self.dixymyApp['encf'][self.indiceFilaselec] == 'si':
            self.printDebug('Desencrypta Regristro')
            self.printDebug(str(self.indiceFilaselec))
            self.printDebug('con clave: "'+self.clavePrivada+'"')
            self.printDebug(self.dixymyApp['cnt'][self.indiceFilaselec])
            self.printDebug(self.dixymyApp['usr'][self.indiceFilaselec])
            self.printDebug(self.dixymyApp['pssw'][self.indiceFilaselec])
            self.printDebug(self.dixymyApp['encf'][self.indiceFilaselec])
            try:
                if decryConkey(self.dixymyApp['pssw'][self.indiceFilaselec], self.clavePrivada) == False:
                    self.printDebug('Enigma dice: Error de Clave')
                    msg = QtWidgets.QMessageBox.warning(self,"Alerta de Clave!","Clave Ingresada Incorrecta!!!\n (Confia en el Señor con todo tu corazón,\n y no te apoyes en tu propia prudencia.)")
                    raise NameError
            except NameError:
                self.printDebug('NameError? Something went wrong con tu clave chamaco')
            else:
                #self.dixymyApp['cnt'][self.indiceFilaselec]=decryConkey(self.dixymyApp['cnt'][self.indiceFilaselec], self.clavePrivada)
                #self.dixymyApp['usr'][self.indiceFilaselec]=decryConkey(self.dixymyApp['usr'][self.indiceFilaselec], self.clavePrivada)
                self.dixymyApp['pssw'][self.indiceFilaselec]=decryConkey(self.dixymyApp['pssw'][self.indiceFilaselec], self.clavePrivada)
                self.dixymyApp['encf'][self.indiceFilaselec]='no'
                self.printDebug('Password Desencryptado!')
                #self.printDebug(self.dixymyApp['cnt'][self.indiceFilaselec])
                #self.printDebug(self.dixymyApp['usr'][self.indiceFilaselec])
                self.printDebug(self.dixymyApp['pssw'][self.indiceFilaselec])
                self.printDebug(self.dixymyApp['encf'][self.indiceFilaselec])
                self.siagregomodificooElimino()
        else:
            self.printDebug('Ojo al piojo que el Password no está Encryptado Barnie!!!')
            msg = QtWidgets.QMessageBox.warning(self,"Alerta de Desencryptado!","""
            Usted está tratando de desencryptar un registro
            previamente desencryptado o jamás encryptado
            por lo cual no puede ser desencryptado!!!

                (El Señor es mi pastor: nada me falta.)
            """)

    def encryptarArchivo(self):
        self.printDebug('Rutina Encryptado de Todo el Archivo...')
        #verificamos que no contenga registros con bandera de encryptado
        try:
            for i in range (len(self.dixymyApp['encf'])):
                self.printDebug(i)
                if self.dixymyApp['encf'][i] != 'no':
                    self.printDebug('Enigma dice: Hay Gato Encerrado y Registro Encryptado #'+str(i))
                    raise StopIteration
        except StopIteration:
            msg = QtWidgets.QMessageBox.warning(self,"Alerta de Encryptado!","""
            Enigma dice:
                Hay Gato Encerrado y Algún Registro Encryptado!

                No es posible encryptar todo el archivo si en
                él existe/n registro/s encryptado/s previamente.

                (Jesús no regala pescados, enseña a pescar.)
            """)
            algo_encryptado = True
            self.printDebug('algo_encryptado: '+str(algo_encryptado))
        else:
            algo_encryptado = False
            self.printDebug('algo_encryptado: '+str(algo_encryptado))
            #proseguimos con el encryptado
            self.printDebug('Se Encrypta Todo el Archivo')
            self.printDebug('con clave: "'+self.clavePrivada+'"')
            for i in range (len(self.dixymyApp['encf'])):
                self.dixymyApp['pssw'][i]=encryConkey(self.dixymyApp['pssw'][i], self.clavePrivada)
                self.dixymyApp['encf'][i]='si'
            self.siagregomodificooElimino()
            self.printDebug('Passwords Encryptados en todo el Archivo!')
            
    def desencryptarArchivo(self):
        self.printDebug('Rutina Desencryptado de Todo el Archivo...')
        #verificamos que no contenga registros con bandera de noencryptado
        try:
            for i in range (len(self.dixymyApp['encf'])):
                self.printDebug(i)
                if self.dixymyApp['encf'][i] != 'si':
                    self.printDebug('Enigma dice: Hay Gato Encerrado y Registro No Encryptado #'+str(i))
                    raise StopIteration
        except StopIteration:
            msg = QtWidgets.QMessageBox.warning(self,"Alerta de Desencryptado!","""
            Enigma dice:
                Hay Gato Encerrado y Algún Registro No Encryptado!

                No es posible desencryptar todo el archivo si en
                él existe/n registro/s desencryptado/s previamente
                o nunca encryptado/s...

                (La fe no hace que las cosas sean fáciles,
                    pero hace que sean posibles.)
            """)
            algo_no_encryptado = True
            self.printDebug('algo_no_encryptado: '+str(algo_no_encryptado))
        else:
            algo_no_encryptado = False
            self.printDebug('algo_no_encryptado: '+str(algo_no_encryptado))
            #proseguimos verificando que la clave sea la correcta
            try:
                for i in range (len(self.dixymyApp['encf'])):
                    self.printDebug(i)
                    if decryConkey(self.dixymyApp['pssw'][i], self.clavePrivada) == False:
                        self.printDebug('Enigma dice: Error de Clave para registro #'+str(i))
                        raise NameError
            except NameError:
                msg = QtWidgets.QMessageBox.warning(self,"Alerta de Clave!","""
                Enigma dice:
                    Clave Ingresada Incorrecta
                    para al menos una de las
                    cuentas registradas!!!
                
                    (menos pregunta Dios y perdona.)
                """)
            else:
                #ahora si proseguimos con el desencryptado
                self.printDebug('clave correcta')
                self.printDebug('Se Desencrypta Todo el Archivo')
                self.printDebug('con clave: "'+self.clavePrivada+'"')
                for i in range (len(self.dixymyApp['encf'])):
                    self.dixymyApp['pssw'][i]=decryConkey(self.dixymyApp['pssw'][i], self.clavePrivada)
                    self.dixymyApp['encf'][i]='no'
                self.siagregomodificooElimino()
                self.printDebug('Passwords Desencryptados en Todo el Archivo!')

    #-----------Elementos de las pantallas modo Archivo y Modo Enigma------------

    def CreateContainers(self):
        #campos de texto
        self.indicadorArchivo = QLineEdit('Debe crear un archivo nuevo o abrir uno existente!',self)
        self.indicadorArchivo.move(55,25)
        self.indicadorArchivo.setFixedSize(600,15)
        self.indicadorArchivo.setFont(QFont('Arial', 8))
        self.indicadorArchivo.setReadOnly(True)
        self.indicadorArchivo.setFrame(False)
        self.indicadorArchivo.setAutoFillBackground(True)
        self.indicadorArchivo.setStyleSheet('background-color: red; color: yellow')
        #self.indicadorArchivo.setStyleSheet('background-color: black; color: white')

        self.indicadorRegistros = QLineEdit('',self)
        self.indicadorRegistros.move(0,360)
        self.indicadorRegistros.setFixedSize(50,15)
        self.indicadorRegistros.setFont(QFont('Arial', 8))
        self.indicadorRegistros.setReadOnly(True)
        self.indicadorRegistros.setFrame(False)
        self.indicadorRegistros.setAutoFillBackground(True)
        self.indicadorRegistros.setStyleSheet('background-color: black; color: white')

        self.indicadorRegselec = QLineEdit('',self)
        #self.correccioTemas() #porque según el tema se corren los tamaños y ubicaciones de las cosas

        self.indicadorRegselec.setFixedSize(50,15)
        self.indicadorRegselec.setFont(QFont('Arial', 8))
        self.indicadorRegselec.setReadOnly(True)
        self.indicadorRegselec.setFrame(False)
        self.indicadorRegselec.setAutoFillBackground(True)
        self.indicadorRegselec.setStyleSheet('background-color: black; color: white')
        self.indicadorRegselec.setVisible(False)

        self.ecpclavePrivada = QLineEdit('debe ingresar una clave para poder encriptar sus datos o recuperarlos!')
        
        self.EntradaDatos = QGroupBox('Entrada de Datos:',self)
        self.EntradaDatos.move(55,38)
        self.EntradaDatos.setFixedSize(600,110)
       
        self.layoutentrada = QGridLayout(self.EntradaDatos)

        self.cuenta = QLineEdit(self)
        self.cuenta.setFixedWidth(500)
        self.cuenta.setEnabled(False)
        self.cuentalabel = QLabel('*Cuenta',self)

        self.usuario = QLineEdit(self)
        self.usuario.setFixedWidth(500)
        self.usuario.setEnabled(False)
        self.usuariolabel = QLabel('*Usuario',self)

        self.password = QLineEdit(self)
        self.password.setFixedWidth(500)
        self.password.setEnabled(False)
        self.passwordlabel = QLabel('Password',self)
        
        self.cuenta.returnPressed.connect(lambda: self.pressEnter(self.usuario))
        self.usuario.returnPressed.connect(lambda: self.pressEnter(self.password))
        self.password.returnPressed.connect(lambda: self.pressEnter(self.agregar))

        self.layoutentrada.addWidget(self.cuentalabel,0,0)
        self.layoutentrada.addWidget(self.cuenta,0,1)
        self.layoutentrada.addWidget(self.usuariolabel,1,0)
        self.layoutentrada.addWidget(self.usuario,1,1)
        self.layoutentrada.addWidget(self.passwordlabel,2,0)
        self.layoutentrada.addWidget(self.password,2,1)
        
        #botones
        self.BotonesDatos = QGroupBox('',self)
        self.BotonesDatos.move(55,135)
        self.BotonesDatos.setFixedSize(600,58)
        self.layoutbotones = QGridLayout(self.BotonesDatos)

        self.buscar = QPushButton("Buscar (*cnt/*usr)", self)
        self.buscar.setFixedWidth(130)
        self.buscar.setFixedHeight(20)
        self.buscar.clicked.connect(self.buscacntusrEndixymyApp)
        self.buscar.clicked.connect(lambda: self.pressEnter(self.cuenta))
        self.buscar.setAutoDefault(True)
        self.buscar.setDisabled(True) #hasta que se habra o cree un archivo
        self.layoutbotones.addWidget(self.buscar,0,0, alignment = Qt.AlignCenter)

        self.agregar = QPushButton("Agregar Cuenta", self)
        self.agregar.setFixedWidth(130)
        self.agregar.setFixedHeight(20)
        self.agregar.clicked.connect(self.agregarAdixymyApp)
        self.agregar.clicked.connect(lambda: self.pressEnter(self.cuenta))
        self.agregar.setAutoDefault(True)
        self.agregar.setDisabled(True) #hasta que se habra o cree un archivo
        self.layoutbotones.addWidget(self.agregar,0,1, alignment = Qt.AlignCenter)

        self.modificar = QPushButton("Modificar Cuenta", self)
        self.modificar.setFixedWidth(130)
        self.modificar.setFixedHeight(20)
        self.modificar.clicked.connect(self.modificarEndixymyApp)
        self.modificar.clicked.connect(lambda: self.pressEnter(self.cuenta))
        self.modificar.setAutoDefault(True)
        self.modificar.setDisabled(True) #hasta que se seleccione una fila o registro de cuenta
        self.layoutbotones.addWidget(self.modificar,0,2, alignment = Qt.AlignCenter)

        self.eliminar = QPushButton("Eliminar Cuenta", self)
        self.eliminar.setFixedWidth(130)
        self.eliminar.setFixedHeight(20)
        self.eliminar.clicked.connect(self.eliminarDedixymyApp)
        self.eliminar.clicked.connect(lambda: self.pressEnter(self.cuenta))
        self.eliminar.setAutoDefault(True)
        self.eliminar.setDisabled(True) #hasta que se seleccione una fila o registro de cuenta
        self.layoutbotones.addWidget(self.eliminar,0,3, alignment = Qt.AlignCenter)

        #tabla
        self.TablaPandatas = QGroupBox('Listado de Datos:',self)
        self.TablaPandatas.move(55,200)
        self.TablaPandatas.setFixedSize(600,180)
        self.layouttabla = QGridLayout(self.TablaPandatas)

        self.tableView = QtWidgets.QTableView(self)
        #self.tableView.setFixedSize(500,125)
        self.tableView.setFixedWidth(500)
        self.tableView.setObjectName("tableView")
        self.tableView.setSortingEnabled(False)
        self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows) #selecciona toda la fila
        self.tableView.setSelectionMode(QAbstractItemView.SingleSelection) #selecciona solo de a una fila
        self.tableView.clicked.connect(self.tableviewClick)
        #self.tableView.horizontalHeader().setStretchLastSection(True) #para que ocupe todo el ancho #ver 14/03/2023
        self.tableView.verticalHeader().setDefaultSectionSize(18)
        #self.tableView.verticalHeader().setHighlightSections(False) #hace que no se seleccionen los indices
        self.tableView.verticalHeader().setVisible(False) #oculta los indices
        #self.tableView.setCornerButtonEnabled(True)
        #self.tableView.verticalHeader().hide() #otro metodo de ocultar los indices
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.AnyKeyPressed|QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed|QtWidgets.QAbstractItemView.SelectedClicked)

        self.tableLabel = QLabel('Listado',self)
        self.layouttabla.addWidget(self.tableLabel,5,0, alignment = Qt.AlignTop)
        self.layouttabla.addWidget(self.tableView,5,1)
        
        #Alertas Iconográficas (ver posibles funciones)
        AlertadeGuardadoPixmap = QPixmap(self.IconPath + os.path.sep + 'savealertred.png')
        self.AlertadeGuardado = QLabel('Alerta Cambios no Guardados!!!', self)
        self.AlertadeGuardado.setStatusTip('Alerta Cambios no Guardados!!!')
        self.AlertadeGuardado.setScaledContents(True)
        self.AlertadeGuardado.setFixedSize(55,55)
        self.AlertadeGuardado.setPixmap(AlertadeGuardadoPixmap)
        self.AlertadeGuardado.move(0,305)
        self.AlertadeGuardado.hide()        

        AlertadeGuardadookPixmap = QPixmap(self.IconPath + os.path.sep + 'savegreen.png')
        self.AlertadeGuardadook = QLabel('Alerta Cambios Guardados', self)
        self.AlertadeGuardadook.setStatusTip('Alerta Cambios Guardados!')
        self.AlertadeGuardadook.setScaledContents(True)
        self.AlertadeGuardadook.setFixedSize(55,55)
        self.AlertadeGuardadook.setPixmap(AlertadeGuardadookPixmap)
        self.AlertadeGuardadook.move(0,305)
        self.AlertadeGuardadook.hide()        
        
        LLavePixmap = QPixmap(self.IconPath + os.path.sep + 'pkeypred.png')
        self.AlertadeLLavepnc = QLabel('Alerta llave No Creada', self)
        self.AlertadeLLavepnc.setStatusTip('Alerta llave No Creada!!!')
        self.AlertadeLLavepnc.setScaledContents(True)
        self.AlertadeLLavepnc.setFixedSize(55,55)
        self.AlertadeLLavepnc.setPixmap(LLavePixmap)
        self.AlertadeLLavepnc.move(0,252)
        self.AlertadeLLavepnc.hide()

        LLavePixmap = QPixmap(self.IconPath + os.path.sep + 'pkeypgreen.png')
        self.AlertadeLLavepc = QLabel('Alerta llave Creada', self)
        self.AlertadeLLavepc.setStatusTip('Alerta llave Creada!')
        self.AlertadeLLavepc.setScaledContents(True)
        self.AlertadeLLavepc.setFixedSize(55,55)
        self.AlertadeLLavepc.setPixmap(LLavePixmap)
        self.AlertadeLLavepc.move(0,252)
        self.AlertadeLLavepc.hide()

        AlertadedebugPixmap = QPixmap(self.IconPath + os.path.sep + 'debug.png')
        self.AlertadeDebug = QLabel('Alerta Modo Debug Consola!!!', self)
        self.AlertadeDebug.setStatusTip('Alerta Modo Debug Consola!!!')
        self.AlertadeDebug.setScaledContents(True)
        self.AlertadeDebug.setFixedSize(32,32)
        self.AlertadeDebug.setPixmap(AlertadedebugPixmap)
        self.AlertadeDebug.move(620,185)
                
        # trasparencia de sef.AlertaDebug
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.50)
        self.AlertadeDebug.setGraphicsEffect(self.opacity_effect)
        
        self.AlertadeDebug.hide() 

        self.GenerarLlave = QGroupBox('Generar llave Privada',self)
        self.GenerarLlave.move(55,38)
        self.GenerarLlave.setFixedSize(600,110)
        
        self.modollave = QLabel('LLave Privada:',self)
        self.llavenocreada = QLabel('No creada!!!',self)
        self.llavecreada = QLabel('LLave Creada!',self)
        #self.llaveprivada = QTextEdit('ingrese aqui su llave privada',self) #no soporta EchoMode
        self.llaveprivada = QLineEdit('ingrese aqui su llave privada',self)
        self.llaveprivada.setEchoMode(QLineEdit.Password)
        self.llavenocreada.setVisible(True)
        self.llavecreada.setVisible(False)

        self.botongenerar = QPushButton('Generar',self)
        self.botongenerar.setFixedWidth(150)
        self.botongenerar.clicked.connect(self.generarllaveBotonclick)

        self.botonmodificar = QPushButton('Modificar',self)
        self.botonmodificar.setFixedWidth(150)
        self.botonmodificar.clicked.connect(self.generarllaveBotonclick)

        self.botoneliminarllave = QPushButton('Eliminar',self)
        self.botoneliminarllave.setFixedWidth(150)
        self.botoneliminarllave.clicked.connect(self.eliminarllaveBotonclick)
        
        self.botonocultarllave = QPushButton('Ocultar',self)
        self.botonocultarllave.setFixedWidth(150)
        self.botonocultarllave.clicked.connect(self.ocultarllaveBotonclick)

        self.botonmostrarllave = QPushButton('Mostrar',self)
        self.botonmostrarllave.setFixedWidth(150)
        self.botonmostrarllave.clicked.connect(self.mostrarllaveBotonclick)

        #13/03/2023
        self.chkregistro = QCheckBox('De a un Registro', self)
        self.chkregistro.setGeometry(300, 150, 120, 20)
        self.chkregistro.setChecked(False)
        self.chkregistro.stateChanged.connect(self.cambiochkregistro)
        self.chkregistro.setEnabled(False)

        self.chkarchivo = QCheckBox('Todo el Archivo', self)
        self.chkarchivo.setGeometry(430, 150, 120, 20)
        self.chkarchivo.setChecked(False)
        self.chkarchivo.stateChanged.connect(self.cambiochkarchivo)
        self.chkarchivo.setEnabled(False)

        self.chkregistro.setVisible(False)
        self.chkarchivo.setVisible(False)
        #13/03/2023
        
        LLavePixmap = QPixmap(self.IconPath + os.path.sep + 'pkeyp.png')
        self.escudoLLave = QLabel('Alerta de llave', self)
        self.escudoLLave.setStatusTip('Alerta de llave!!!')
        self.escudoLLave.setScaledContents(True)
        self.escudoLLave.setFixedSize(32,32)
        self.escudoLLave.setPixmap(LLavePixmap)
        
        self.layoullaveprivada = QGridLayout(self.GenerarLlave)
        self.layoullaveprivada.addWidget(self.modollave,0,0,alignment = Qt.AlignTop)
        self.layoullaveprivada.addWidget(self.llaveprivada,0,1)
        self.layoullaveprivada.addWidget(self.escudoLLave,1,0,alignment = Qt.AlignCenter)
        self.layoullaveprivada.addWidget(self.botongenerar,1,1,alignment = Qt.AlignLeft)
        self.layoullaveprivada.addWidget(self.botonmodificar,1,1,alignment = Qt.AlignCenter)
        self.layoullaveprivada.addWidget(self.botoneliminarllave,1,1,alignment = Qt.AlignRight)
        self.layoullaveprivada.addWidget(self.llavenocreada,2,0,alignment = Qt.AlignCenter)
        self.layoullaveprivada.addWidget(self.llavecreada,2,0,alignment = Qt.AlignCenter)
        self.layoullaveprivada.addWidget(self.botonocultarllave,2,1,alignment = Qt.AlignLeft)
        self.layoullaveprivada.addWidget(self.botonmostrarllave,2,1,alignment = Qt.AlignRight)
        
        self.GenerarLlave.setVisible(False)
        self.show

    def cambiochkregistro(self):
        if self.chkregistro.isChecked() == True:
            self.chkarchivo.setChecked(False)
            self.deshabilitaCryptoAll(True)
            if self.indiceFilaselec != '':
                self.deshabilitaCrypto(False)
                if self.mododebug:
                    self.indicadorRegselec.setVisible(True)
        if self.chkregistro.isChecked() == False:
            #if not self.mododebug and self.indiceFilaselec == '':
            self.indicadorRegselec.setVisible(False)
            self.deshabilitaCrypto(True)
    
    def cambiochkarchivo(self):
        if self.chkarchivo.isChecked() == True:
            self.chkregistro.setChecked(False)
            #if not self.mododebug and self.indiceFilaselec == '':
            #if self.indiceFilaselec == '':
            self.indicadorRegselec.setVisible(False)
            if self.clavePrivada != '':
                self.deshabilitaCrypto(True)
                self.deshabilitaCryptoAll(False)
        if self.chkarchivo.isChecked() == False:
            self.deshabilitaCryptoAll(True)

    #------------se explica por si sola----------

    def tableviewClick(self):
        index=(self.tableView.selectionModel().currentIndex())
        value=index.sibling(index.row(),index.column()).data()
        self.printDebug('click en fila: '+str(index.row())+', columna: '+str(index.column())+', contenido: '+value)
        #tomar la fila para modificar self.dixymyApp asi: self.indiceFilaselec = index.row()
        self.cuenta.setText(index.sibling(index.row(),0).data())
        self.usuario.setText(index.sibling(index.row(),1).data())
        self.password.setText(index.sibling(index.row(),2).data())
        #al tocar en la tabla se habilitan botones modificar y eliminar.
        self.indiceFilaselec = index.row()
        self.printDebug('indice fila seleccionada: '+str(self.indiceFilaselec))
        self.indicadorRegselec.setText(str(self.indiceFilaselec))
        #if not self.modoenigma and self.mododebug:
        if self.mododebug:
            self.indicadorRegselec.setVisible(True)
        if self.modoenigma and self.chkregistro.isChecked() and self.mododebug:
            self.indicadorRegselec.setVisible(True)
        if self.modoenigma and self.chkarchivo.isChecked() and self.mododebug:
            self.indicadorRegselec.setVisible(False)
        
        self.modificar.setDisabled(False) 
        self.eliminar.setDisabled(False)
        #cambio estas variables al clic en tabla luego de los eventos
        if self.clavePrivada != '':
            if self.chkregistro.isChecked() == True:
                self.deshabilitaCrypto(False)
                #self.deshabilitaCryptoAll(False)
        if self.dixymyApp['encf'][self.indiceFilaselec] == 'si':
            self.modificar.setDisabled(True)
            self.eliminar.setDisabled(False)
        if self.dixymyApp['encf'][self.indiceFilaselec] == 'no':
            self.modificar.setDisabled(False)
            self.eliminar.setDisabled(False)
        #trata de seguir la fila seleccionada y primer columna
        self.tableView.SelectionBehavior(QtWidgets.QAbstractItemView.SelectColumns)
        self.tableView.scrollTo(self.tableView.model().index(self.indiceFilaselec,0))
            
    #-------------nuevo archivo / abrir archivo ----------------

    def nuevoArchivo(self):
        if self.huboCambios:
            eleccion = self.cambiosSinguardar('Está Seguro que Desea Crear Otro Archivo?') #continuar, salir de todos modos, seguir con esta vida absurda alejado de Dios y de los Pandas?
            self.printDebug('mi eleccion: '+eleccion) #['Si','Guardado','Cancelar']
            if eleccion == 'Guardado' or eleccion == 'Si':
                self.printDebug('eligió "Guardar" o "Si", se creará archivo')
                self.creandoArchivo()
            elif eleccion == 'Cancelar':
                self.printDebug('eligió "Cancelar", sigue a ventana principal sin cambios')
                #sigue a ventana principal sin cambios
            else:
                self.printDebug('sabrá Dios como llegó aquí')
        else:
            self.creandoArchivo()
        self.sicreoabroguardooGuardocomo()

    def creandoArchivo(self):
        archivo_en_uso = self.Archivo
        self.Archivo, _ = QtWidgets.QFileDialog.getSaveFileName (
            self, "Nuevo Archivo Enigma", "", "Archivo Enigma (*.ef)"
        )
        if self.Archivo:
            self.dixymyApp = {"cnt": [], "usr": [], "pssw": [], "encf": []}
            guardarArchivo(self.Archivo, self.dixymyApp)
            self.sicreonuevooAbroexistente()
        else:
            self.Archivo = archivo_en_uso

    def abrirArchivo(self):
        if self.huboCambios:
            eleccion = self.cambiosSinguardar('Está Seguro que Desea Abrir Otro Archivo?') #continuar, salir de todos modos, seguir con esta vida absurda alejado de Dios y de los Pandas?
            self.printDebug('mi eleccion: '+eleccion) #['Si','Guardado','Cancelar']
            if eleccion == 'Guardado' or eleccion == 'Si':
                self.printDebug('eligió "Guardar" o "Si", se abrirá archivo')
                self.abriendoArchivo()
            elif eleccion == 'Cancelar':
                self.printDebug('eligió "Cancelar", sigue a ventana principal sin cambios')
                #sigue a ventana principal sin cambios
            else:
                self.printDebug('sabrá Dios como llegó aquí')
        else:
            self.abriendoArchivo()
        self.sicreoabroguardooGuardocomo()
        self.tableView.scrollToBottom() #18/03/2023

    def abriendoArchivo(self):
        archivo_en_uso = self.Archivo
        self.Archivo, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Abrir Archivo Enigma", "", "Archivo Enigma (*.ef)","(*.ef)"
        )
        if self.Archivo:
            self.dixymyApp = cargarArchivo(self.Archivo)
            self.sicreonuevooAbroexistente()
        else:
            self.Archivo = archivo_en_uso

    def sicreonuevooAbroexistente(self):
        #cuando efectivamente se crea o abre un archivo
        #bandera
        self.archivoeliminado = False
        #boton agregar cuenta
        self.agregar.setEnabled(True)
        self.buscar.setEnabled(True)
        #en submenu y toolbar archivo
        self.cerrarArchivoSubmenu.setEnabled(True)
        self.closea.setEnabled(True)
        #campos de entrada de texto
        self.cuenta.setEnabled(True)
        self.usuario.setEnabled(True)
        self.password.setEnabled(True)
        self.sicreonuevooAbroexistenteoCierro()

    #--------------------cerrar archivo----------------------    
    #(depurar y ver todas las cominaciones de len==0, huboCambios y cambiosGuardados )
    def cerrarArchivo(self):
        self.printDebug('eligó cerrar archivo')
        df=pd.DataFrame(self.dixymyApp)
        if (len(df.index)) == 0 and self.huboCambios and not self.cambiosGuardados:
            if self.huboCambios:
                eleccion = self.cambiosSinguardar('Está Seguro que Desea Cerrar el Archivo?') #continuar, salir de todos modos, seguir con esta vida absurda alejado de Dios y de los Pandas?
                self.printDebug('mi eleccion: '+eleccion) #['Si','Guardado','Cancelar']
                if eleccion == 'Guardado' or eleccion == 'Si':
                    self.printDebug('eligió "Guardar" o "Si", se cerrará archivo')
                    titulo = "Listado Vacío"
                    mensaje = "El listado está vacío, Quiere Eliminar el archivo al Cerrarlo?...\n  (Dios le da pan al que no tiene dientes.)"
                    vacio = self.archivoVacio(titulo, mensaje)
                    if vacio == 'Yes' or vacio == 'No':
                        self.printDebug('eligió "Yes" o "No", se cerrará archivo')
                        self.condicionesIniciales()
                    elif vacio == "Cancel":
                        self.printDebug('eligió "Cancel", sigue a ventana principal sin cambios')
                    #self.condicionesIniciales()
                elif eleccion == 'Cancelar':
                    self.printDebug('eligió "Cancelar", sigue a ventana principal sin cambios')
            else:
                self.condicionesIniciales()
        elif (len(df.index)) == 0:
            titulo = "Listado Vacío"
            mensaje = "El listado está vacío, Quiere Eliminar el archivo al Cerrarlo?...\n  (Dios le da pan al que no tiene dientes.)"
            vacio = self.archivoVacio(titulo, mensaje)
            if vacio == 'Yes' or vacio == 'No':
                self.condicionesIniciales()
            elif vacio == "Cancel":
                self.printDebug('eligió "Cancel", sigue a ventana principal sin cambios')
        elif (len(df.index)) != 0 and self.huboCambios and not self.cambiosGuardados:
            if self.huboCambios:
                eleccion = self.cambiosSinguardar('Está Seguro que Desea Cerrar el Archivo?') #continuar, salir de todos modos, seguir con esta vida absurda alejado de Dios y de los Pandas?
                self.printDebug('mi eleccion: '+eleccion) #['Si','Guardado','Cancelar']
                if eleccion == 'Guardado' or eleccion == 'Si':
                    self.printDebug('eligió "Guardar" o "Si", se cerrará archivo')
                    self.condicionesIniciales()
                elif eleccion == 'Cancelar':
                    self.printDebug('eligió "Cancelar", sigue a ventana principal sin cambios')
            else:
                self.condicionesIniciales()
        elif (len(df.index)) != 0 and (not self.huboCambios or self.cambiosGuardados):
            self.condicionesIniciales()

    def condicionesIniciales(self):
        self.printDebug('Seteando Condiciones Iniciales...')
        #self.archivoVacio() #se evalua si el archivo está vacío y se pregunta en caso verdadero si se quiere guardar en ese estado de vacuidad
        self.dixymyApp = {"cnt": [], "usr": [], "pssw": [], "encf": []}
        self.llaveprivada.setText(self.clavePrivada)
        self.Archivo = '' #contenedor fisico de claves
        #bandera
        self.archivoeliminado = True
        #en submenu y toolbar archivo 
        self.guardarcomoSubmenu.setEnabled(False)
        self.saveas.setEnabled(False) 
        self.cerrarArchivoSubmenu.setEnabled(False)
        self.closea.setEnabled(False) 
        #armado de pantalla inicial modo registro
        self.modoRegistros()
        self.sicreonuevooAbroexistenteoCierro()
        #y si hago lo que sea tenga que hacer...
        self.sihagoLoquesea()
        #botones de modo registro
        self.agregar.setEnabled(False) #hasta que se habra o cree un archivo
        self.buscar.setEnabled(False) #hasta que se habra o cree un archivo
        #campos de entrada de texto
        self.cuenta.setEnabled(False)
        self.usuario.setEnabled(False)
        self.password.setEnabled(False)
        #ventana y archivo
        self.setWindowTitle(self.title)
        self.indicadorArchivo.setText('Debe crear un archivo nuevo o abrir uno existente!')
        self.indicadorArchivo.setStyleSheet('background-color: red; color: yellow')

    def sicreonuevooAbroexistenteoCierro(self):
        #en submenu y toolbar archivo
        self.save.setEnabled(False) 
        self.guardarSubmenu.setEnabled(False)
        self.guardarcomoSubmenu.setEnabled(False)
        self.saveas.setEnabled(False) 
        #banderas
        self.huboCambios = False 
        self.cambiosGuardados = True 
        #alertas
        self.AlertadeGuardado.hide() 
        self.AlertadeGuardadook.hide() 

    #--------------guardar archivo / guardar como ---------------
    # depurar toda la funcion
    def guardarArchivoef(self):
        if len(self.dixymyApp['cnt']) != 0:
            self.printDebug(pd.DataFrame(self.dixymyApp)) #por debug
            self.alguardaroguardarcomo()
            self.sicreoabroguardooGuardocomo()
        if len(self.dixymyApp['cnt']) == 0:
            titulo = "listado Vacío"
            mensaje = "El listado está vacío, Quiere Eliminar el archivo al guardar?...\n  Eliminar el archivo vuelve el programa a condiciones iniciales!\n (Dios le da pan al que no tiene dientes.)"
            eliminavacio = self.archivoVacio(titulo, mensaje)
            if eliminavacio == "Yes":
                self.printDebug('Eligio (Yes) se elimina archivo vacío')
                self.printDebug(pd.DataFrame(self.dixymyApp)) #por debug
                self.huboCambios = False
                self.cambiosGuardados = True
                self.AlertadeGuardado.hide()
                self.AlertadeGuardadook.show()
                self.guardarSubmenu.setDisabled(True)
                self.save.setDisabled(True) 
                self.cerrarArchivoSubmenu.setEnabled(True)
                self.closea.setEnabled(True)
                self.sicreoabroguardooGuardocomo()
                self.condicionesIniciales()
            elif eliminavacio == "No":
                self.printDebug('Eligio (No) Eliminar archivo vacío')
                self.printDebug(pd.DataFrame(self.dixymyApp)) #por debug
                self.alguardaroguardarcomo()
                self.sicreoabroguardooGuardocomo()
            elif eliminavacio == "Cancel":
                self.printDebug('Eligio (Cancel) sigue a la aplicación sin guardar')
 
    def guardarComo(self):
        self.printDebug(pd.DataFrame(self.dixymyApp)) #por debug
        archtemp=self.Archivo
        self.Archivo, _ = QtWidgets.QFileDialog.getSaveFileName (
            self, "Guardar Como", "", "Archivo Enigma (*.ef)"
        )
        if self.Archivo:
            self.alguardaroguardarcomo()
        else:
            self.Archivo=archtemp
        self.sicreoabroguardooGuardocomo()

    def alguardaroguardarcomo(self):
        self.printDebug('guardando listado de registros en archivo...')
        self.printDebug(self.Archivo)
        guardarArchivo(self.Archivo, self.dixymyApp)
        self.huboCambios = False
        self.cambiosGuardados = True
        self.AlertadeGuardado.hide()
        self.AlertadeGuardadook.show()
        self.guardarSubmenu.setDisabled(True)
        self.save.setDisabled(True) 
        self.cerrarArchivoSubmenu.setEnabled(True)
        self.closea.setEnabled(True) 

    def sicreoabroguardooGuardocomo(self):
        self.sihagoLoquesea()

    #------------botones Registros Modo Archivo Agregar/Modificar/Eliminar----------

    def agregarAdixymyApp(self):
        print('len dixymyApp: ',len(self.dixymyApp['cnt']))
        self.printDebug('verificando datos existentes...')
        if len(self.dixymyApp['cnt']) != 0 and self.cuenta.text()!='' and self.usuario.text()!='' and self.password.text()!='':
            self.printDebug('al menos un registro!')
            try:
                self.printDebug('verificando coincidencias...')
                indice=self.buscarEndixymyApp(self.cuenta.text(),self.usuario.text())
                if indice != 'no esta' and indice != None:
                    self.printDebug('lo tengo en id:'+str(indice))
                    self.tableView.selectRow(indice)
                    self.tableviewClick()
                    raise ValueError
                elif indice == 'no esta':
                    self.printDebug('no lo tengo')
            except ValueError:
                self.printDebug('Cuenta/Usuario ya registrados')
                msg = QtWidgets.QMessageBox.warning(self,"Cuenta/Usuario Existente!","""
                Enigma dice:
                    Para la Cuenta y Usuario indicados
                       ya existe un registro previo,
                      el mismo ha sido seleccionado!
                
                     (Dios es nuestro amparo y nuestra fortaleza,
                    nuestra ayuda segura en momentos de angustia.)
                """)
            else:
                self.printDebug('sin coincidencias, agregando registro...')
                self.siagregarAdixymyApp()
        elif len(self.dixymyApp['cnt']) == 0 and self.cuenta.text()!='' and self.usuario.text()!='' and self.password.text()!='':
            self.printDebug('Sin registros previos...')
            self.siagregarAdixymyApp()
        else:
            self.printDebug('cuenta y usuario vacios!!!')
            msg = QtWidgets.QMessageBox.warning(self,"Cuenta/Usuario Vacios!","""
                Enigma dice:
                    No sea hereje, por favor complete
                      Cuenta, Usuario y Password
                          que desea agregar...
                
                    (Así que no temas, porque yo estoy contigo;
                      no te angusties, porque yo soy tu Dios.)
                """)

    def siagregarAdixymyApp(self):
        agregarCuenta(self.dixymyApp,'cnt',self.cuenta.text())
        agregarCuenta(self.dixymyApp,'usr',self.usuario.text())
        agregarCuenta(self.dixymyApp,'pssw',self.password.text())
        agregarCuenta(self.dixymyApp,'encf','no')
        self.siagregomodificooElimino()
        self.tableView.scrollToBottom() #18/03/2023

    def modificarEndixymyApp(self):
        try:
            self.printDebug('verificando coincidencias...')
            indice=self.buscarEndixymyApp(self.cuenta.text(),self.usuario.text())
            if indice != 'no esta' and indice != None and indice != self.indiceFilaselec:
                self.printDebug('lo tengo en id:'+str(indice))
                self.tableView.selectRow(indice)
                self.tableviewClick()
                raise ValueError
            elif indice == 'no esta':
                self.printDebug('no lo tengo')
        except ValueError:
            self.printDebug('Cuenta/Usuario en otro registro!')
            msg = QtWidgets.QMessageBox.warning(self,"Cuenta/Usuario Existente!","""
            Enigma dice:
                Para la Cuenta y Usuario indicados
                    ya existe otro registro,
                el mismo ha sido seleccionado!
                
                 (Todo lo que pidan en la oración, 
                con tal de que crean, lo recibirán.)
            """)
        else:
            self.printDebug('sin coincidencias, modificando registro...')
            self.simodificarEndixymyApp()
    
    def simodificarEndixymyApp(self):
        segurola = self.estaSeguroque(
        'Confirmación de Modificación',"""
        Está usted seguro de modificar:
        """+
        'cuenta: '+str(self.dixymyApp['cnt'][self.indiceFilaselec])+
        ', usuario: '+str(self.dixymyApp['usr'][self.indiceFilaselec])+
        ', password: '+str(self.dixymyApp['pssw'][self.indiceFilaselec])+
        """
                            ...por:
        """+
        'cuenta: '+self.cuenta.text()+
        ', usuario: '+self.usuario.text()+
        ', password: '+self.password.text()
        )
        if segurola == 'Si':
            self.printDebug('dijo que si')
            self.printDebug('modificando el indice: '+str(self.indiceFilaselec))
            self.dixymyApp['cnt'][self.indiceFilaselec]=self.cuenta.text()
            self.dixymyApp['usr'][self.indiceFilaselec]=self.usuario.text()
            self.dixymyApp['pssw'][self.indiceFilaselec]=self.password.text()
            #self.dixymyApp['encf'][self.indiceFilaselec]='no'
            self.siagregomodificooElimino()  
        if segurola == 'No':
            self.printDebug('dijo que no')

    def eliminarDedixymyApp(self):
        segurola = self.estaSeguroque(
        'Confirmación de Eliminación',"""
        Está usted seguro de Eliminar el registro:
        """+
        'cuenta: '+str(self.dixymyApp['cnt'][self.indiceFilaselec])+
        ', usuario: '+str(self.dixymyApp['usr'][self.indiceFilaselec])+
        ', password: '+str(self.dixymyApp['pssw'][self.indiceFilaselec])
        )
        if segurola == 'Si':
            self.printDebug('dijo que si')
            self.printDebug('eliminando cuenta seleccionada')
            del self.dixymyApp['cnt'][self.indiceFilaselec]
            del self.dixymyApp['usr'][self.indiceFilaselec]
            del self.dixymyApp['pssw'][self.indiceFilaselec]
            del self.dixymyApp['encf'][self.indiceFilaselec]
            self.siagregomodificooElimino()
        if segurola == 'No':
            self.printDebug('dijo que no')

    def buscacntusrEndixymyApp(self):
        if self.cuenta.text()!='' and self.usuario.text()!='':
            indice=self.buscarEndixymyApp(self.cuenta.text(),self.usuario.text())
            if indice != 'no esta' and indice != None:
                self.printDebug('lo tengo id: '+str(indice))
                #self.tableView.SelectionBehavior(QtWidgets.QAbstractItemView.SelectColumns)
                #self.tableView.scrollTo(self.tableView.model().index(indice,0))
                self.tableView.selectRow(indice)
                self.tableviewClick()
                #self.indiceFilaselec = indice
            elif indice == 'no esta':
                self.printDebug('no lo tengo')
                self.tableView.scrollToBottom()
                self.tableView.clearSelection()
                self.limpiarCampos()
                self.pressEnter(self.cuenta)
                self.indiceFilaselec = ''
                self.indicadorRegselec.setVisible(False)
                msg = QtWidgets.QMessageBox.warning(self,"Registro Inexistente!","""
                Enigma dice:
                    No Existe Registro guardado
                    para la cuenta y el usuario
                    indicados!!!
                
                    (Me buscarán y me encontrarán
                  cuando me busquen de todo corazón.)
                """)
        else:
            self.printDebug('busqueda vacía')
            self.tableView.scrollToBottom()
            self.tableView.clearSelection()
            self.limpiarCampos()
            self.pressEnter(self.cuenta)
            self.indiceFilaselec = ''
            self.indicadorRegselec.setVisible(False)
            msg = QtWidgets.QMessageBox.warning(self,"Busqueda Inexistente!","""
                Enigma dice:
                    No sea Fariseo, por favor indique
                    la cuenta y el usuario que desea
                    Buscar...
                
                    (Oh Dios, tú eres mi Dios;
                    yo te busco intensamente.)
                """)

    def buscarEndixymyApp(self,cuenta,usuario):
        resultado = False
        for registro in range (len(self.dixymyApp['cnt'])):
            if (self.dixymyApp['cnt'][registro]).upper() == cuenta.upper() and (self.dixymyApp['usr'][registro]).upper() == usuario.upper():
                self.printDebug('Está en id: '+str(registro))
                resultado = True
                break
            else:
                self.printDebug('El Registro No Está!... El Registro No Está!... El Registro No Está!...')
                resultado = False
        if resultado:
            return registro
        else:
            return 'no esta'

    def estaSeguroque(self,titulo,mensaje):
        msg = QtWidgets.QMessageBox.question(self, titulo, mensaje, QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes)
        if msg == QtWidgets.QMessageBox.No:
            self.printDebug('eligió que no esta seguro')
            return 'No'
        elif msg == QtWidgets.QMessageBox.Yes:
            self.printDebug('eligió que si esta seguro')
            return 'Si'
        else:
            self.printDebug('dios sabe que habra eligido usted, amén!')

    def siagregomodificooElimino(self):
        self.huboCambios = True
        self.cambiosGuardados = False
        self.AlertadeGuardado.show()
        self.AlertadeGuardadook.hide()
        self.guardarSubmenu.setDisabled(False)
        self.save.setDisabled(False)
        self.saveas.setDisabled(False)
        self.guardarcomoSubmenu.setDisabled(False) 
        self.cerrarArchivoSubmenu.setDisabled(False)
        self.closea.setDisabled(False) 
        self.sihagoLoquesea()

    def sihagoLoquesea(self):
        self.indiceFilaselec = ''
        self.indicadorRegselec.setVisible(False)
        self.dixyTotable(self.dixymyApp)
        self.eliminar.setDisabled(True)
        self.modificar.setDisabled(True)
        self.deshabilitaCrypto(True)
        self.deshabilitaCryptoAll(True)
        
        self.cambiochkregistro()
        self.cambiochkarchivo()
        
        self.limpiarCampos()
        self.pressEnter(self.cuenta)            

    def deshabilitaCrypto(self,estado):
        self.Encrypt.setDisabled(estado)
        self.Decrypt.setDisabled(estado)
        self.EnigmaEncrypt.setDisabled(estado)
        self.EnigmaDecrypt.setDisabled(estado)
    
    def deshabilitaCryptoAll(self,estado):
        self.EncryptAll.setDisabled(estado)
        self.DecryptAll.setDisabled(estado)
        self.EnigmaEncryptAll.setDisabled(estado)
        self.EnigmaDecryptAll.setDisabled(estado)        

    #------------Completar el tableView con el Dataframe de Pandas-------------

    def dixyTotable(self, dixy):
        df = pd.DataFrame(dixy)
        self.printDebug(df)
        # usar el dataframe que mejor aplique al programa
        model = PandasModel5(df) #no soporta ordenamiento por columnas (muestra indices)
        #model = PandasModel(df) #soporta ordenamiento por columnas (muestra indices)
        #model = DataFrameModel(df) #soporta ordenamiento de columnas (muestra indices)
        #model = PandasModel3(df) #soporta ordenamiento de columnas (no muestra indices)
        #model = PandasModel4(df) #soporta ordenamiento de columnas (no muestra indices)
        self.tableView.setModel(model)
        #seguimiento de archivo abierto
        if self.Archivo == '':
            self.setWindowTitle(self.title)
            self.indicadorArchivo.setText('Debe crear un archivo nuevo o abrir uno existente!')
            self.indicadorArchivo.setStyleSheet('background-color: red; color: yellow')
        else:
            self.setWindowTitle(self.shorttitle+self.Archivo)
            self.indicadorArchivo.setStyleSheet('background-color: green; color: white')
            self.indicadorArchivo.setText('file: '+self.Archivo)
        #para debug
        self.printDebug('len(df.index): ' + str(len(df.index))) #evalua tamaño de dataframe con pandas
        self.printDebug('len dict[cnt]: ' + str(len(dixy['cnt'])))
        self.printDebug('len dict[usr]: ' + str(len(dixy['usr'])))
        self.printDebug('len dict[pssw]: ' + str(len(dixy['pssw'])))
        self.printDebug('len dict[encf]: ' + str(len(dixy['encf'])))
        #contador de registros
        self.indicadorRegistros.setText(str(len(dixy['cnt'])))
        if (len(dixy['cnt'])) == 0:
            self.modificar.setDisabled(True) 
            self.eliminar.setDisabled(True) 
            self.EnigmaEnigma.setEnabled(False)
            self.mEnigma.setEnabled(False)
        #para habilitar menu enigma y toolbar enigma
        if (len(dixy['cnt'])) != 0:
            self.EnigmaEnigma.setEnabled(True)
            self.mEnigma.setEnabled(True)
        #seguimiento de fila seleccionada
        self.indicadorRegselec.setText(str(self.indiceFilaselec))
        '''
        self.tableView.SelectionBehavior(QtWidgets.QAbstractItemView.SelectColumns)
        if self.indiceFilaselec != '':
            self.tableView.scrollTo(self.tableView.model().index(self.indiceFilaselec,0))
            #self.tableView.setCurrentIndex(self.indiceFilaselec)
        else:
            self.tableView.scrollTo(self.tableView.model().index((len(df.index)-1),0))
            #self.tableView.scrollToBottom()
        '''
        #columnas y formato de tabla
        if not self.mododebug:
            self.tableView.setColumnHidden(3,True) #oculta la columa flag 'encf'
            self.tableView.verticalHeader().setVisible(False) #oculta los indices
        if self.mododebug:
            self.tableView.setColumnHidden(3,False) #oculta la columa flag 'encf'
            self.tableView.verticalHeader().setVisible(True) #oculta los indices
        #for i in range (len(df.columns)):
        #    self.tableView.resizeColumnToContents(i) #ajusta por indice de columna
        self.tableView.resizeColumnToContents(0)
        self.tableView.resizeColumnToContents(1)
        self.tableView.resizeColumnToContents(2)
        self.tableView.horizontalHeader().setStretchLastSection(True)#ajusta por ultima de columna
        #self.tableView.resizeColumnsToContents() #ajusta a todas

    def limpiarCampos(self):
        self.cuenta.clear()
        self.usuario.clear()
        self.password.clear()

    def pressEnter(self, campo):
        campo.setFocus()    

    #---------evaluo cambios al cerrar app----------

    def closeEvent(self, event):
        if self.huboCambios == True:# or self.cambiosGuardados == False:
            eleccion = self.cambiosSinguardar('Está Seguro que Desea Salir?') #continuar, salir de todos modos, seguir con esta vida absurda alejado de Dios y de los Pandas?
            self.printDebug('mi eleccion: '+eleccion) #['Si','Guardado','Cancelar']
            if eleccion == 'Si':
                event.accept()
                self.close()
            elif eleccion == 'Guardado':
                event.accept()
                self.printDebug('se guardó y ahora se cierra programa')
                self.close()
            elif eleccion == 'Cancelar':
                event.ignore()
                self.window()
                self.pressEnter(self.cuenta)
            else:
                event.ignore()
                self.printDebug('dios sabe que habra eligido usted, amén!')
                self.window()
                self.pressEnter(self.cuenta)
        else:
            df=pd.DataFrame(self.dixymyApp)
            self.printDebug('\nSaliendo... len(df.index): '+str(len(df.index))) #evalua tamaño de dataframe con pandas
            self.printDebug('CambiosGuardados: '+str(self.cambiosGuardados))
            self.printDebug('archivo: '+self.Archivo)
        #titulo = "Archivo Vacío"
        #mensaje = "El archivo está vacío, Quiere Eliminarlo al Salir?...\n  (Dios le da pan al que no tiene dientes.)"
        #self.archivoVacio(titulo, mensaje)
        self.printDebug('Saliendo...')
        self.close()
    
    #----manejo de archivos vacios al cerrarlos o cerrar la app----

    def archivoVacio(self, titulo, mensaje):
        df=pd.DataFrame(self.dixymyApp)
        if (len(df.index)) == 0 and self.archivoeliminado == False:
            msg = QtWidgets.QMessageBox.question(self, titulo, mensaje, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)
            if msg == QtWidgets.QMessageBox.Yes:
                self.printDebug('...se eliminará archivo vacío: '+self.Archivo)
                os.remove(self.Archivo)
                self.archivoeliminado = True
                return 'Yes'
            elif msg == QtWidgets.QMessageBox.No:
                self.printDebug('...el archivo: '+self.Archivo+' quedará en su sistema')
                return 'No'
            elif msg == QtWidgets.QMessageBox.Cancel:
                self.printDebug('...el archivo: '+self.Archivo+' quedará en su sistema')
                return 'Cancel'
            else:
                self.printDebug('dios sabe que habra eligido usted, amén!')
                self.window()
                self.pressEnter(self.cuenta)

    #---evaluo si hubo o no cambios en la dixymyApp (diccionario en memoria de la app)---

    def cambiosSinguardar(self, mensaje):
        if self.huboCambios == True:# or self.cambiosGuardados == False:
            msg = QtWidgets.QMessageBox.question(self, mensaje, "Hay cambios sin guardar, Elija una Opción...\n (Jesús enseña a sus disipulos a ser prudentes!)", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Save)
            if msg == QtWidgets.QMessageBox.Yes:
                self.printDebug('eligió continuar sin guardar')
                return 'Si'
            elif msg == QtWidgets.QMessageBox.Save:
                self.printDebug('eligió guardar')
                self.guardarArchivoef()
                self.printDebug('se guardó y ahora continua flujo de programa')
                return 'Guardado'
            elif msg == QtWidgets.QMessageBox.Cancel:
                self.printDebug('eligió cancelar')
                return 'Cancelar'
            else:
                self.printDebug('dios sabe que habra eligido usted, amén!')
                self.window()
                self.pressEnter(self.cuenta)

    #-------manejo de los estilos graficos o temas de la app-------

    def modoTemaClasico(self):
        self.printDebug('Modo Clasico Seleccionado...')
        save_settings('MonkeyPythonCodingCircus','EnigmaCP','Tema','Clasico',True)
        save_settings('MonkeyPythonCodingCircus','EnigmaCP','Tema','Claro',False)
        save_settings('MonkeyPythonCodingCircus','EnigmaCP','Tema','Oscuro',False)
        self.setStyleSheet("QMainWindow{background-image: url(ecpclaro.png)}")
        qApp.setStyleSheet("")
        qApp.setStyle('Fusion')
        self.correccioTemas()
    
    def modoTemaClaro(self):
        self.printDebug('Modo Claro Seleccionado...')
        save_settings('MonkeyPythonCodingCircus','EnigmaCP','Tema','Clasico',False)
        save_settings('MonkeyPythonCodingCircus','EnigmaCP','Tema','Claro',True)
        save_settings('MonkeyPythonCodingCircus','EnigmaCP','Tema','Oscuro',False)
        self.setStyleSheet("QMainWindow{background-image: url(ecpclaro.png)}")
        qApp.setStyleSheet(qdarkstyle.load_stylesheet(LightPalette))
        self.correccioTemas()

    def modoTemaOscuro(self):
        self.printDebug('Modo Oscuro Seleccionado...')
        save_settings('MonkeyPythonCodingCircus','EnigmaCP','Tema','Clasico',False)
        save_settings('MonkeyPythonCodingCircus','EnigmaCP','Tema','Claro',False)
        save_settings('MonkeyPythonCodingCircus','EnigmaCP','Tema','Oscuro',True)
        self.setStyleSheet("QMainWindow{background-image: url(ecposcuro.png)}")
        qApp.setStyleSheet(qdarkstyle.load_stylesheet(DarkPalette))
        self.correccioTemas()

    def correccioTemas(self):
        self.printDebug('ajustando para '+qApp.style().metaObject().className())
        if (qApp.style().metaObject().className() == 'QFusionStyle') and not self.modoenigma:  
            self.opacity_effect.setOpacity(0.50)
            self.AlertadeDebug.setGraphicsEffect(self.opacity_effect)
            self.indicadorRegselec.move(200,200)
            self.TablaPandatas.move(55,200) #cond tabla en modo registro
            self.TablaPandatas.setFixedSize(600,180) #cond tabla en modo registro
        
        elif (qApp.style().metaObject().className() != 'QFusionStyle') and not self.modoenigma: #para QStyleSheetStyle
            self.opacity_effect.setOpacity(1)
            self.AlertadeDebug.setGraphicsEffect(self.opacity_effect)
            self.indicadorRegselec.move(200,190)
            self.TablaPandatas.move(55,200) #cond tabla en modo registro
            self.TablaPandatas.setFixedSize(600,180) #cond tabla en modo registro
        
        elif (qApp.style().metaObject().className() == 'QFusionStyle') and self.modoenigma:  
            self.opacity_effect.setOpacity(0.50)
            self.AlertadeDebug.setGraphicsEffect(self.opacity_effect)
            self.indicadorRegselec.move(200,155)
            self.chkregistro.move(280, 152)
            self.chkarchivo.move(430, 152) 
            self.TablaPandatas.move(55,155)
            self.TablaPandatas.setFixedSize(600,225)
            
        elif (qApp.style().metaObject().className() != 'QFusionStyle') and self.modoenigma: #para QStyleSheetStyle
            self.opacity_effect.setOpacity(1)
            self.AlertadeDebug.setGraphicsEffect(self.opacity_effect)
            self.indicadorRegselec.move(200,148)
            self.chkregistro.move(280, 145)
            self.chkarchivo.move(430, 145) 
            self.TablaPandatas.move(55,160)
            self.TablaPandatas.setFixedSize(600,220)

    #----Debug por Consola----

    def printDebug(self, bug):
        if self.mododebug:
            print(bug)

    #---this is the end---

    def appCerrar(self):
        self.close()
        #app.quit()

    '''
    def customize_window(self, checked):
        self.w = clase_customic(self)
        self.w.show()
    '''

if __name__ == '__main__':
    #app
    qApp = QApplication(sys.argv)
    QMainWindow().setWindowModality(QtCore.Qt.ApplicationModal)
    qApp.setStyleSheet("")
    qApp.setStyle('Fusion')
    #app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    #app.setStyleSheet(qdarkstyle.load_stylesheet(LightPalette))
    #app.setStyleSheet(qdarkstyle.load_stylesheet(DarkPalette))
    ventana = enigmaVentana()
    ventana.show()
    sys.exit(qApp.exec_())