from io import SEEK_CUR
import sys

from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QShortcut, QStackedLayout, QStackedWidget, QWidget
from PyQt5.QtCore import QTimer, QTime, QDate,pyqtSignal, QEvent
from PyQt5 import QtWidgets
from PyQt5.uic.uiparser import QtCore
from serial import serial_for_url
import comunication_serial

class main(QMainWindow):
    def __init__(self):
        super().__init__()
        # cargamos la página principal.
        uic.loadUi("guide/ventana_principal.ui",self)
        self.setupUI()
        # definimos las variables extras.
        self.enable_lcd = False
        self.str_lcd = ""
        self.cont_num_lcd = 0
        self.cont_horas = 0
        self.enable_lcd_int = False
        self.enable_lcd_float = False
        self.digits_horas = ""
        # variables de configuracion.
        self.num_est = 1           # número de estación actual.
        self.tipo_riego = [0,0,0]  # vector de tipo de riego.

    def setupUI(self):
        # creamos las páginas.
        self.cont_screen21_rep = 0
        self.cont_screen22_rep = 0
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        self.pages = QStackedLayout()
        centralWidget.setLayout(self.pages)

        self.screen0 = anuncio_00()
        self.screen1 = anuncio_01()
        self.screen2 = anuncio_02()
        self.screen3 = anuncio_03()
        self.screen21 = anuncio_021(0,1)
        self.screen22 = anuncio_022(1)
        self.screen31 = anuncio_031(1)
        self.screen311 = anuncio_0311(1)
        self.screen312 = anuncio_0312(1)
        self.screen313 = anuncio_0313(1)
        self.screen3111 = anuncio_03111(1)
        self.screen3112 = anuncio_03112(1)
        self.screen3113 = anuncio_03113()
        self.screen3121 = anuncio_03121(1)
        self.screen3122 = anuncio_03122(1)
        self.screen31111 = anuncio_031111(1)
        self.screen31112 = anuncio_031112(1)
        self.screen31113 = anuncio_031113(1)
        self.screen31211 = anuncio_031211(1)
        self.screen311111 = anuncio_0311111()
        self.screen311112 = anuncio_0311112()
        self.screen3111121 = anuncio_03111121()
        self.screen3111122 = anuncio_03111122()
        self.screen3111123 = anuncio_03111123()
        self.screen311121 = anuncio_0311121()
        self.screen311122 = anuncio_0311122()
        self.screen311131 = anuncio_0311131()
        self.screen311132 = anuncio_0311132()
        self.screen312111 = anuncio_0312111()
        self.screen312112 = anuncio_0312112()
        self.screen312113 = anuncio_0312113()
        self.screen23 = anuncio_023(0,1,False)
        self.screen24 = anuncio_024(0,1,False)

        self.pages.addWidget(self.screen0)
        self.pages.addWidget(self.screen1)
        self.pages.addWidget(self.screen2)
        self.pages.addWidget(self.screen3)
        self.pages.addWidget(self.screen21)
        self.pages.addWidget(self.screen22)
        self.pages.addWidget(self.screen31)
        self.pages.addWidget(self.screen311)
        self.pages.addWidget(self.screen312)
        self.pages.addWidget(self.screen313)
        self.pages.addWidget(self.screen3111)
        self.pages.addWidget(self.screen3112)
        self.pages.addWidget(self.screen3113)
        self.pages.addWidget(self.screen3121)
        self.pages.addWidget(self.screen3122)
        self.pages.addWidget(self.screen31111)
        self.pages.addWidget(self.screen31112)
        self.pages.addWidget(self.screen31113)
        self.pages.addWidget(self.screen31211)
        self.pages.addWidget(self.screen311111)
        self.pages.addWidget(self.screen311112)
        self.pages.addWidget(self.screen3111121)
        self.pages.addWidget(self.screen3111122)
        self.pages.addWidget(self.screen3111123)
        self.pages.addWidget(self.screen311121)
        self.pages.addWidget(self.screen311122)
        self.pages.addWidget(self.screen311131)
        self.pages.addWidget(self.screen311132)
        self.pages.addWidget(self.screen312111)
        self.pages.addWidget(self.screen312112)
        self.pages.addWidget(self.screen312113)
        self.pages.addWidget(self.screen23)
        self.pages.addWidget(self.screen24) 

        ## etapa de envío de datos.
        self.reloj = QTimer(self)
        self.reloj.timeout.connect(self.enviar_datos)
        self.reloj.start(1000)
        
    def enviar_datos(self):
        self.hora_actual = QTime.currentTime()
        self.fecha_actual = QDate.currentDate()
        self.hora = self.hora_actual.hour()
        self.minuto = self.hora_actual.minute()
        self.segundo = self.hora_actual.second()
        print("{0}:{1}:{2}".format(self.hora,self.minuto,self.segundo))
        if ((self.minuto%2) == 0 and self.segundo == 0):
            fecha = "{0}/{1}/{2};{3}:{4}:{5}".format(self.fecha_actual.year(),self.fecha_actual.month(),self.fecha_actual.day(),self.hora,self.minuto,self.segundo)
            print(fecha)
            comunication_serial.enviar_datos(arduino1,fecha)

    def keyPressEvent(self, event):
        self.key = event.text()
        self.screen_num = self.pages.currentIndex()
        print("Tecla:{0} \t pantalla:{1}".format(self.key,self.screen_num))

        if (self.key == 'a'):
            self.GoToinitialPage()

        if (self.screen_num == 0): 
            if (self.key == '0'):
                self.GoTohomePage()

        ##### Pantalla de inicio ##########        
        if (self.screen_num == 1):
            if (self.key == '1'):
                self.GoToShowDataPage()
            if (self.key == '2'):
                self.GoToConfigPage()
        ##########################################
        ##### Pantalla de mostrar datos ##########
        ##########################################        
        if (self.screen_num == 2):
            self.tipo_riego = self.screen1.tipo_riego_est
            if (self.key == '1'):
                if (self.tipo_riego[0] == 1):
                    self.num_est = 1
                    self.screen21.modif_lbl(self.tipo_riego[0],self.num_est)
                    self.GoToEstData()
                else:
                    self.num_est = 1
                    self.screen23.send_enable = True
                    self.GoToShowSensorData()


            if (self.key == '2'):
                if (self.tipo_riego[1] == 1):
                    self.num_est = 2
                    self.screen21.modif_lbl(self.tipo_riego[1],self.num_est)
                    self.GoToEstData()
                else:
                    self.num_est = 2
                    self.screen23.send_enable = True
                    self.GoToShowSensorData()

            if (self.key == '3'):
                if (self.tipo_riego[2] == 1):
                    self.num_est = 3
                    self.screen21.modif_lbl(self.tipo_riego[2],self.num_est)
                    self.GoToEstData()
                else:
                    self.num_est = 3
                    self.screen23.send_enable = True
                    self.GoToShowSensorData()

            if (self.key == '-'):
                # obtenemos el tipo de riego configurado.
                self.GoTohomePage()
        
        ## datos programa inteligente 1 ##
        if (self.screen_num == 4):
            if (self.key == '+'):
                self.screen22.modif_lbl(self.num_est)
                self.GoToEstData2()

            if (self.key == '-'):
                self.GoToShowDataPage()
            
        ## datos programa inteligente 1 ##
        if (self.screen_num == 5):
            if (self.key == '-'):
                self.GoToEstData()
        
        ##########################################
        ##### Pantalla de configuración ##########
        ##########################################
        if (self.screen_num == 3):
            if (self.key == '1'):
                print("est 1")
                self.num_est = 1
                self.screen31.modif_lbl(self.num_est)
                self.GoToTipoRiego()

            if (self.key == '2'):
                self.num_est = 2
                self.screen31.modif_lbl(self.num_est)
                self.GoToTipoRiego()
                
            if (self.key == '3'):
                self.num_est = 3
                self.screen31.modif_lbl(self.num_est)
                self.GoToTipoRiego()

            if (self.key == '-'):
                self.screen1.modif_lbl_riego()
                self.GoTohomePage()
        
        #### Tipo de riego ####
        if (self.screen_num == 6):
            # Riego inteligente.
            if (self.key == '1'):
                self.screen311.modif_lbl(self.num_est)
                self.GoToRiegoIntel()
            # Riego automático
            if (self.key == '2'):
                self.screen312.modif_lbl(self.num_est)
                self.GoToRiegoAuto()
            # Riego manual.    
            if (self.key == '3'):
                self.screen313.modif_lbl(self.num_est)
                self.GoToRiegoManual()
            # Atras.
            if (self.key == '-'):
                self.GoTohomePage()
        
        ## Riego inteligente.##
        if (self.screen_num == 7):
            # Registrar sensores.
            if (self.key == '1'):
                self.screen3111.modif_lbl(self.num_est)
                self.GoToNewSensor()
            # Definir datos del suelo.
            if (self.key == '2'):
                self.screen3112.modif_lbl(self.num_est)
                self.GoToGroundData()
            # Lamina y tiempo de riego.
            if (self.key == '3'):
                self.GoToIrrigationTime()
            # Atras.
            if (self.key == '-'):
                self.GoToTipoRiego()

        ## Riego programado ##
        if (self.screen_num == 8):
            # Configurar programa.
            if (self.key == '1'):
                self.screen3121.modif_lbl(self.num_est)
                self.GoToConfigProg()
            # Seleccionar programa.
            if (self.key == '2'):
                self.screen3122.modif_lbl(self.num_est)
                self.goToSelectProg()
            # Atras.
            if (self.key == '-'):
                self.GoToTipoRiego()
                
        ## Riego manual ##
        if (self.screen_num == 9):
            # Habilitar riego.
            if (self.key == '1'):
                ########### Cambiar a modo riego #########
                estaciones[self.num_est -1].modif_riego(2)
                self.tipo_riego[self.num_est -1] = 2
                ##########################################
                self.GoToTipoRiego()
                
            # No habilitar riego.
            if (self.key == '2'):
                self.GoToTipoRiego()

        ## registrar sensores ##
        if (self.screen_num == 10):
            # Sensor de humedad del suelo
            if (self.key == '1'):
                self.screen31111.modif_lbl(self.num_est)
                self.GoToNewVWC()
            # Sensor de temperatura del ambiente.
            if (self.key == '2'):
                self.screen31112.modif_lbl(self.num_est)
                self.GoToNewTamb()
            # Sensor de humedad del ambiente.
            if (self.key == '3'):
                self.screen31113.modif_lbl(self.num_est)
                self.GoToNewHamb()
            # Atras.
            if (self.key == '-'):
                self.GoToRiegoIntel()
                
        ## definir parámetros del suelo ###
        if (self.screen_num == 11):
            self.screen3112.modif_lbl(self.num_est) 
            lcd_display = [self.screen3112.lcd_number_1,self.screen3112.lcd_number_2]
            self.introducirDatos(lcd_display,event,32,'c',16777220)
            if (self.finish):
                self.pmp = self.result[0]
                self.cc = self.result[1]
                print("pmp = {}".format(self.pmp))
                print("cc = {}".format(self.cc))
                self.GoToRiegoIntel()
            if (self.key == '-'):
                self.GoToRiegoIntel()
        ## definir parámetros de lámina y tiempo de riego ###
        if (self.screen_num == 12):
            lcd_display = [self.screen3113.lcd_number_1,self.screen3113.lcd_number_2,self.screen3113.lcd_number_3,self.screen3113.lcd_number_4]
            self.introducirDatos(lcd_display,event,32,'c',16777220)
            if (self.finish):
                self.pr = self.result[0]
                self.ur = self.result[1]
                self.area = self.result[2]
                self.caudal = self.result[3]
                print("pr = {}".format(self.pr))
                print("ur = {}".format(self.ur))
                print("area = {}".format(self.area))
                print("caudal = {}".format(self.caudal))
                self.GoToRiegoIntel()
            if (self.key == '-'):
                self.GoToRiegoIntel()

        if (self.screen_num == 13):
            # Sensor de humedad del suelo
            if (self.key == '1'):
                self.num_progr = 'A'
                self.prog_riego_prog = 0
                self.screen31211.modif_lbl(self.num_progr) 
                self.GoToProg()
            # Sensor de temperatura del ambiente.
            if (self.key == '2'):
                self.num_progr = 'B'
                self.prog_riego_prog = 1
                self.screen31211.modif_lbl(self.num_progr) 
                self.GoToProg()
            # Sensor de humedad del ambiente.
            if (self.key == '3'):
                self.num_progr = 'C'
                self.prog_riego_prog = 2
                self.screen31211.modif_lbl(self.num_progr) 
                self.GoToProg()
            if (self.key == '4'):
                self.num_progr = 'D'
                self.prog_riego_prog = 3
                self.screen31211.modif_lbl(self.num_progr) 
                self.GoToProg()
            # Atras.
            if (self.key == '-'):
                self.GoToRiegoAuto()
        # seleccionar programa.
        if (self.screen_num == 14):
            self.screen3122.modif_lbl(self.num_est) 
            check_box = [self.screen3122.checkBox_1,self.screen3122.checkBox_2,self.screen3122.checkBox_3,self.screen3122.checkBox_4]
            self.seleccionarUnaOpcion(check_box,event,16777220)
            if (self.finishCheck):
                self.num_programa = self.result_prog
                print("Programa {}".format(self.num_programa))
                estaciones[self.num_est-1].modif_num_prog(self.num_programa)
                self.GoToRiegoAuto()

            if (self.key == '-'):
                self.GoToRiegoAuto()
        
        if (self.screen_num == 15):
            if (self.key == '1'):
                self.screen311111 = anuncio_0311111()
                self.GoToNameVWC()

            if (self.key == '2'):
                self.screen311112 = anuncio_0311112()
                self.GoToTypEqVWC()
                
            if (self.key == '-'):
                self.GoToNewSensor()   
        # registrar nuevo sensor de temperatura.
        if (self.screen_num == 16):
            if (self.key == '1'):
                self.screen311121 = anuncio_0311121()
                self.GoToNameTa()

            if (self.key == '2'):
                self.screen311122 = anuncio_0311122()
                self.GoToLimTa()
                
            if (self.key == '-'):
                self.GoToNewSensor()  
        # registrar nuevo sensor de humedad.
        if (self.screen_num == 17):
            if (self.key == '1'):
                self.screen311131 = anuncio_0311131()
                self.GoToNameHa()

            if (self.key == '2'):
                self.screen311132 = anuncio_0311132()
                self.GoToLimHa()
                
            if (self.key == '-'):
                self.GoToNewSensor() 
        
        # Menu de configurar programa,
        if (self.screen_num == 18):
            # definir dias.
            if (self.key == '1'):
                self.screen312111 = anuncio_0312111()
                self.GoToDay()
            # definir hora de inicio.
            if (self.key == '2'):
                self.screen312112 = anuncio_0312112()
                self.GoToStartHour()
            # definir tiempo de riego.
            if (self.key == '3'):
                self.screen312113 = anuncio_0312113()
                self.GoToSetIrrigationTime()
            # Atras    
            if (self.key == '-'):
                self.GoToConfigProg()
        
        # nombre de sensor de humedad del suelo.
        if (self.screen_num == 19):
            lcd_data_int = [self.screen311111.lcd_number_1]
            lcd_data_float = [self.screen311111.lcd_number_2]
            self.introdMixDatos(lcd_data_int,lcd_data_float,event,32,'c',16777220, 10)
            # Atras    
            if (self.key == '-'):
                self.enable_lcd_int = False
                self.enable_lcd_float = False
                self.str_lcd = ""
                self.cont_num_lcd = 0
                self.GoToNewVWC()
            if (self.finish_mix):
                self.num_vwc = self.result[0]
                self.prof = self.result[1]
                print("vwc: {}".format(self.num_vwc))
                print("prof: {}".format(self.prof))
                self.GoToNewVWC()
        # Ecuaciones a usar 
        if (self.screen_num == 20):
            # ecuación de primer grado.
            if (self.key == '1'):
                self.screen3111121 = anuncio_03111121()
                self.GoToGrade1()
            # ecuación de segundo grado.
            if (self.key == '2'):
                self.screen3111122 = anuncio_03111122()
                self.GoToGrade2()
            # ecuación de tercer grado.
            if (self.key == '3'):
                self.screen3111123 = anuncio_03111123()
                self.GoToGrade3()
            # Atras    
            if (self.key == '-'):
                self.GoToNewVWC()
        
        # Nuevo Ta
        if (self.screen_num == 21):
            lcd_display = [self.screen311121.lcd_number_1]
            self.introducirDatosInt(lcd_display,event,32,'c',16777220,10)
            # condicion de fin
            if (self.finish):
                self.num_Ta = self.result[0]
                print("Ta: {}".format(self.num_Ta))
                self.GoToNewTamb()
            # Atras    
            if (self.key == '-'):
                self.enable_lcd = False
                self.str_lcd = ""
                self.cont_num_lcd = 0
                self.GoToNewTamb()
        # limites valor de temperatura.
        if (self.screen_num == 22):
            
            lcd_display = [self.screen311122.lcd_number_1, self.screen311122.lcd_number_2]
            lbl_signo = [self.screen311122.lbl_signo_1, self.screen311122.lbl_signo_2]
            self.introducirDatosSigno(lcd_display,lbl_signo,event,32,'c',16777220,'s')

            # condicion de fin
            if (self.finish):
                self.max_Ta = self.result[0]
                self.min_Ta = self.result[1]
                print("Ta max: {}".format(self.max_Ta))
                print("Ta min: {}".format(self.min_Ta))
                self.GoToNewTamb()
            # Atras    
            if (self.key == '-'):
                self.enable_lcd = False
                self.str_lcd = ""
                self.cont_num_lcd = 0
                self.GoToNewTamb()
        
        if (self.screen_num == 23):
            lcd_display = [self.screen311131.lcd_number_1]
            self.introducirDatosInt(lcd_display,event,32,'c',16777220,10)
            # condicion de fin
            if (self.finish):
                self.num_Ha = self.result[0]
                print("Ha: {}".format(self.num_Ha))
                self.GoToNewHamb()
            # Atras    
            if (self.key == '-'):
                self.enable_lcd = False
                self.str_lcd = ""
                self.cont_num_lcd = 0
                self.GoToNewHamb()
        # limites valor de temperatura.
        if (self.screen_num == 24):
            lcd_display = [self.screen311132.lcd_number_1, self.screen311132.lcd_number_2]
            lbl_signo = [self.screen311132.lbl_signo_1, self.screen311132.lbl_signo_2]
            self.introducirDatosSigno(lcd_display,lbl_signo,event,32,'c',16777220,'s')

            # condicion de fin
            if (self.finish):
                self.max_Ha = self.result[0]
                self.min_Ha = self.result[1]
                print("Ha max: {}".format(self.max_Ha))
                print("Ha min: {}".format(self.min_Ha))
                self.GoToNewHamb()
            # Atras    
            if (self.key == '-'):
                self.enable_lcd = False
                self.str_lcd = ""
                self.cont_num_lcd = 0
                self.GoToNewHamb()

        if(self.screen_num == 25):
            check_box = [self.screen312111.checkBox_1,self.screen312111.checkBox_2,self.screen312111.checkBox_3,self.screen312111.checkBox_4,self.screen312111.checkBox_5,self.screen312111.checkBox_6,self.screen312111.checkBox_7]
            self.seleccionarOpciones(check_box,event,16777220)
            # guardar datos.
            if (self.finishCheck):
                self.dias_programa = self.result_check
                for x in self.result_check:
                    print(x)
                estaciones[self.num_est-1].modif_dias_riego_prog(self.dias_programa,self.prog_riego_prog)
                self.GoToProg()
            # Atras    
            if (self.key == '-'):
                self.GoToProg()
        # definir horas de riego.
        if (self.screen_num == 26):
            # widgets de las horas.
            widgets_horas = [self.screen312112.widget_1,self.screen312112.widget_2,self.screen312112.widget_3,self.screen312112.widget_4,self.screen312112.widget_5,self.screen312112.widget_6]

            lbls_horas = [self.screen312112.label_hora_1,self.screen312112.label_hora_2,self.screen312112.label_hora_3,self.screen312112.label_hora_4,self.screen312112.label_hora_5,self.screen312112.label_hora_6]
            self.addhours(widgets_horas,lbls_horas,event,32,'c',16777220)

            # Atras    
            if (self.key == '-'):
                self.screen312112 = anuncio_0312112()
                self.GoToProg()

            # condicion de fin
            if (self.finish):
                self.horas_prog = []
                for x in self.result:
                    self.horas_prog.append(x)
                    print("Hora: {0}".format(x))
                
                self.GoToProg()
        # Tiempo de riego 
        if (self.screen_num == 27):
            lcd_display = [self.screen312113.lcd_number_1]
            self.introducirDatosInt(lcd_display,event,32,'c',16777220,200000)
            # condicion de fin
            if (self.finish):
                self.tiempo_riego = self.result[0]
                print("Tiempo riego: {} minutos".format(self.tiempo_riego))
                self.GoToProg()
            # Atras    
            if (self.key == '-'):
                self.enable_lcd = False
                self.str_lcd = ""
                self.cont_num_lcd = 0
                self.GoToProg()
            

        # Ecuación lineal.
        if (self.screen_num == 28):
            
            lcd_display = [self.screen3111121.lcd_number_1, self.screen3111121.lcd_number_2]
            lbl_signo = [self.screen3111121.lbl_signo_1, self.screen3111121.lbl_signo_2]
            self.introducirDatosSigno(lcd_display,lbl_signo,event,32,'c',16777220,'s')

            # condicion de fin
            if (self.finish):
                self.a = self.result[0]
                self.b = self.result[1]
                print("a: {}".format(self.a))
                print("b: {}".format(self.b))
                self.GoToTypEqVWC()
            # Atras    
            if (self.key == '-'):
                self.enable_lcd = False
                self.str_lcd = ""
                self.cont_num_lcd = 0
                self.GoToTypEqVWC()
        
        # Ecuación cuadrática.
        if (self.screen_num == 29):
            
            lcd_display = [self.screen3111122.lcd_number_1, self.screen3111122.lcd_number_2,self.screen3111122.lcd_number_3]
            lbl_signo = [self.screen3111122.lbl_signo_1, self.screen3111122.lbl_signo_2, self.screen3111122.lbl_signo_3]
            self.introducirDatosSigno(lcd_display,lbl_signo,event,32,'c',16777220,'s')

            # condicion de fin
            if (self.finish):
                self.a = self.result[0]
                self.b = self.result[1]
                self.c = self.result[2]
                print("a: {}".format(self.a))
                print("b: {}".format(self.b))
                print("c: {}".format(self.c))
                self.GoToTypEqVWC()
            # Atras    
            if (self.key == '-'):
                self.enable_lcd = False
                self.str_lcd = ""
                self.cont_num_lcd = 0
                self.GoToTypEqVWC()

        # Ecuación cúbica.
        if (self.screen_num == 30):
            
            lcd_display = [self.screen3111123.lcd_number_1, self.screen3111123.lcd_number_2,self.screen3111123.lcd_number_3, self.screen3111123.lcd_number_4]
            lbl_signo = [self.screen3111123.lbl_signo_1, self.screen3111123.lbl_signo_2, self.screen3111123.lbl_signo_3, self.screen3111123.lbl_signo_4]
            self.introducirDatosSigno(lcd_display,lbl_signo,event,32,'c',16777220,'s')

            # condicion de fin
            if (self.finish):
                self.a = self.result[0]
                self.b = self.result[1]
                self.c = self.result[2]
                self.d = self.result[3]
                print("a: {}".format(self.a))
                print("b: {}".format(self.b))
                print("c: {}".format(self.c))
                print("d: {}".format(self.d))
                self.GoToTypEqVWC()
            # Atras    
            if (self.key == '-'):
                self.enable_lcd = False
                self.str_lcd = ""
                self.cont_num_lcd = 0
                self.GoToTypEqVWC()

        # Tiempo de riego 
        if (self.screen_num == 31):
            tipo_riego = self.screen1.tipo_riego_est
            # Siguente.
            if (self.key == '+'):
                self.screen23.send_enable = False
                self.screen24.show_enable = True
                self.screen24.actualizar_datos()
                self.GoToGroundData()
            # Atrás.
            if (self.key == '-'):
                self.screen23.send_enable = False
                if (tipo_riego[0] == 1):
                    self.GoToEstData2()
                    ############
                else:
                    self.GoToShowDataPage()
        # Datos del suelo.
        if (self.screen_num == 32):
            tipo_riego = self.screen1.tipo_riego_est
            # Siguente.
            if (self.key == '-'):
                self.screen23.send_enable = True
                self.screen24.show_enable = False
                self.GoToShowSensorData()
            
    # Añadir horas.
    def addhours(self,widgets_horas,label_horas,event,key_next,key_remove,key_finish):
        num_elem = len(widgets_horas)  # número de widgets.
        self.finish = False
        
        # definimos una tecla condicional para editar el lcd.
        if (event.key() == key_next):
            self.enable_lcd = True
            self.cont_digitos_hora = 0 
            self.cont_horas = self.cont_horas + 1
            self.cont_digitos_hora = 0
            self.digits_horas = ""

            if (self.cont_horas > num_elem):
                self.cont_horas = 0
                self.enable_lcd = False

        # una vez habilitado el lcd.
        if (self.enable_lcd):
            # Añadir datos.
            if (self.key != key_remove):
                # En caso de tener 4 elementos.
                hora_inicial = "0000"
                try:
                    self.digits_horas =  self.digits_horas + str(int(self.key))

                except:
                    print("Dato no entero")
                
                hora_inicial = self.digits_horas + hora_inicial 
                print(hora_inicial)
                hora_modif = hora_inicial[0:4]
                hora = int(hora_modif[0:2])
                minuto = int(hora_modif[2:4])
                print(hora)
                print(minuto)
                if (hora >23):
                    hora = 0
                    self.digits_horas = ""
                    
                if (minuto > 59):
                    minuto = 0
                    self.digits_horas = self.digits_horas[0:2]
                    

                time1 = QTime(hora,minuto)
                showTime1=time1.toString('hh:mm')
                label_horas[self.cont_horas-1].setText(showTime1)
                widgets_horas[self.cont_horas-1].show()
                # reinicio de contador.
                if (len(self.digits_horas) > 4):
                    self.digits_horas = ""

            # En caso de querer eliminar la hora actual.
            else:
                # Ocultamos el fichero actual.
                widgets_horas[self.cont_horas-1].hide()
                # Reducimos el valor del contador.
                self.cont_horas = self.cont_horas-1
                self.digits_horas = ""

        if (event.key() == key_finish):
            self.enable_lcd = False
            print("enter was pressed")
            self.result = []

            for i in range (0,self.cont_horas):
                self.result.append(label_horas[i].text())
            self.cont_horas = 0
            self.digits_horas = ""
            self.finish = True 


    # introducir datos enteros.
    def introducirDatosInt(self,lcd_display,event,key_next,key_erase,key_finish, lim_int):
        num_elem = len(lcd_display)  # número de LCD a configurar.
        self.finish = False
        # una vez habilitado el lcd.
        if (self.enable_lcd and self.key != key_erase):
            self.str_lcd =  self.str_lcd + self.key
            print(self.str_lcd)
                
            try:
                if (int(self.str_lcd) > lim_int):
                    self.str_lcd =  self.str_lcd[:-1]

                lcd_display[self.cont_num_lcd -1].display(int(self.str_lcd))
            except:
                print("No es un dato que corresponde a un número flotante.")
                self.str_lcd =  self.str_lcd[:-1]
                
        if (self.enable_lcd and self.key == key_erase):
            self.str_lcd =  self.str_lcd[:-1]
            if (self.str_lcd == ""):
                lcd_display[self.cont_num_lcd -1].display(0)
            else:
                lcd_display[self.cont_num_lcd -1].display(int(self.str_lcd))
            print(self.str_lcd)

        # definimos una tecla condicional para editar el lcd.
        if (event.key() == key_next):
            self.enable_lcd = True
                
            self.cont_num_lcd = self.cont_num_lcd + 1
            self.str_lcd = ""

            print(self.cont_num_lcd)
            if (self.cont_num_lcd > num_elem):
                self.cont_num_lcd = 0
                self.enable_lcd = False

        if (event.key() == key_finish):
            self.enable_lcd = False
            print("enter was pressed")
            self.result = []
            for i in range (num_elem):
                self.result.append(lcd_display[i].value())
            self.finish = True    

    # Introducir datos enteros y flotantes.
    def introdMixDatos(self,lcd_display_int, lcd_display_float,event,key_next,key_erase,key_finish,  val_max):
        num_elem_float = len(lcd_display_float)  # número de LCD a configurar.
        num_elem_int = len(lcd_display_int)
        self.finish_mix = False
        # una vez habilitado el lcd.
        
        if ((self.enable_lcd_float or self.enable_lcd_int) and self.key != key_erase):
            self.str_lcd =  self.str_lcd + self.key
            print(self.str_lcd)
            if (self.enable_lcd_float):    
                try:
                    lcd_display_float[self.cont_num_lcd -1].display(float(self.str_lcd))
                
                except:
                    print("No es un dato que corresponde a un número flotante.")
                    self.str_lcd =  self.str_lcd[:-1]
                
            if (self.enable_lcd_int):
                try:
                    lcd_display_int[self.cont_num_lcd -1].display(int(self.str_lcd))    
                except:
                    print("No es un dato que corresponde a un número flotante.")
                    self.str_lcd =  self.str_lcd[:-1]

        if (self.enable_lcd_int and int(self.str_lcd) > val_max and self.key != key_erase and self.key != key_finish):
            print("El valor ingresado es mayor que el límite.")
            self.str_lcd =  self.str_lcd[:-1]    
            lcd_display_int[self.cont_num_lcd -1].display(int(self.str_lcd)) 


        if ((self.enable_lcd_int or self.enable_lcd_float) and self.key == key_erase):
            self.str_lcd =  self.str_lcd[:-1]
            if (self.enable_lcd_float):
                if (self.str_lcd == ""):
                    lcd_display_float[self.cont_num_lcd -1].display(0)
                else:
                    lcd_display_float[self.cont_num_lcd -1].display(float(self.str_lcd))
                
            if (self.enable_lcd_int):
                if (self.str_lcd == ""):
                    lcd_display_int[self.cont_num_lcd -1].display(0)
                else:
                    lcd_display_int[self.cont_num_lcd -1].display(int(self.str_lcd))
            
            print(self.str_lcd)
        # definimos una tecla condicional para editar el lcd.
        if (event.key() == key_next):
            # parámetro inicial. 
            if (self.enable_lcd_int or self.enable_lcd_float != True):
                self.enable_lcd_int = True

            # habilitamos el valor entero.
            self.str_lcd = ""
            print("int: ".format(self.enable_lcd_int))
            print("float: ".format(self.enable_lcd_float))
            

            # condicional en caso de que se tenga todos los datos enteros.
            if (self.enable_lcd_int and self.cont_num_lcd >= num_elem_int):
                self.enable_lcd_int = False
                self.enable_lcd_float = True
                self.cont_num_lcd = 0
                self.str_lcd = ""
                

            if (self.enable_lcd_float and self.cont_num_lcd >= num_elem_float):
                self.cont_num_lcd = 0
                self.enable_lcd_float = False
                self.str_lcd = ""
                self.enable_lcd_int = True
            # habilitamos la suma de los elementos.
            self.cont_num_lcd = self.cont_num_lcd + 1    

        if (event.key() == key_finish):
            self.enable_lcd_int = False
            self.enable_lcd_float = False
            self.cont_num_lcd = 0
            print("enter was pressed")
            self.result = []
            self.result_int = []
            self.result_float = []
            for i in range (num_elem_int):
                self.result_int.append(lcd_display_int[i].value())

            for i in range (num_elem_float):
                self.result_float.append(lcd_display_float[i].value())
            
            self.result.append(self.result_int)
            self.result.append(self.result_float)
            self.finish_mix = True 

    # introducir datos flotantes sin singo.
    def introducirDatos(self,lcd_display,event,key_next,key_erase,key_finish):
        num_elem = len(lcd_display)  # número de LCD a configurar.
        self.finish = False
        # una vez habilitado el lcd.
        if (self.enable_lcd and self.key != key_erase):
            self.str_lcd =  self.str_lcd + self.key
            print(self.str_lcd)
                
            try:
                lcd_display[self.cont_num_lcd -1].display(float(self.str_lcd))
                self.pmp = float(self.str_lcd)
            except:
                print("No es un dato que corresponde a un número flotante.")
                self.str_lcd =  self.str_lcd[:-1]
                
        if (self.enable_lcd and self.key == key_erase):
            self.str_lcd =  self.str_lcd[:-1]
            if (self.str_lcd == ""):
                lcd_display[self.cont_num_lcd -1].display(0)
            else:
                lcd_display[self.cont_num_lcd -1].display(float(self.str_lcd))
            print(self.str_lcd)

        # definimos una tecla condicional para editar el lcd.
        if (event.key() == key_next):
            self.enable_lcd = True
            self.str_lcd = ""

            print(self.cont_num_lcd)
            if (self.cont_num_lcd >= num_elem):
                self.cont_num_lcd = 0
                self.enable_lcd = False
            
            self.cont_num_lcd = self.cont_num_lcd + 1

        if (event.key() == key_finish):
            self.enable_lcd = False
            print("enter was pressed")
            self.result = []
            for i in range (num_elem):
                self.result.append(lcd_display[i].value())
            self.finish = True    

