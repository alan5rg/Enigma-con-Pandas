#!UTC/Encode to Python with Monkey Python Coding Circus by Alan.R.G.Systemas
#     Jesús ayudame a programar en python, Amén!
#    No se maltrataron pandas creando este código!!!

# v.1.4.81 09/03/2023 (tareas)
# ver como implementar el encryptado/desencryptado de todo el archivo 
# ver logica de "crear", "modificar" y "eliminar" clave privada
# depurar codigo para las condiciones de mostrar archivo en uso
# ver activacion de botones "eliminar" y/o "modificar" en diferentes condiciones
# ver si da errores si se llega a presionar "eliminar" sin seleccionar ninguna fila en alguna condicion
# [por ejemplo al guardar como y no seleccionar ningun archivo o ir a abrir y no selecionar ningun archivo.
# ver que pasa cuando se abre archivo pero se cancela y se cierra aplicacion... error
# ver que pasa si se abre un archivo guardado vacio y se sale sin cambios y sin guardar (lo elimina)
# agregar boton "fijar posición" a toolbar

# ver ayuda en https://foroayuda.es/tag/qtableview/

# v.1.4.8 utilizando el flag clave 'encf' del diccionario se permite o no encryptar o desencryptar
# v.1.4.7 si no hubo cambios se deshabilita "guardar"
# v.1.4.7 se agrega funcionalidad a menu y toolbar "archivo cerrar"
# v.1.4.7 se agregan alertas iconograficas coloridas de guardado y clave privada
# v.1.4.7 se depuraron varias funciones eliminando patrones redundantes
# v.1.4.63 no habilita encrypt/decrypt si no hay registros para seleccionar o seleccionado
# v.1.4.63 se corrigue que seleccionar del listado y guardar dejaba habilitado encrypt/decrypt
# v.1.4.62 se verifica que se seleccione un item para poder encriptarlo
# v.1.4.62 si se genera la clave o llave privada me habilita a encryptar o desencriptar registros
# v.1.4.6 se agrega flag de estado encriptacion en el mismo diccionario clave 'encf'
# v.1.4.6 se implementa menu herramientas/modo de programa (registros / enigma)
# v.1.4.5 se agregó herramienta themes
# v.1.4.5 se deshabilita menu Enigma/llave privada si no hay archivo abierto o hay modificaciones sin guardar
# se consolida nueva version (1.4.5 = 1.4.3c + 1.4.4)
# v.1.4.4 se agregó funcionalizad a boton "modificar" cuenta
# v.1.4.3 cuando se borran todos los registros se deshabilitan el boton "eliminar" y "modificar"
# v.1.4.3 se agrego label con cantidad de registros de len(dixymyApp['cnt']) 
# v.1.4.3 se agregan botones para modificar y eliminar registro 'cuenta'
# v.1.4.2 se agrega label que indica el archivo que se esta trabajando
# v.1.4.2 se agrega un label con status de guardado o un icono gráfico
# v.1.4.2 se agrega submenu y boton en toolbar para cerrar archivo 
# v.1.4.1 si no hay archivo cargado deshabilitados los campos y botones agregar guardar y guardar como
# v.1.4.1 si se crea archivo nuevo pero no se agrega nada (queda vacio) y se sale sin guardar lo borra
# v.1.4.1 se pregunta si se quiere guardar cambios si hubo cambios al crear nuevo archivo o abrir archivo existente
# v.1.4.1 se deshabilitan campos hasta que se cree uno nuevo o abra un archivo existente
# v.1.4.1 se deshabilitan guardar y guardar como hasta no crear nuevo o abrir archivo existente
# v.1.4.1 se cambia medodo de acceso por teclas a menu guardar como
# v.1.4 se sacó orden de la tableview modificando el PandasModel5 de PandasToTable
# v.1.4 se agrega seleccion de registro con autocompletado de campos para modificar
# v.1.3 se agrega en titulo de la ventana el archivo que está abierto
# v.1.3 se agrega esquema de colores oscuro
# v.1.2 se documentan algunas funciones
# v.1.2 se ajusta tamaño de columnas tabla al contenido cada vez que la muestra
# v.1.2 21/02/2023 se agrego toolbox flotante
# v.1.1 se separaron groupbox de entrada y tabla en pantalla principal