# introducir datos flotantes sin singo.
    def introducirDatosSigno(self,lcd_display,lbl_sign,event,key_next,key_erase,key_finish, key_sign):
        num_elem = len(lcd_display)  # número de LCD a configurar.
        self.finish = False
        # una vez habilitado el lcd.
        if (self.enable_lcd and self.key != key_erase):
            self.str_lcd =  self.str_lcd + self.key
            print(self.str_lcd)
            # condición de signo.
            if (self.key == key_sign):
                if (lbl_sign[self.cont_num_lcd -1].text() == "-"):
                    lbl_sign[self.cont_num_lcd -1].setText("+")
                else:
                    lbl_sign[self.cont_num_lcd -1].setText("-")
            try:
                lcd_display[self.cont_num_lcd -1].display(float(self.str_lcd))
                self.pmp = float(self.str_lcd)
            except:
                print("No es un dato que corresponde a un número flotante.")
                self.str_lcd =  self.str_lcd[:-1]
                
        if (self.enable_lcd and self.key == key_erase):
            self.str_lcd =  self.str_lcd[:-1]
            if (self.str_lcd == ""):
                lcd_display[self.cont_num_lcd -1].display(0)
            else:
                lcd_display[self.cont_num_lcd -1].display(float(self.str_lcd))
            print(self.str_lcd)

        # definimos una tecla condicional para editar el lcd.
        if (event.key() == key_next):
            self.enable_lcd = True
            self.str_lcd = ""
            self.cont_num_lcd = self.cont_num_lcd + 1
            print(self.cont_num_lcd)
            if (self.cont_num_lcd > num_elem):
                self.cont_num_lcd = 0
                self.enable_lcd = False
            
            

        if (event.key() == key_finish):
            self.enable_lcd = False
            print("enter was pressed")
            self.result = []
            for i in range (num_elem):
                if (lbl_sign[i].text() == "-"):
                    self.result.append(-lcd_display[i].value())
                else:
                    self.result.append(lcd_display[i].value())
            self.finish = True 

    def seleccionarOpciones(self,check_box,event,key_finish):
        num_comp = len(check_box)
        self.finishCheck = False
        for i in range (1, num_comp +1):
            if (self.key == str(i)):
                if (check_box[i-1].isChecked()):
                    check_box[i-1].setChecked(False)
                else:
                    check_box[i-1].setChecked(True)

        if (event.key() == key_finish):
            self.result_check = []
            for i in range (num_comp):
                self.result_check.append(check_box[i-1].isChecked())
            self.finishCheck = True

    def seleccionarUnaOpcion(self,check_box,event,key_finish):
        num_comp = len(check_box)
        self.finishCheck = False
        for i in range (1, num_comp +1):
            if (self.key == str(i)):
                # Borramos todas las opciones.
                for x in check_box:
                    x.setChecked(False)
                # marcamos la opción correcta
                check_box[i-1].setChecked(True)
                
        if (event.key() == key_finish):
            self.result_prog = 0
            for i in range (num_comp):
                if (check_box[i].isChecked()):
                    self.result_prog = i + 1
            self.finishCheck = True

    def GoToinitialPage(self):
        self.pages.setCurrentIndex(0)

    def GoTohomePage(self):
        self.pages.insertWidget(1,self.screen1)
        self.pages.setCurrentIndex(1)
    
    def GoToShowDataPage(self):
        print("Ir a la pantalla 2")
        self.pages.insertWidget(2,self.screen2)
        self.pages.setCurrentIndex(2)
    
    def GoToConfigPage(self):
        self.pages.setCurrentIndex(3)
    
    def GoToEstData(self):
        # verificamos que la ventana se añadió anteriormente
        self.pages.insertWidget(4,self.screen21)
        self.pages.setCurrentIndex(4)

    def GoToEstData2(self):
        self.pages.insertWidget(5,self.screen22)
        self.pages.setCurrentIndex(5)
        
    def GoToTipoRiego(self):
        self.pages.insertWidget(6,self.screen31)
        self.pages.setCurrentIndex(6)
    
    def GoToRiegoIntel(self):
        self.pages.insertWidget(7,self.screen311)
        self.pages.setCurrentIndex(7)

    def GoToRiegoAuto(self):
        self.pages.insertWidget(8,self.screen312)
        self.pages.setCurrentIndex(8)

    def GoToRiegoManual(self):
        self.pages.insertWidget(9,self.screen313)
        self.pages.setCurrentIndex(9)

    def GoToNewSensor(self):
        self.pages.insertWidget(10,self.screen3111)
        self.pages.setCurrentIndex(10)

    def GoToGroundData(self):
        self.pages.insertWidget(11,self.screen3112)
        self.pages.setCurrentIndex(11)
    
    def GoToIrrigationTime(self):
        self.pages.insertWidget(12,self.screen3113)
        self.pages.setCurrentIndex(12)
    
    def GoToConfigProg(self):
        self.pages.insertWidget(13,self.screen3121)
        self.pages.setCurrentIndex(13)

    def goToSelectProg(self):
        self.pages.insertWidget(14,self.screen3122)
        self.pages.setCurrentIndex(14)
        
    def GoToNewVWC(self):
        self.pages.insertWidget(15,self.screen31111)
        self.pages.setCurrentIndex(15)
    
    def GoToNewTamb(self):
        self.pages.insertWidget(16,self.screen31112)
        self.pages.setCurrentIndex(16)

    def GoToNewHamb(self):
        self.pages.insertWidget(17,self.screen31113)
        self.pages.setCurrentIndex(17)

    def GoToProg(self):
        self.pages.insertWidget(18,self.screen31211)
        self.pages.setCurrentIndex(18)
    
    def GoToNameVWC(self):
        self.pages.insertWidget(19,self.screen311111)
        self.pages.setCurrentIndex(19)
    
    def GoToTypEqVWC(self):
        self.pages.insertWidget(20,self.screen311112)
        self.pages.setCurrentIndex(20)

    def GoToNameTa(self):
        self.pages.insertWidget(21,self.screen311121)
        self.pages.setCurrentIndex(21)

    def GoToLimTa(self):
        self.pages.insertWidget(22,self.screen311122)
        self.pages.setCurrentIndex(22)

    def GoToNameHa(self):
        self.pages.insertWidget(23,self.screen311131)
        self.pages.setCurrentIndex(23)

    def GoToLimHa(self):
        self.pages.insertWidget(24,self.screen311132)
        self.pages.setCurrentIndex(24)
    
    def GoToDay(self):
        self.pages.insertWidget(25,self.screen312111)
        self.pages.setCurrentIndex(25)
    
    def GoToStartHour(self):
        self.pages.insertWidget(26,self.screen312112)
        self.pages.setCurrentIndex(26)

    def GoToSetIrrigationTime(self):
        self.pages.insertWidget(27,self.screen312113)
        self.pages.setCurrentIndex(27)

    def GoToGrade1(self):
        self.pages.insertWidget(28,self.screen3111121)
        self.pages.setCurrentIndex(28)
    
    def GoToGrade2(self):
        self.pages.insertWidget(29,self.screen3111122)
        self.pages.setCurrentIndex(29)
    
    def GoToGrade3(self):
        self.pages.insertWidget(30,self.screen3111123)
        self.pages.setCurrentIndex(30)

    def GoToShowSensorData(self):
        self.pages.insertWidget(31,self.screen23)
        self.pages.setCurrentIndex(31)

    def GoToGroundData(self):
        print("Ir a la pantalla 32")
        self.pages.insertWidget(32,self.screen24)
        self.pages.setCurrentIndex(32)

class anuncio_00(QWidget):
    def __init__(self):
        super().__init__() 
        uic.loadUi("guide/wideget_00.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
    
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate)

class anuncio_01(QWidget):
    def __init__(self):
        super().__init__() 
        uic.loadUi("guide/wideget_01.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        self.modif_lbl_riego()
    
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate)
    
    def modif_lbl_riego(self):
        # obtenemos el tipo de riego.
        lbl_riego = [self.lbl_riego_est_1,self.lbl_riego_est_2,self.lbl_riego_est_3]
        self.tipo_riego_est = []
        for i in range(len( estaciones)):
            riego = estaciones[i].obtener_tipo_riego()
            self.tipo_riego_est.append(riego[0])
            if riego[0] == 0:
                lbl_riego[i].setText("Estación {0}: {1}".format(i+1,"Riego inteligente"))
                print("Estación{0}: {1}".format(i+1,"Riego inteligente"))
                lbl_riego[i].setStyleSheet('font: 22pt "Ubuntu"; color:rgb(249, 112, 112);')
                
            if riego[0] == 1:
                lbl_riego[i].setText("Estación {0}: {1}".format(i+1,"Riego programado"))
                print("Estación{0}: {1}".format(i+1,"Riego programado"))
                lbl_riego[i].setStyleSheet('font: 22pt "Ubuntu"; color:rgb(142, 249, 149);')
            if riego[0] == 2:
                lbl_riego[i].setText("Estación {0}: {1}".format(i+1,"Riego manual"))
                print("Estación{0}: {1}".format(i+1,"Riego manual"))
                lbl_riego[i].setStyleSheet('font: 22pt "Ubuntu"; color:rgb(194, 102, 255)')