from jesúscrypto import encryConkey, decryConkey, guardarArchivo, cargarArchivo, agregarCuenta, encriptaDixy, desencriptaDixy
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
    def __init__(self, parent=None):
        super(enigmaVentana, self).__init__()
        self.title = "Enigma con Pandas v.1.4.81"
        self.shorttitle = "File:"
        self.top = 300
        self.left = 500
        self.width = 660
        self.height = 400
        self.setWindowIcon(QtGui.QIcon('icons/cool.png'))
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMinimumSize(660,400)
        self.setFixedSize(660,400)
        self.setWindowTitle(self.title)
        self.dixymyApp = {"cnt": [], "usr": [], "pssw": [], "encf": []}
        self.indiceFilaselec = ''
        self.clavePrivada = ''
        self.Archivo = '' #contenedor fisico de claves
        self.huboCambios = False
        self.cambiosGuardados = True #evaluar
        self.CreateMenu()
        self.CreateContainers()
        #jehovah es la llave para desencriptar los misterios. Aleluya!!!
        self.jehovah = 'Hear, O Israel: The Lord our God, the Lord is one'
        self.texto = 'En el principio creó Dios los cielos y la tierra'
        #Prueba del poder de Jesúscripto
        self.textoencriptado = encryConkey(self.texto, self.jehovah)
        print('   texto encriptado: ', self.textoencriptado, '\n')
        print('texto desencriptado: ', decryConkey(self.textoencriptado, self.jehovah), '\n')

    def CreateMenu(self):
        mainMenu = QMenuBar(self)   
        self.layout().setMenuBar(mainMenu)
        self.fileMenu = mainMenu.addMenu('Archivo')
        self.enigmaMenu = mainMenu.addMenu('Enigma')   #add 28/02/2023
        self.enigmaMenu.setEnabled(False) #hasta que no se cree o habra un archivo
        self.toolsMenu = mainMenu.addMenu('Herramientas')        
        self.helpMenu = mainMenu.addMenu('Ayuda')

        self.esquemaSubmenu = self.toolsMenu.addMenu(QIcon('icons/panda.png'),'Esquema de Colores')
        self.modoSubmenu = self.toolsMenu.addMenu(QIcon('icons/cool.png'),'Modos del Programa')
        
        nuevoButton = QAction(QIcon('icons/new.png'), '&Nuevo', self)
        nuevoButton.setShortcut('Ctrl+N')
        nuevoButton.setStatusTip('Crear nuevo archivo Enigma (*.ef)')
        nuevoButton.triggered.connect(self.nuevoArchivo)

        abrirButton = QAction(QIcon('icons/abrirarchivo.png'), '&Abrir', self)
        abrirButton.setShortcut('Ctrl+A')
        abrirButton.setStatusTip('Abrir archivo Enigma (*.ef)')
        abrirButton.triggered.connect(self.abrirArchivo)
        
        self.guardarSubmenu = QAction(QIcon('icons/save.png'), '&Guardar', self)
        self.guardarSubmenu.setShortcut('Ctrl+G')
        self.guardarSubmenu.setStatusTip('Guardar archivo Enigma (actual)')
        self.guardarSubmenu.triggered.connect(self.guardarArchivoef)
        self.guardarSubmenu.setDisabled(True)
        
        self.guardarcomoSubmenu = QAction(QIcon('icons/saveas.png'), 'Guardar Como', self)
        self.guardarcomoSubmenu.setShortcut('Ctrl+Shift+G')
        self.guardarcomoSubmenu.setStatusTip('Guardar archivo Enigma (nuevo archivo)')
        self.guardarcomoSubmenu.triggered.connect(self.guardarComo)
        self.guardarcomoSubmenu.setDisabled(True)

        self.cerrarArchivoSubmenu = QAction(QIcon('icons/cerrararchivo.png'), '&Cerrar', self)
        self.cerrarArchivoSubmenu.setShortcut('Ctrl+C')
        self.cerrarArchivoSubmenu.setStatusTip('Cerrar archivo Enigma (*.ef)')
        self.cerrarArchivoSubmenu.triggered.connect(self.cerrarArchivo)
        self.cerrarArchivoSubmenu.setDisabled(True)

        #01/03/2023
        self.EnigmaEncrypt = QAction(QIcon('icons/crypt.png'), 'Encryptar Redistro', self)
        self.EnigmaEncrypt.setStatusTip('Encryptar Registro')
        self.EnigmaEncrypt.triggered.connect(self.encryptarRegistro)
        self.enigmaMenu.addAction(self.EnigmaEncrypt)

        self.EnigmaDecrypt = QAction(QIcon('icons/decrypt.png'), 'Desencryptar Registro', self)
        self.EnigmaDecrypt.setStatusTip('Desencryptar Registro')
        self.EnigmaDecrypt.triggered.connect(self.desencryptarRegistro)
        self.enigmaMenu.addAction(self.EnigmaDecrypt)
        #01/03/2023

        #02/03/2023
        self.modonormalSubmenu = QAction(QIcon('icons/panda.png'), 'Tema Clasico', self)
        self.modonormalSubmenu.setStatusTip('Esquema de colores Clasico')
        self.modonormalSubmenu.triggered.connect(self.modoTemaClasico)
        self.modoclaroSubmenu = QAction(QIcon('icons/pandaclaro.png'), 'Tema Claro', self)
        self.modoclaroSubmenu.setStatusTip('Esquema de colores Claro')
        self.modoclaroSubmenu.triggered.connect(self.modoTemaClaro)
        self.modooscuroSubmenu = QAction(QIcon('icons/pandaoscuro.png'), 'Tema Oscuro', self)
        self.modooscuroSubmenu.setStatusTip('Esquema de colores Oscuro')
        self.modooscuroSubmenu.triggered.connect(self.modoTemaOscuro)
                
        self.esquemaSubmenu.addAction(self.modonormalSubmenu)
        self.esquemaSubmenu.addAction(self.modoclaroSubmenu)
        self.esquemaSubmenu.addAction(self.modooscuroSubmenu)
        #02/03/2023

        #28/02/2023 -- 03/03/2023
        self.EnigmaEnigma = QAction(QIcon('icons/pkeyp.png'), 'Modo Enigma', self)
        self.EnigmaEnigma.setStatusTip('Modo Enigma')
        self.EnigmaEnigma.triggered.connect(self.modollavePrivada)
        self.EnigmaEnigma.setEnabled(False) #hasta que no se cree o habra un archivo

        self.EnigmaRegistros = QAction(QIcon('icons/editar.png'), 'Modo Registros', self)
        self.EnigmaRegistros.setStatusTip('Modo Registros')
        self.EnigmaRegistros.triggered.connect(self.modoRegistros)
        
        self.modoSubmenu.addAction(self.EnigmaEnigma)
        self.modoSubmenu.addAction(self.EnigmaRegistros)
        #03/03/2023

        acercadeSubmenu =  QAction(QIcon('icons/acerca.png'), 'Acerca de', self)
        acercadeSubmenu.setStatusTip('Acerca de Enigma Con Pandas')
        acercadeSubmenu.triggered.connect(self.acercaDe)

        exitButton = QAction(QIcon('icons/cerrar.png'), 'Salir', self)
        exitButton.setShortcut('Ctrl+S')
        exitButton.setStatusTip('Salir de Enigma')
        exitButton.triggered.connect(self.appCerrar)
        
        self.fileMenu.addAction(nuevoButton)
        self.fileMenu.addAction(abrirButton)
        self.fileMenu.addAction(self.guardarSubmenu)
        self.fileMenu.addAction(self.guardarcomoSubmenu)
        self.fileMenu.addAction(self.cerrarArchivoSubmenu)
        self.fileMenu.addAction(exitButton)
        
        self.helpMenu.addAction(acercadeSubmenu)

        #01/03/2023 modified
        #toolbar personalizada
        self.tbf = QToolBar("File toolbar")
        self.tbf = self.addToolBar("Archivo")#, Qt.TopToolBarArea)
        #self.addToolBar(Qt.TopToolBarArea, self.tbf)
        self.tbf.setOrientation(Qt.Vertical)
        self.tbf.setFixedWidth(48)
       
        self.addToolBarBreak()#Qt.TopToolBarArea) # or self.addToolBarBreak()

        self.tbe = QToolBar("Enigma toolbar")
        self.tbe = self.addToolBar('Enigma')#, Qt.TopToolBarArea)
        #self.addToolBar(Qt.TopToolBarArea, self.tbe)
        #self.insertToolBar(self.tbf, self.tbe)
        self.tbe.setOrientation(Qt.Vertical)
        self.tbe.setFixedWidth(48)
     
        #for reg toolbar
        self.mregs = QAction(QIcon("icons/editar.png"),"Modo Registros",self)
        self.mregs.setStatusTip('Modo Registros')
        self.mregs.triggered.connect(self.modoRegistros)
        self.tbe.addAction(self.mregs)

        self.gclave = QAction(QIcon("icons/pkeyp.png"),"Generar CLave Privada",self)
        self.gclave.setStatusTip('Generar Clave Privada')
        self.gclave.triggered.connect(self.generarllaveBotonclick)
        self.tbe.addAction(self.gclave)

        self.Encrypt = QAction(QIcon('icons/crypt.png'), 'Encryptar Redistro', self)
        self.Encrypt.setStatusTip('Encryptar Registro')
        self.Encrypt.triggered.connect(self.encryptarRegistro)
        self.tbe.addAction(self.Encrypt)

        self.Decrypt = QAction(QIcon('icons/decrypt.png'), 'Desencryptar Registro', self)
        self.Decrypt.setStatusTip('Desencryptar Registro')
        self.Decrypt.triggered.connect(self.desencryptarRegistro)
        self.tbe.addAction(self.Decrypt)
        
        self.tbe.setVisible(False)
        #01/03/2023 modified

        #08/03/2023 mantener deshabilitado hasta que se cree la clave
        self.Encrypt.setDisabled(True)
        self.Decrypt.setDisabled(True)
        self.EnigmaEncrypt.setDisabled(True)
        self.EnigmaDecrypt.setDisabled(True)
        #08/03/2023

        #for file toolbar
        newf = QAction(QIcon("icons/new.png"),"Nuevo",self)
        newf.setStatusTip('Crear nuevo archivo Enigma (*.ef)')
        newf.triggered.connect(self.nuevoArchivo)
        self.tbf.addAction(newf)
        
        open = QAction(QIcon("icons/abrirarchivo.png"),"Abrir",self)
        open.setStatusTip('Abrir archivo Enigma (*.ef)')
        open.triggered.connect(self.abrirArchivo)
        self.tbf.addAction(open)
        
        self.save = QAction(QIcon("icons/save.png"),"Guardar",self)
        self.save.setStatusTip('Guardar archivo Enigma (actual)')
        self.save.triggered.connect(self.guardarArchivoef)
        self.tbf.addAction(self.save)
        self.save.setDisabled(True) #hasta que se cree o se habra un archivo
        
        self.saveas = QAction(QIcon("icons/saveas.png"),"Guardar Como",self)
        self.saveas.setStatusTip('Guardar archivo Enigma (nuevo archivo)')
        self.saveas.triggered.connect(self.guardarComo)
        self.tbf.addAction(self.saveas)
        self.saveas.setDisabled(True) #hasta que se cree o se habra un archivo
        
        self.closea = QAction(QIcon("icons/cerrararchivo.png"),"Cerrar",self)
        self.closea.setStatusTip('Cerrar archivo Enigma')
        self.closea.triggered.connect(self.cerrarArchivo)
        self.tbf.addAction(self.closea)
        self.closea.setDisabled(True) #hasta que se cree o se habra un archivo
        
        self.tbf.addSeparator()
        panda = QAction(QIcon("icons/cool.png"),"Acerda de Enigma Con Pandas",self)
        panda.setStatusTip('Acerca de Enigma Con Pandas')
        panda.triggered.connect(self.acercaDe)
        self.tbf.addAction(panda)

        #self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage('Listo para crear o abrir archivo enigma (*.ef)')
        self.statusBar().show()

    def acercaDe(self):  #replace information to about
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

                """)

    #28/02/2023
    def modollavePrivada(self):
        print('construye pantalla de generación de clave privada')
        self.indicadorRegselec.setText(str(self.indiceFilaselec))
        if self.clavePrivada == '':
            self.AlertadeLLavepc.hide()
            self.AlertadeLLavepnc.show()
        else:
            self.AlertadeLLavepnc.hide()
            self.AlertadeLLavepc.show()
        self.regMode(False)
        self.pressEnter(self.llaveprivada) 

    def modoRegistros(self):
        self.indicadorRegselec.setText(str(self.indiceFilaselec))
        print('recontruye pantalla de modo resgistros')
        self.AlertadeLLavepnc.hide()
        self.AlertadeLLavepc.hide()
        self.regMode(True)
        self.pressEnter(self.cuenta)

    def regMode(self,mode):
        self.enigmaMenu.setDisabled(mode)
        self.tbf.setVisible(mode) #toolbar file
        self.tbe.setHidden(mode) #toolbar enigma
        self.EntradaDatos.setVisible(mode) #groupbox
        self.BotonesDatos.setVisible(mode) #groupbox
        self.GenerarLlave.setHidden(mode) #groupbox
    
    def generarllaveBotonclick(self):
        #self.clavePrivada = self.llaveprivada.toPlainText() #para QTextEdit()
        self.clavePrivada = self.llaveprivada.text()
        print('se genero clave privada: "', self.clavePrivada,'"')
        self.llaveEstado(True)

    def eliminarllaveBotonclick(self):
        self.clavePrivada = ''
        self.llaveprivada.setText('ingrese aqui su llave privada')
        print('se eliminó clave privada')
        self.llaveEstado(False)

    #08/03/2023
    def llaveEstado(self,estado):
        self.llavenocreada.setHidden(estado)
        self.llavecreada.setVisible(estado)
        if estado:
            self.AlertadeLLavepc.show()
            self.AlertadeLLavepnc.hide()
        else:
            self.AlertadeLLavepc.hide()
            self.AlertadeLLavepnc.show()
        if self.indiceFilaselec != '':
            self.Encrypt.setEnabled(estado)
            self.Decrypt.setEnabled(estado)
            self.EnigmaEncrypt.setEnabled(estado)
            self.EnigmaDecrypt.setEnabled(estado)
    #08/03/2023

    def ocultarllaveBotonclick(self):
        print('ocultar llave')
        self.llaveprivada.setEchoMode(QLineEdit.Password)

    def mostrarllaveBotonclick(self):
        print('mostrar llave')
        self.llaveprivada.setEchoMode(QLineEdit.Normal)

    #01/03/2023
    def encryptarRegistro(self):
        #08/03/2023 agregar manejo de errores
        if self.dixymyApp['encf'][self.indiceFilaselec] == 'no':
            print('Encrypta Registro')
            print(self.indiceFilaselec)
            print('con clave: "',self.clavePrivada,'"')
            print(self.dixymyApp['cnt'][self.indiceFilaselec])
            print(self.dixymyApp['usr'][self.indiceFilaselec])
            print(self.dixymyApp['pssw'][self.indiceFilaselec])
            print(self.dixymyApp['encf'][self.indiceFilaselec])
            #self.dixymyApp['cnt'][self.indiceFilaselec]=encryConkey(self.dixymyApp['cnt'][self.indiceFilaselec], self.clavePrivada)
            #self.dixymyApp['usr'][self.indiceFilaselec]=encryConkey(self.dixymyApp['usr'][self.indiceFilaselec], self.clavePrivada)
            self.dixymyApp['pssw'][self.indiceFilaselec]=encryConkey(self.dixymyApp['pssw'][self.indiceFilaselec], self.clavePrivada)
            self.dixymyApp['encf'][self.indiceFilaselec]='si'
            #print(self.dixymyApp['cnt'][self.indiceFilaselec])
            #print(self.dixymyApp['usr'][self.indiceFilaselec])
            print(self.dixymyApp['pssw'][self.indiceFilaselec])
            print(self.dixymyApp['encf'][self.indiceFilaselec])
            self.siagregomodificooElimino()
        else:
            print('ojo al piojo que la cuenta ya está encryptada Barnie!!!')
            msg = QtWidgets.QMessageBox.warning(self,"Alerta de Encryptado","""
            Usted está intentado encryptar un registro
            previamente encryptado, recapacite, tomese su
            tiempo y revea su actitud. Gracias Totales!
            Jesús enseña a sus disipulos a ser prudentes!
            """)

    def desencryptarRegistro(self):
        #08/03/2023 agregar manejo de errores
        if self.dixymyApp['encf'][self.indiceFilaselec] == 'si':
            print('Desencripta Regristro')
            print(self.indiceFilaselec)
            print('con clave: "',self.clavePrivada,'"')
            print(self.dixymyApp['cnt'][self.indiceFilaselec])
            print(self.dixymyApp['usr'][self.indiceFilaselec])
            print(self.dixymyApp['pssw'][self.indiceFilaselec])
            print(self.dixymyApp['encf'][self.indiceFilaselec])
            #self.dixymyApp['cnt'][self.indiceFilaselec]=decryConkey(self.dixymyApp['cnt'][self.indiceFilaselec], self.clavePrivada)
            #self.dixymyApp['usr'][self.indiceFilaselec]=decryConkey(self.dixymyApp['usr'][self.indiceFilaselec], self.clavePrivada)
            self.dixymyApp['pssw'][self.indiceFilaselec]=decryConkey(self.dixymyApp['pssw'][self.indiceFilaselec], self.clavePrivada)
            self.dixymyApp['encf'][self.indiceFilaselec]='no'
            #print(self.dixymyApp['cnt'][self.indiceFilaselec])
            #print(self.dixymyApp['usr'][self.indiceFilaselec])
            print(self.dixymyApp['pssw'][self.indiceFilaselec])
            print(self.dixymyApp['encf'][self.indiceFilaselec])
            self.siagregomodificooElimino()
        else:
            print('ojo al piojo que la cuenta no está encryptada Barnie!!!')
            msg = QtWidgets.QMessageBox.warning(self,"Alerta de Desencryptado","""
            Usted está tratando de desencryptar un registro
            previamente desencryptado o jamás encryptado
            por lo cual no puede ser desencryptado!!!
            Jesús enseña a sus disipulos a ser prudentes!
            """)
            
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
        self.correccioTemas() #porque según el tema se corren los tamaños y ubicaciones de las cosas
        '''
        print(app.style().metaObject().className())
        if app.style().metaObject().className() == 'QFusionStyle':  
            self.indicadorRegselec.move(200,200)
        else: #para QStyleSheetStyle
            self.indicadorRegselec.move(200,190)
        '''
        self.indicadorRegselec.setFixedSize(50,15)
        self.indicadorRegselec.setFont(QFont('Arial', 8))
        self.indicadorRegselec.setReadOnly(True)
        self.indicadorRegselec.setFrame(False)
        self.indicadorRegselec.setAutoFillBackground(True)
        self.indicadorRegselec.setStyleSheet('background-color: black; color: white')

        self.ecpclavePrivada = QLineEdit('debe ingresar una clave para poder encriptar sus datos o recuperarlos!')
        
        self.EntradaDatos = QGroupBox('Entrada de Datos:',self)
        self.EntradaDatos.move(55,38)
        self.EntradaDatos.setFixedSize(600,110)
       
        self.layoutentrada = QGridLayout(self.EntradaDatos)

        self.cuenta = QLineEdit(self)
        self.cuenta.setFixedWidth(500)
        self.cuenta.setEnabled(False)
        self.cuentalabel = QLabel('Cuenta',self)

        self.usuario = QLineEdit(self)
        self.usuario.setFixedWidth(500)
        self.usuario.setEnabled(False)
        self.usuariolabel = QLabel('Usuario',self)

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

        self.agregar = QPushButton("Agregar Cuenta", self)
        self.agregar.setFixedWidth(150)
        self.agregar.setFixedHeight(20)
        self.agregar.clicked.connect(self.agregarAdixymyApp)
        self.agregar.clicked.connect(lambda: self.pressEnter(self.cuenta))
        self.agregar.setAutoDefault(True)
        self.agregar.setDisabled(True) #hasta que se habra o cree un archivo
        self.layoutbotones.addWidget(self.agregar,0,0, alignment = Qt.AlignCenter)

        self.modificar = QPushButton("Modificar Cuenta", self)
        self.modificar.setFixedWidth(150)
        self.modificar.setFixedHeight(20)
        self.modificar.clicked.connect(self.modificarEndixymyApp)
        self.modificar.clicked.connect(lambda: self.pressEnter(self.cuenta))
        self.modificar.setAutoDefault(True)
        self.modificar.setDisabled(True) #hasta que se seleccione una fila o registro de cuenta
        self.layoutbotones.addWidget(self.modificar,0,1, alignment = Qt.AlignCenter)

        self.eliminar = QPushButton("Eliminar Cuenta", self)
        self.eliminar.setFixedWidth(150)
        self.eliminar.setFixedHeight(20)
        self.eliminar.clicked.connect(self.eliminarDedixymyApp)
        self.eliminar.clicked.connect(lambda: self.pressEnter(self.cuenta))
        self.eliminar.setAutoDefault(True)
        self.eliminar.setDisabled(True) #hasta que se seleccione una fila o registro de cuenta
        self.layoutbotones.addWidget(self.eliminar,0,2, alignment = Qt.AlignCenter)

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
        #self.tableView.horizontalHeader().setStretchLastSection(True) #para que ocupe todo el ancho
        self.tableView.verticalHeader().setDefaultSectionSize(18)
        #self.tableView.verticalHeader().setHighlightSections(False) #hace que no se seleccionen los indices
        #self.tableView.verticalHeader().setVisible(True) #oculta los indices
        #self.tableView.setCornerButtonEnabled(True)
        #self.tableView.verticalHeader().hide() #otro metodo de ocultar los indices
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.AnyKeyPressed|QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed|QtWidgets.QAbstractItemView.SelectedClicked)

        self.tableLabel = QLabel('Listado',self)
        self.layouttabla.addWidget(self.tableLabel,5,0, alignment = Qt.AlignTop)
        self.layouttabla.addWidget(self.tableView,5,1)
        
        #Alertas Iconográficas (ver posibles funciones)
        AlertadeGuardadoPixmap = QPixmap('icons/savealertred.png')
        self.AlertadeGuardado = QLabel('Alerta Cambios no Guardados!!!', self)
        self.AlertadeGuardado.setStatusTip('Alerta Cambios no Guardados!!!')
        self.AlertadeGuardado.setScaledContents(True)
        self.AlertadeGuardado.setFixedSize(55,55)
        self.AlertadeGuardado.setPixmap(AlertadeGuardadoPixmap)
        self.AlertadeGuardado.move(0,305)
        self.AlertadeGuardado.hide()        

        AlertadeGuardadookPixmap = QPixmap('icons/savegreen.png')
        self.AlertadeGuardadook = QLabel('Alerta Cambios Guardados', self)
        self.AlertadeGuardadook.setStatusTip('Alerta Cambios Guardados!')
        self.AlertadeGuardadook.setScaledContents(True)
        self.AlertadeGuardadook.setFixedSize(55,55)
        self.AlertadeGuardadook.setPixmap(AlertadeGuardadookPixmap)
        self.AlertadeGuardadook.move(0,305)
        self.AlertadeGuardadook.hide()        
        
        LLavePixmap = QPixmap('icons/pkeypred.png')
        self.AlertadeLLavepnc = QLabel('Alerta llave No Creada', self)
        self.AlertadeLLavepnc.setStatusTip('Alerta llave No Creada!!!')
        self.AlertadeLLavepnc.setScaledContents(True)
        self.AlertadeLLavepnc.setFixedSize(55,55)
        self.AlertadeLLavepnc.setPixmap(LLavePixmap)
        self.AlertadeLLavepnc.move(0,252)
        self.AlertadeLLavepnc.hide()

        LLavePixmap = QPixmap('icons/pkeypgreen.png')
        self.AlertadeLLavepc = QLabel('Alerta llave Creada', self)
        self.AlertadeLLavepc.setStatusTip('Alerta llave Creada!')
        self.AlertadeLLavepc.setScaledContents(True)
        self.AlertadeLLavepc.setFixedSize(55,55)
        self.AlertadeLLavepc.setPixmap(LLavePixmap)
        self.AlertadeLLavepc.move(0,252)
        self.AlertadeLLavepc.hide()

        #generacion de clave 28/02/2023
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
        
        LLavePixmap = QPixmap('icons/pkeyp.png')
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
        #para debug
        #enigmaVentana.cleanconsole()
        print(pd.DataFrame(self.dixymyApp))
        self.show

    def tableviewClick(self):
        index=(self.tableView.selectionModel().currentIndex())
        value=index.sibling(index.row(),index.column()).data()
        print('click en fila:',index.row(),'columna:',index.column(),'contenido:',value)
        #tomar la fila para modificar self.dixymyApp asi: self.indiceFilaselec = index.row()
        self.cuenta.setText(index.sibling(index.row(),0).data())
        self.usuario.setText(index.sibling(index.row(),1).data())
        self.password.setText(index.sibling(index.row(),2).data())
        #al tocar en la tabla se habilitan botones modificar y eliminar.
        self.indiceFilaselec = index.row()
        print('indice fila seleccionada:',self.indiceFilaselec)
        self.indicadorRegselec.setText(str(self.indiceFilaselec))
        self.modificar.setDisabled(False) 
        self.eliminar.setDisabled(False)
        #ver estas variables al clic en tabla luego de los eventos
        if self.clavePrivada != '':
            self.Encrypt.setDisabled(False)
            self.Decrypt.setDisabled(False)
            self.EnigmaEncrypt.setDisabled(False)
            self.EnigmaDecrypt.setDisabled(False)

    def nuevoArchivo(self):
        if self.huboCambios:
            eleccion = self.cambiosSinguardar('Está Seguro que Desea Crear Otro Archivo?') #continuar, salir de todos modos, seguir con esta vida absurda alejado de Dios y de los Pandas?
            print('mi eleccion:',eleccion) #['Si','Guardado','Cancelar']
            if eleccion == 'Guardado' or eleccion == 'Si':
                print('eligió "Guardar" o "Si", se creará archivo')
                archivo_en_uso = self.Archivo
                self.Archivo, _ = QtWidgets.QFileDialog.getSaveFileName (
                    self, "Nuevo archivo", "", "Archivo Enigma (*.ef)"
                )
                if self.Archivo:
                    self.dixymyApp = {"cnt": [], "usr": [], "pssw": [], "encf": []}
                    guardarArchivo(self.Archivo, self.dixymyApp)
                    self.sicreonuevooAbroexistente()
                else:
                    self.Archivo = archivo_en_uso
            elif eleccion == 'Cancelar':
                print('eligió "Cancelar", sigue a ventana principal sin cambios')
                #sigue a ventana principal sin cambios
            else:
                print('sabrá Dios como llegó aquí')
        else:
            temp_archivo=self.Archivo
            self.Archivo, _ = QtWidgets.QFileDialog.getSaveFileName (
                    self, "Nuevo archivo", "", "Archivo Enigma (*.ef)"
                )
            if self.Archivo:
                self.dixymyApp = {"cnt": [], "usr": [], "pssw": [], "encf": []}
                guardarArchivo(self.Archivo, self.dixymyApp)
                self.sicreonuevooAbroexistente()
            else:
                self.Archivo=temp_archivo
        self.sicreoabroguardooGuardocomo()

    def abrirArchivo(self):
        if self.huboCambios:
            eleccion = self.cambiosSinguardar('Está Seguro que Desea Abrir Otro Archivo?') #continuar, salir de todos modos, seguir con esta vida absurda alejado de Dios y de los Pandas?
            print('mi eleccion:',eleccion) #['Si','Guardado','Cancelar']
            if eleccion == 'Guardado' or eleccion == 'Si':
                print('eligió "Guardar" o "Si", se abrirá archivo')
                archivo_en_uso = self.Archivo
                self.Archivo, _ = QtWidgets.QFileDialog.getOpenFileName(
                    self, "Abrir archivo", "", "Archivo Enigma (*.ef)"
                )
                if self.Archivo:
                    self.dixymyApp = cargarArchivo(self.Archivo)
                    self.sicreonuevooAbroexistente()
                else:
                    self.Archivo = archivo_en_uso
            elif eleccion == 'Cancelar':
                print('eligió "Cancelar", sigue a ventana principal sin cambios')
                #sigue a ventana principal sin cambios
            else:
                print('sabrá Dios como llegó aquí')
        else:
            temp_archivo=self.Archivo
            self.Archivo, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, "Abrir archivo", "", "Archivo Enigma (*.ef)"
            )
            if self.Archivo:
                self.dixymyApp = cargarArchivo(self.Archivo)
                self.sicreonuevooAbroexistente()
            else:
                self.Archivo=temp_archivo
        self.sicreoabroguardooGuardocomo()

    def cerrarArchivo(self):
        print('eligó cerrar archivo')
        if self.huboCambios:
            eleccion = self.cambiosSinguardar('Está Seguro que Desea Cerrar el Archivo Actual?') #continuar, salir de todos modos, seguir con esta vida absurda alejado de Dios y de los Pandas?
            print('mi eleccion:',eleccion) #['Si','Guardado','Cancelar']
            if eleccion == 'Guardado' or eleccion == 'Si':
                print('eligió "Guardar" o "Si", se cerrará archivo')
                self.condicionesIniciales()
            elif eleccion == 'Cancelar':
                print('eligió "Cancelar", sigue a ventana principal sin cambios')
        else:
            self.condicionesIniciales()

    def condicionesIniciales(self):
        print('Seteando Condiciones Iniciales...')
        self.dixymyApp = {"cnt": [], "usr": [], "pssw": [], "encf": []}
        self.clavePrivada = ''
        self.Archivo = '' #contenedor fisico de claves
        self.huboCambios = False
        self.cambiosGuardados = True #evaluar
        #en submenu y toolbar archivo 
        self.guardarSubmenu.setDisabled(True)
        self.save.setDisabled(True) 
        self.guardarcomoSubmenu.setDisabled(True)
        self.saveas.setDisabled(True) 
        self.cerrarArchivoSubmenu.setDisabled(True)
        self.closea.setDisabled(True) 
        #en menu enigma y toolbar enigma
        self.EnigmaEnigma.setEnabled(False)
        #armado de pantalla inicial modo registro
        self.modoRegistros()
        #y si hago lo que sea tengo que hacer...
        self.sihagoLoquesea()
        #botones de modo registro
        self.agregar.setDisabled(True) #hasta que se habra o cree un archivo
        #campos de entrada de texto
        self.cuenta.setEnabled(False)
        self.usuario.setEnabled(False)
        self.password.setEnabled(False)
        #
        self.AlertadeGuardado.hide()
        self.AlertadeGuardadook.hide() 
        self.setWindowTitle(self.title)
        self.indicadorArchivo.setText('Debe crear un archivo nuevo o abrir uno existente!')
        self.indicadorArchivo.setStyleSheet('background-color: red; color: yellow')
        #
                
    def sicreonuevooAbroexistente(self):
        self.EnigmaEnigma.setEnabled(True) # ver 08/03/2023
        self.agregar.setDisabled(False)
        
        self.save.setDisabled(True)
        self.saveas.setDisabled(False)
        self.closea.setDisabled(False)
        
        self.cuenta.setEnabled(True)
        self.usuario.setEnabled(True)
        self.password.setEnabled(True)

        self.guardarSubmenu.setDisabled(True)
        self.guardarcomoSubmenu.setDisabled(False)
        self.cerrarArchivoSubmenu.setDisabled(False)
        
        self.AlertadeGuardado.hide()
        self.AlertadeGuardadook.hide()

    def guardarArchivoef(self):
        print(pd.DataFrame(self.dixymyApp)) #por debug
        self.alguardaroguardarcomo()
        self.sicreoabroguardooGuardocomo()
 
    def guardarComo(self):
        print(pd.DataFrame(self.dixymyApp)) #por debug
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
        print(self.Archivo)
        guardarArchivo(self.Archivo, self.dixymyApp)
        self.huboCambios = False #porque ya se guardaron
        self.cambiosGuardados = True
        self.AlertadeGuardado.hide()
        self.AlertadeGuardadook.show()
        self.guardarSubmenu.setDisabled(True)
        self.save.setDisabled(True) 

    def sicreoabroguardooGuardocomo(self):
        #self.EnigmaEnigma.setEnabled(True)  #08/03/2023 ver esta condicion
        self.sihagoLoquesea()

    def agregarAdixymyApp(self):
        agregarCuenta(self.dixymyApp,'cnt',self.cuenta.text())
        agregarCuenta(self.dixymyApp,'usr',self.usuario.text())
        agregarCuenta(self.dixymyApp,'pssw',self.password.text())
        agregarCuenta(self.dixymyApp,'encf','no')
        self.siagregomodificooElimino()

    def modificarEndixymyApp(self):
        #print('quiere modificar el indice',self.indiceFilaselec,'? pague la version completa raton!!!')
        print('modificando el indice',self.indiceFilaselec)
        self.dixymyApp['cnt'][self.indiceFilaselec]=self.cuenta.text()
        self.dixymyApp['usr'][self.indiceFilaselec]=self.usuario.text()
        self.dixymyApp['pssw'][self.indiceFilaselec]=self.password.text()
        self.dixymyApp['encf'][self.indiceFilaselec]='no'
        self.siagregomodificooElimino()       

    def eliminarDedixymyApp(self):
        print('eliminando cuenta seleccionada')
        del self.dixymyApp['cnt'][self.indiceFilaselec]
        del self.dixymyApp['usr'][self.indiceFilaselec]
        del self.dixymyApp['pssw'][self.indiceFilaselec]
        del self.dixymyApp['encf'][self.indiceFilaselec]
        self.siagregomodificooElimino()

    def siagregomodificooElimino(self):
        self.huboCambios = True
        self.cambiosGuardados = False
        self.AlertadeGuardado.show()
        self.AlertadeGuardadook.hide()
        self.guardarSubmenu.setDisabled(False)
        self.save.setDisabled(False) 
        #self.EnigmaEnigma.setEnabled(False)  #08/03/2023 ver esta condicion
        self.sihagoLoquesea()

    def sihagoLoquesea(self):
        self.indiceFilaselec = ''
        self.dixyTotable(self.dixymyApp)
        self.eliminar.setDisabled(True)
        self.modificar.setDisabled(True)
        self.Encrypt.setDisabled(True)
        self.Decrypt.setDisabled(True)
        self.EnigmaEncrypt.setDisabled(True)
        self.EnigmaDecrypt.setDisabled(True)
        self.limpiarCampos()
        self.pressEnter(self.cuenta)            

    def dixyTotable(self, dixy):
        df = pd.DataFrame(dixy)
        print(df)
        # usar el dataframe que mejor aplique al programa
        model = PandasModel5(df) #no soporta ordenamiento por columnas (muestra indices)
        #model = PandasModel(df) #soporta ordenamiento por columnas (muestra indices)
        #model = DataFrameModel(df) #soporta ordenamiento de columnas (muestra indices)
        #model = PandasModel3(df) #soporta ordenamiento de columnas (no muestra indices)
        #model = PandasModel4(df) #soporta ordenamiento de columnas (no muestra indices)
        self.tableView.setModel(model)
        #for i in range (len(df.columns)):
        #    self.tableView.resizeColumnToContents(i) #ajusta por indice de columna
        self.tableView.resizeColumnsToContents() #ajusta a todas
        self.tableView.scrollToBottom()
        #seguimiento de archivo abierto
        self.setWindowTitle(self.shorttitle+self.Archivo)
        self.indicadorArchivo.setStyleSheet('background-color: green; color: white')
        self.indicadorArchivo.setText('file:'+self.Archivo)
        #para debug
        print('len(df.index)',len(df.index)) #evalua tamaño de dataframe con pandas
        print('len dict["cnt"]',len(dixy['cnt']))
        print('len dict["usr"]',len(dixy['usr']))
        print('len dict["pssw"]',len(dixy['pssw']))
        print('len dict["encf"]',len(dixy['encf']))
        #contador de registros
        self.indicadorRegistros.setText(str(len(dixy['cnt'])))
        if (len(dixy['cnt'])) == 0:
            self.modificar.setDisabled(True) 
            self.eliminar.setDisabled(True) 
        #seguimiento de fila seleccionada
        self.indicadorRegselec.setText(str(self.indiceFilaselec))

    def limpiarCampos(self):
        self.cuenta.clear()
        self.usuario.clear()
        self.password.clear()

    def pressEnter(self, campo):
        campo.setFocus()    
        
    def closeEvent(self, event):
        if self.huboCambios == True:# or self.cambiosGuardados == False:
            eleccion = self.cambiosSinguardar('Está Seguro que Desea Salir?') #continuar, salir de todos modos, seguir con esta vida absurda alejado de Dios y de los Pandas?
            print('mi eleccion:',eleccion) #['Si','Guardado','Cancelar']
            if eleccion == 'Si':
                event.accept()
                self.close()

            elif eleccion == 'Guardado':
                event.accept()
                print('se guardó y ahora se cierra programa')
                self.close()

            elif eleccion == 'Cancelar':
                event.ignore()
                self.window()
                self.pressEnter(self.cuenta)

            else:
                event.ignore()
                print('dios sabe que habra eligido usted, amén!')
                self.window()
                self.pressEnter(self.cuenta)
            
        else:
            df=pd.DataFrame(self.dixymyApp)
            print('\nSaliendo... len(df.index)',len(df.index)) #evalua tamaño de dataframe con pandas
            print('CambiosGuardados: ',self.cambiosGuardados)
            print('archivo:', self.Archivo)
            if (len(df.index)) == 0 :
                print('Saliendo...')
                if self.cambiosGuardados == False:
                    print('...se eliminará archivo no guardado:', self.Archivo)
                    os.remove(self.Archivo)
        
        self.close()
    
    def cambiosSinguardar(self, mensaje):
        if self.huboCambios == True:# or self.cambiosGuardados == False:
            msg = QtWidgets.QMessageBox.question(self, mensaje, "Hay cambios sin guardar, Elija una Opción...\nJesús enseña a sus disipulos a ser prudentes!", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Save)
            
            if msg == QtWidgets.QMessageBox.Yes:
                print('eligió continuar sin guardar')
                return 'Si'

            elif msg == QtWidgets.QMessageBox.Save:
                print('eligió guardar')
                self.guardarArchivoef()
                print('se guardó y ahora continua flujo de programa')
                return 'Guardado'

            elif msg == QtWidgets.QMessageBox.Cancel:
                print('eligió cancelar')
                return 'Cancelar'

            else:
                print('dios sabe que habra eligido usted, amén!')
                self.window()
                self.pressEnter(self.cuenta)

    def modoTemaClasico(self):
        app.setStyleSheet("")
        app.setStyle('Fusion')
        self.correccioTemas()
    
    def modoTemaClaro(self):
        app.setStyleSheet(qdarkstyle.load_stylesheet(LightPalette))
        self.correccioTemas()

    def modoTemaOscuro(self):
        app.setStyleSheet(qdarkstyle.load_stylesheet(DarkPalette))
        self.correccioTemas()

    def correccioTemas(self):
        print(app.style().metaObject().className())
        if app.style().metaObject().className() == 'QFusionStyle':  
            self.indicadorRegselec.move(200,200)
        else: #para QStyleSheetStyle
            self.indicadorRegselec.move(200,190)

    def appCerrar(self):
        self.close()
        #app.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QMainWindow().setWindowModality(QtCore.Qt.ApplicationModal)
    #app.setStyle('Windows')
    #app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    #app.setStyleSheet(qdarkstyle.load_stylesheet(LightPalette))
    #app.setStyleSheet(qdarkstyle.load_stylesheet(DarkPalette))
    ventana = enigmaVentana()
    ventana.show()
    sys.exit(app.exec_())