################## Mostrar datos ##########################
class anuncio_02(QWidget):
    def __init__(self):
        super().__init__() 
        uic.loadUi("guide/wideget_02.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
    
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate)

# ---------------------------------------------- #
class anuncio_021(QWidget):
    def __init__(self,tipo_riego,num_est):
        self.tipo_riego = tipo_riego
        self.num_est = num_est

        super().__init__() 
        uic.loadUi("guide/wideget_021.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        self.modif_lbl(self.tipo_riego,self.num_est)
        
        #####################################################
        # Leer datos de tipo de riego, numero de programa y datos de tiempo
        # de riego y horas.
        #####################################################
    
    def modif_lbl(self,tipo_riego,num_est):
        self.num_est = num_est
        self.tipo_riego = tipo_riego
        self.lbl_num_est.setText("Estación " + str(self.num_est))

    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate)


# ---------------------------------------------- #
class anuncio_022(QWidget):
    def __init__(self,num_est):
        self.num_est = num_est
        super().__init__() 
        uic.loadUi("guide/wideget_022.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        self.modif_lbl(self.num_est)

    def modif_lbl(self,num_est):
        self.num_est = num_est    
        self.lbl_num_est.setText("Estación " + str(self.num_est))
        #####################################################
        # Leer datos de tipo de riego, numero de programa y datos de tiempo
        # de riego y horas.
        #####################################################
    
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate)

################## Configuracion ##########################
class anuncio_03(QWidget):
    def __init__(self):
        super().__init__() 
        uic.loadUi("guide/wideget_03.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
    
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate)

class anuncio_031(QWidget):
    def __init__(self,num_est):
        self.num_est = num_est
        super().__init__() 
        uic.loadUi("guide/wideget_031.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        self.modif_lbl(self.num_est)

    def modif_lbl(self,num_est):
        self.num_est = num_est
        self.lbl_num_est.setText("Estación " + str(self.num_est))
        
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate)

class anuncio_0311(QWidget):
    def __init__(self,num_est):
        self.num_est = num_est
        super().__init__() 
        uic.loadUi("guide/wideget_0311.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        self.modif_lbl(self.num_est)

    def modif_lbl(self,num_est):
        self.num_est = num_est
        self.lbl_num_est.setText("Estación " + str(self.num_est))
        
        
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate)

class anuncio_0312(QWidget):
    def __init__(self,num_est):
        self.num_est = num_est
        super().__init__() 
        uic.loadUi("guide/wideget_0312.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        self.modif_lbl(self.num_est)

    def modif_lbl(self,num_est):
        self.num_est = num_est
        self.lbl_num_est.setText("Estación " + str(self.num_est))
        
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate)

class anuncio_0313(QWidget):
    def __init__(self,num_est):
        self.num_est = num_est
        super().__init__() 
        uic.loadUi("guide/wideget_0313.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        self.modif_lbl(self.num_est)

    def modif_lbl(self,num_est):
        self.num_est = num_est
        self.lbl_num_est.setText("Estación " + str(self.num_est))

    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate)

class anuncio_03111(QWidget):
    def __init__(self,num_est):
        self.num_est = num_est
        super().__init__() 
        uic.loadUi("guide/wideget_03111.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        self.modif_lbl(self.num_est)

    def modif_lbl(self,num_est):
        self.num_est = num_est
        self.lbl_num_est.setText("Estación " + str(self.num_est))
        
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate)

class anuncio_03112(QWidget):
    def __init__(self,num_est):
        self.num_est = num_est
        super().__init__() 
        uic.loadUi("guide/wideget_03112.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        self.modif_lbl(self.num_est)

    def modif_lbl(self,num_est):
        self.num_est = num_est
        self.lbl_num_est.setText("Estación " + str(self.num_est))
        
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate)        

class anuncio_03113(QWidget):
    def __init__(self):
        
        super().__init__() 
        uic.loadUi("guide/wideget_03113.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        
        
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate)        

class anuncio_03121(QWidget):
    def __init__(self,num_est):
        self.num_est = num_est
        super().__init__() 
        uic.loadUi("guide/wideget_03121.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        self.modif_lbl(self.num_est)

    def modif_lbl(self,num_est):
        self.num_est = num_est
        self.lbl_num_est.setText("Estación " + str(self.num_est))
        
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate)   

class anuncio_03122(QWidget):
    def __init__(self,num_est):
        self.num_est = num_est
        super().__init__() 
        uic.loadUi("guide/wideget_03122.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        self.modif_lbl(self.num_est)

    def modif_lbl(self,num_est):
        self.num_est = num_est
        self.lbl_num_est.setText("Estación " + str(self.num_est))
        
        
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate)   

class anuncio_031111(QWidget):
    def __init__(self,num_est):
        self.num_est = num_est
        super().__init__() 
        uic.loadUi("guide/wideget_031111.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        self.modif_lbl(self.num_est)

    def modif_lbl(self,num_est):
        self.num_est = num_est
        self.lbl_num_est.setText("Estación " + str(self.num_est))
        
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate) 

class anuncio_031112(QWidget):
    def __init__(self,num_est):
        self.num_est = num_est
        super().__init__() 
        uic.loadUi("guide/wideget_031112.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        self.modif_lbl(self.num_est)

    def modif_lbl(self,num_est):
        self.num_est = num_est
        self.lbl_num_est.setText("Estación " + str(self.num_est))
        
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate) 

class anuncio_031113(QWidget):
    def __init__(self,num_est):
        self.num_est = num_est
        super().__init__() 
        uic.loadUi("guide/wideget_031113.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        self.modif_lbl(self.num_est)

    def modif_lbl(self,num_est):
        self.num_est = num_est
        self.lbl_num_est.setText("Estación " + str(self.num_est))
        
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate) 

class anuncio_031211(QWidget):
    def __init__(self,num_prog):
        self.num_prog = num_prog
        super().__init__() 
        uic.loadUi("guide/wideget_031211.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        self.modif_lbl(self.num_prog)

    def modif_lbl(self,num_prog):
        self.num_prog = num_prog
        self.lbl_num_prog.setText("Programa " + str(self.num_prog))
        
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate) 

class anuncio_0311111(QWidget):
    def __init__(self):
        super().__init__() 
        uic.loadUi("guide/wideget_0311111.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate) 


class anuncio_0311112(QWidget):
    def __init__(self):
        super().__init__() 
        uic.loadUi("guide/wideget_0311112.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate) 

class anuncio_03111121(QWidget):
    def __init__(self):
        super().__init__() 
        uic.loadUi("guide/wideget_03111121.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate) 

class anuncio_03111122(QWidget):
    def __init__(self):
        super().__init__() 
        uic.loadUi("guide/wideget_03111122.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate) 

class anuncio_03111123(QWidget):
    def __init__(self):
        super().__init__() 
        uic.loadUi("guide/wideget_03111123.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate) 

class anuncio_0311121(QWidget):
    def __init__(self):
        super().__init__() 
        uic.loadUi("guide/wideget_0311121.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate) 

class anuncio_0311122(QWidget):
    def __init__(self):
        super().__init__() 
        uic.loadUi("guide/wideget_0311122.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate) 

class anuncio_0311131(QWidget):
    def __init__(self):
        super().__init__() 
        uic.loadUi("guide/wideget_0311131.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate) 

class anuncio_0311132(QWidget):
    def __init__(self):
        super().__init__() 
        uic.loadUi("guide/wideget_0311132.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate) 

class anuncio_0312111(QWidget):
    def __init__(self):
        super().__init__() 
        uic.loadUi("guide/wideget_0312111.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate) 

class anuncio_0312112(QWidget):
    def __init__(self):
        super().__init__() 
        uic.loadUi("guide/wideget_0312112.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        # ocultar tods los widgets.
        self.widgets_hora = [self.widget_1, self.widget_2, self.widget_3, self.widget_4, self.widget_5, self.widget_6]
        for x in self.widgets_hora:
            x.hide()
        
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate) 

class anuncio_0312113(QWidget):
    def __init__(self):
        super().__init__() 
        uic.loadUi("guide/wideget_0312113.ui",self)
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate) 

class anuncio_023(QWidget):
    def __init__(self,tipo_riego,num_est,send_enable):
        super().__init__() 
        uic.loadUi("guide/wideget_023.ui",self)
        self.tipo_riego = tipo_riego
        self.num_est = num_est
        self.send_enable = send_enable
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime1)
        self.fecha.start(1000)
        self.modif_lbl(self.tipo_riego,self.num_est)
        
    def modif_lbl(self,tipo_riego,num_est):
        self.tipo_riego = tipo_riego
        self.num_est = num_est
        # Modificamos los labels de inicio.
        self.lbl_num_est.setText("Estación " + str(self.num_est))
        if (self.tipo_riego == 0):
            self.lbl_tipo_riego.setText("Riego inteligente")
        
        if (self.tipo_riego == 1):
            self.lbl_tipo_riego.setText("Riego automático")
        
        if (self.tipo_riego == 2):
            self.lbl_tipo_riego.setText("Riego manual")

        
    def displayTime1(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate) 
        # Actualizamos valores.
        if (self.send_enable):
            segundos = currentTime.second()
            minutos = currentTime.second()
            try:
                if (segundos % 5 == 0 and minutos != 0):
                    self.datos = estaciones[self.num_est -1].obtener_datos_sensores_rtd()
                    self.lbl_datos = [self.lbl_vwc_1,self.lbl_vwc_2,self.lbl_vwc_3,self.lbl_vwc_4,self.lbl_vwc_5,self.lbl_Ta_1,self.lbl_Ha_1]
                    for i in range (len(self.datos)):
                        self.lbl_datos[i].setText(str(self.datos[i]))
            except:
                print("No se pudo comunicar con el dispositivo")

class anuncio_024(QWidget):
    def __init__(self,tipo_riego,num_est,show_enable):
        super().__init__() 
        uic.loadUi("guide/wideget_024.ui",self)
        self.tipo_riego = tipo_riego
        self.num_est = num_est
        self.show_enable = show_enable
        self.fecha = QTimer(self)
        self.fecha.timeout.connect(self.displayTime)
        self.fecha.start(1000)
        # Actualizamos los valores del suelo
        self.actualizar_datos()
        self.modif_lbl(self.tipo_riego,self.num_est)
        
    def modif_lbl(self,tipo_riego,num_est):
        self.tipo_riego = tipo_riego
        self.num_est = num_est
        # Modificamos los labels de inicio.
        self.lbl_num_est.setText("Estación " + str(self.num_est))
        if (self.tipo_riego == 0):
            self.lbl_tipo_riego.setText("Riego inteligente")
        
        if (self.tipo_riego == 1):
            self.lbl_tipo_riego.setText("Riego automático")
        
        if (self.tipo_riego == 2):
            self.lbl_tipo_riego.setText("Riego manual")
        
        
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()

        displayTime=currentTime.toString('hh:mm:ss')
        displayDate=currentDate.toString('dd/MM/yyyy')
        # print(displayTime)
        self.lbl_hora.setText(displayTime)
        self.lbl_fecha.setText(displayDate) 
    
    def actualizar_datos(self):
        labels_datos = [self.lbl_cc,self.lbl_pmp,self.lbl_pr,self.lbl_ur,self.lbl_area,self.lbl_caudal]
        if (self.show_enable):
            try:
                self.datos_suelo = estaciones[self.num_est -1].obtener_datos_suelo()
                for i in range(len(self.datos_suelo)):
                    labels_datos[i].setText(str(self.datos_suelo[i]))
            except:
                pass

############### Programa principal ########################
if __name__ == '__main__':
    # Creamos una conexión con el microcontrolador.
    arduino1 = comunication_serial.Arduino("/dev/ttyACM0", 9600)
    estaciones = [arduino1]
    app = QApplication(sys.argv)
    win = main()
    win.show()
    
    try:
        sys.exit(app.exec_())
    except:
        print("killing")
        arduino1.cerrar_puerto()