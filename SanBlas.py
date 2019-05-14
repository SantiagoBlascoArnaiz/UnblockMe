# -*- coding:utf-8 -*-

#Blasco Arnaiz Santiago
#Aguado Labrador Patricia

import gtk
import sys
from gtk._gtk import RESPONSE_DELETE_EVENT

class Coches:
    def __init__(self):
        global intentos,nivel
        letraCoche = 65
        pintar = 0          #Pintar nos sirve para acceder a las posiciones de la lsita colores
        self.intentos = 0
        for _ in coches:
            orientacion = str((coches[chr(letraCoche)])[0]) #lee los datos de cada coche del diccionario coches
            x = int((coches[chr(letraCoche)])[1])
            y = int((coches[chr(letraCoche)])[2])
            longitud = str((coches[chr(letraCoche)])[3])
            
            '''Aprovechamos el grado de POO que tiene python para asignarle atributos a las event 
            boxes directamente en vez de crear objetos y asignarselos a estos'''
            
            car = gtk.EventBox()
            cars.append(car)
            car.show()
            color = colores[pintar] + orientacion + longitud + '.png' #la concatenacion de esos strings forma los nombres de las diferentes imagenes
            
            if nivel == 20 and color == 'rojoH2.png':#En el último nivel el coche rojo se convierte en el DeLorean de Back to the future!!
                color = 'delorean.png'
                
            car.letra = chr(letraCoche)                 
            car.orientacion = orientacion
            car.coordenadax = sizeRecuadro * x
            car.coordenaday = sizeRecuadro * y
            car.longitud = int(longitud)
            car.nuevax = 0
            car.nuevay = 0
            car.set_visible_window(False)

            
            img = gtk.Image()                       #Creamos y cargamos la iamgen del coche
            img.show()
            img.set_from_file('Images/' + color)
            car.add(img)
            
            tablero.put(car,sizeRecuadro * x,sizeRecuadro * y)  #Colocamos el coche en el tablero
            
            car.connect('button_press_event', self.EventoPulsar)            #conectamos sus diferentes funciones
            car.connect('button_release_event', self.EventoSoltar)
            car.connect('motion_notify_event', self.EventoArrastrar)
            
            car.arrastrando = False
            
            car.show()
            if pintar == 7:                     #Hace que sólo el coche que tiene que salir sea de color rojo,para poder diferenciarlo
                pintar=1
            else:
                pintar = pintar + 1
            
            letraCoche = letraCoche + 1
        
    def EventoPulsar(self, car, event,data = None):
        global intentos,mensajeIntentos,mensajeInfo
        intentos += 1
        if intentos ==1:
            mensajeIntentos.set_label('Llevas ' + str(intentos) + ' intento.')
        else:
            mensajeIntentos.set_label('Llevas ' + str(intentos) + ' intentos.')
        mensajeInfo.set_label("")
        car.arrastrando = True
        car.xInicial = int(event.x_root)
        car.yInicial = int(event.y_root)
        
        '''Establece los límites del coche que se está pulsando, primero determina si es vertical u horizontal y despues recorre la matriz 
        hueco desde la posicion del coche hacia los extremos,en cuanto encuentre un obstaculo,algo distinto de 0,se detiene y establece 
        en ese punto el limite de ese coche'''
        
        if car.orientacion == 'H':
            contador = 0
            while True:
                if hueco[int(car.coordenaday/sizeRecuadro) + 1][int(car.coordenadax/sizeRecuadro)-contador] != 0:
                    car.limiteIz = int(car.coordenadax/sizeRecuadro)-contador
                    break
                else:
                    contador += 1
            contador = 0
            while True:
                if hueco[int(car.coordenaday/sizeRecuadro) + 1][int(car.coordenadax/sizeRecuadro) + 1 + car.longitud + contador] != 0:
                    car.limiteDe = int(car.coordenadax/sizeRecuadro) + contador
                    break
                else:
                    contador += 1
        else:
            contador = 0
            while True:
                if hueco[int(car.coordenaday/sizeRecuadro)-contador][int(car.coordenadax/sizeRecuadro) + 1] != 0:
                    car.limiteAr = int(car.coordenaday/sizeRecuadro)-contador
                    break
                else:
                    contador += 1
            contador = 0
            while True:
                if hueco[int(car.coordenaday/sizeRecuadro) + 1 + car.longitud + contador][int(car.coordenadax/sizeRecuadro) + 1] != 0:
                    car.limiteAb = int(car.coordenaday/sizeRecuadro) + contador
                    break
                else:
                    contador += 1
        return gtk.TRUE
        
    
    def EventoArrastrar(self, car, event, data = None):

        if not car.arrastrando:
            return gtk.FALSE
        
        if car.orientacion == 'H':
            movimientox = int(event.x_root) - car.xInicial
            nuevax = car.coordenadax + movimientox
            nuevay = car.coordenaday
            
            if nuevax < car.limiteIz * sizeRecuadro:           #si el puntero se sale del tablero el coche permanece en la maxima posicion que puede alcanzar por ese lado
                nuevax = car.limiteIz * sizeRecuadro
            elif nuevax > car.limiteDe * sizeRecuadro:
                nuevax = car.limiteDe * sizeRecuadro
            else:
                nuevax = nuevax
                    
        else:
            
            movimientoy = int(event.y_root) -  car.yInicial
            nuevay = car.coordenaday + movimientoy
            nuevax = car.coordenadax
            
            if nuevay < car.limiteAr * sizeRecuadro:
                nuevay = car.limiteAr * sizeRecuadro
            elif nuevay > car.limiteAb * sizeRecuadro:
                nuevay = car.limiteAb * sizeRecuadro
            else:
                nuevay = nuevay
                
        tablero.move(car, nuevax, nuevay)     #Mueve el coche a su nueva posicon y almacena en el diccionario sus nuevos valores
        
        orientacion = str((coches[car.letra])[0])
        longitud = str((coches[car.letra])[3])
        
        coches[car.letra] = orientacion + str(int(nuevax/sizeRecuadro)) + str(int(nuevay/sizeRecuadro)) + longitud
        
        return gtk.TRUE
    
    def EventoSoltar(self, car, event, data = None):
        global maximoNivel,deshacer,intentos,tablero,cars,coches,tbox_level
        car.arrastrando = False
        
        if car.orientacion == 'H':
            movimientox = int(event.x_root) - car.xInicial
            nuevax = int((car.coordenadax + movimientox)/sizeRecuadro)
            nuevay = int(car.coordenaday/sizeRecuadro)
            
            if nuevax < car.limiteIz:           #si el puntero se sale del tablero el coche permanece en la maxima posicion que puede alcanzar por ese lado
                nuevax = car.limiteIz
            elif nuevax > car.limiteDe:
                nuevax = car.limiteDe
            else:
                nuevax = nuevax
                    
        else:
            
            movimientoy = int(event.y_root) -  car.yInicial
            nuevay = int((car.coordenaday + movimientoy)/sizeRecuadro)
            nuevax = int((car.coordenadax)/sizeRecuadro)
            
            if nuevay < car.limiteAr:
                nuevay = car.limiteAr
            elif nuevay > car.limiteAb:
                nuevay = car.limiteAb
            else:
                nuevay = nuevay
        
        car.coordenadax = nuevax * sizeRecuadro
        car.coordenaday = nuevay * sizeRecuadro
        
        tablero.move(car, car.coordenadax, car.coordenaday)
        
        actualizarPosiciones()
        
        imagen_reset = gtk.Image()      #Como ya ha empezado a jugar permite que se pueda pulsar el boton de reset de nivel
        imagen_reset.set_from_file("Images/reset.png")
        reset.set_image(imagen_reset)
        reset.set_sensitive(True)
        reset.connect_object("clicked",self.Reiniciar,car)
        
        
        if car.letra == 'A' and int(car.coordenadax/sizeRecuadro) == 5: #Condicion de victoria

            victoria = gtk.EventBox()       #Muestra una imagen felicitando al jugador
            victoria.modify_bg(gtk.STATE_NORMAL,victoria.get_colormap().alloc_color('white'))
            cars.append(victoria)
            win = gtk.Image()
            win.show()
            win.set_from_file('Images/win.gif')
            victoria.add(win)
            victoria.set_visible_window(False)
            tablero.put(victoria,0,0)
            victoria.show()
            mensajeIntentos.set_label('Lo has conseguido en ' + str(intentos) + ' movimientos')
            
            Records(intentos)       #Se actualizan los records y dependiendo de los niveles jugados habilita los botones correspondientes y uno mas
            records = open('records.txt', 'r')
            lista = records.readlines()
            maximoNivel = len(lista)
            records.close()
            
            for n in range(maximoNivel):
                botones[n].set_sensitive(True)
                botones[n].set_relief(gtk.RELIEF_NORMAL)
                if n == 19:
                    break
                
            tbox_level.set_text("1-" + str(maximoNivel))
                
        return gtk.TRUE
    
    def Reiniciar(self, car):
        global nivel,tablero,cars,coches,mensajeNivel,intentos,mensajeIntentos,reset,imagen_resetInicial,mensajeInfo
        
        reset.set_image(imagen_resetInicial)
        reset.set_sensitive(False)
        coches = {}
        guardarCoches(nivel)
        actualizarPosiciones()
        for car in cars:
            car.destroy()
        cars = []
        intentos = 0
        mensajeIntentos.set_label('')
        mensajeNivel.set_label("Nivel " + str(nivel))
        if nivel == 20:
            mensajeInfo.set_label("¡Ayuda a ese coche para que pueda regresar al futuro!")
        else:
            mensajeInfo.set_label("Saca el coche rojo por la derecha para ganar")
        Coches()
    
class Botones:
    def __init__(self):
        global sizeBorde,sizeRecuadro,totalNiveles,maximoNivel,tbox_level
        '''Existen 2 formatos diferentes de itnerfaz,dependiendo del total de niveles 
        a los que se pueda jugar se utiliza uno u otro.
        Podriamos poner directamente la interfaz para más de 20 niveles,pero nos gusta más con botones'''
        if totalNiveles > 20:
            tbox_level.set_text("1-" + str(maximoNivel))
            pantalla.put(tbox_level,5*sizeRecuadro + sizeBorde*3 ,6*sizeRecuadro + sizeBorde*3)
            tbox_level.set_size_request(sizeRecuadro,sizeBorde *2)
            
            escoge = gtk.Button()
            escoge.set_label('¡Jugar!')
            escoge.set_relief(gtk.RELIEF_NORMAL)
            escoge.set_size_request(sizeRecuadro,sizeBorde *3)
            escoge.connect("clicked",self.escogerNivel)
            pantalla.put(escoge,5*sizeRecuadro + sizeBorde*3 ,6*sizeRecuadro + sizeBorde*6)
            
            
        botx =int(sizeRecuadro/2)
        boty = int((sizeRecuadro*6)/10)
            
        x=0
        y=0
        for n in range (totalNiveles):   #Crea tantos botones como numero de niveles exista
            bot = gtk.Button()
            botones.append(bot)
            bot.set_label(str(n + 1))
            bot.numero = n      #Tratamos a los botones como bojetos y les asignamos un atributo numero
            bot.set_relief(gtk.RELIEF_NONE)
            bot.set_size_request(botx,boty)
            bot.set_sensitive(False)
            bot.connect("clicked",self.seleccionarNivel)
            pantalla.put(bot,x * botx,y * boty + sizeBorde*2)
            x+=1
            if x==2:
                x=0
                y+=1
            if n == 19:
                break
                    
        for n in range(maximoNivel):
            botones[n].set_sensitive(True)
            botones[n].set_relief(gtk.RELIEF_NORMAL)
            if n == 19:
                break
                
    def seleccionarNivel(self,bot):
        global nivel,tablero,cars,coches,mensajeNivel,mensajeInfo,intentos
        
        nivel = bot.numero + 1      #Resetea todos los contenedores de coches para no crear conflictos entre niveles
        coches = {}
        guardarCoches(nivel)
        actualizarPosiciones()
        for car in cars:
            car.destroy()
        cars = []
        intentos = 0
        mensajeIntentos.set_label('')
        if nivel == 20:
            mensajeInfo.set_label("¡Ayuda al DeLorean a salir de este atasco\npara que pueda volver de regreso al futuro!")
        else:
            mensajeInfo.set_label("Saca el coche rojo por la derecha para ganar")
        mensajeNivel.set_label("Nivel " + str(nivel))
        Coches()
        
    def escogerNivel(self,bot): #La funcion para escoger niveles cuando hay mas de 196
        global nivel,tablero,cars,coches,mensajeNivel,mensajeInfo,intentos,tbox_level,maximoNivel
        try:
            nivel = int(tbox_level.get_text())    #Resetea todos los contenedores de coches para no crear conflictos entre niveles
            if nivel >= 1 and nivel <= maximoNivel:
                coches = {}
                guardarCoches(nivel)
                actualizarPosiciones()
                for car in cars:
                    car.destroy()
                cars = []
                intentos = 0
                mensajeIntentos.set_label('')
                if nivel == 20:
                    mensajeInfo.set_label("¡Ayuda al DeLorean a salir de este atasco\npara que pueda volver de regreso al futuro!")
                else:
                    mensajeInfo.set_label("Saca el coche rojo por la derecha para ganar")
                mensajeNivel.set_label("Nivel " + str(nivel))
                Coches()
            else:
                tbox_level.set_text("No admitido")
        except:
            tbox_level.set_text("No admitido")

def guardarCoches (nivel):
    global totalNiveles
    letraMayus = 65
    niveles.seek(0)
    totalNiveles = int(niveles.readline())
    
    for _ in range(nivel - 1):
            indicaLineasSalto = int(niveles.readline())
            
            for linea in range(indicaLineasSalto):
                salto = niveles.readline()    #Pasa el puntero a la siguiente linea
    
    numeroCoches = int(niveles.readline())
    for datosCoche in range (numeroCoches):
        orientacion = niveles.read(1)
        x = int(niveles.read(1))
        y = int(niveles.read(1))
        longitud = int(niveles.read(1))
        
        if orientacion != 'H' and orientacion != 'V':
            sys.exit()
            
        elif  x < 1 or x > sizeTablero:
            sys.exit()
            
        elif  y < 1 or y > sizeTablero:
            sys.exit()
            
        elif longitud < 2 or longitud > 3:
            sys.exit()
        
        else:
            coches[chr(letraMayus)] = str(orientacion) + str(x - 1) + str(y - 1) + str(longitud)   #Guardamos la informacion de cada coche en el diccionario coches
            salto = niveles.readline()    #Pasa el puntero a la siguiente linea
            letraMayus = letraMayus + 1

def limpiartablero(tablero,tableroVacio):
    
    x = -1
    y = -1
    for fila in tablero:
            y += 1
            xt = x
            for caracter in fila:
                xt += 1
                caracter = tableroVacio[y][xt]
                tablero[y][xt] = caracter

def actualizarPosiciones():
    '''Refresca el tabero hueco con las nuevas posiciones de los coches almacenadas en el diccionario coches'''
    limpiartablero(hueco,huecoVacio);
    
    letraCoche = 65
    
    for coche in range (len(coches)):
        orientacion = str((coches[chr(letraCoche)])[0])
        x = int((coches[chr(letraCoche)])[1]) + 1
        y = int((coches[chr(letraCoche)])[2]) + 1
        longitud = int((coches[chr(letraCoche)])[3])
        
        if orientacion == 'H':                  
            for posicion in range(longitud):   
                hueco[y][x] = 1
                x += 1
                
        else:
            for posicion in range(longitud):
                hueco[y][x] = 1
                y += 1
                
        letraCoche += 1
        
def Records(movimientos):
    global nivel,mensajeInfo
    
    try:
        records = open('records.txt','r')
        listaRecords = records.readlines()
                
        if int(listaRecords[nivel-1]) > movimientos and int(listaRecords[nivel-1]) != 0:
            listaRecords[nivel-1] = str(movimientos) + '\n'
            records = open('records.txt','w')
                    
            for record in listaRecords:
                records.write(record)
                        
            mensajeInfo.set_label('¡Oh vaya, tenemos un nuevo record!')
            records.close()
                    
        elif int(listaRecords[nivel-1]) == 0:
                    
            if len(listaRecords) < totalNiveles:
                listaRecords[nivel-1]=str(movimientos) + '\n'
                records = open('records.txt','w')
                        
                for record in listaRecords:
                    records.write(record)
                records.write('0')
                mensajeInfo.set_label('¡Oh vaya, tenemos un nuevo record!')
                records.close()
                        
            else:
                listaRecords[nivel-1] = str(movimientos) + '\n'
                records = open('records.txt','w')
                for record in listaRecords:
                    records.write(record)
                mensajeInfo.set_label('¡Oh vaya, tenemos un nuevo record!')
                records.close()
                        
        else:
            mensajeInfo.set_label('El record actual es de ' + str(listaRecords[nivel - 1]))
                    
    except:
        mensajeInfo.set_label('¡Oh vaya, tenemos un nuevo record!')
        records = open('records.txt','w')
        records.write(str(movimientos) + '\n0')
        records.close()
        
def Salir(widget,data=None):
    global salida
    salida.show_all()
    return gtk.TRUE

def Seguir(widget,data=None):
    global salida
    salida.hide_all()
    
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
#############################################################################################################################

hueco = [[2,2,2,2,2,2,2,2],         #Matriz qeu almacenara las posiciones de los coches durante el juego
         [2,0,0,0,0,0,0,2],
         [2,0,0,0,0,0,0,2],
         [2,0,0,0,0,0,0,0,2],
         [2,0,0,0,0,0,0,2],
         [2,0,0,0,0,0,0,2],
         [2,0,0,0,0,0,0,2],
         [2,2,2,2,2,2,2,2]]

huecoVacio = [[2,2,2,2,2,2,2,2],        #Matriz utilizada para limpir la matriz hueco
              [2,0,0,0,0,0,0,2],
              [2,0,0,0,0,0,0,2],
              [2,0,0,0,0,0,0,0,2],
              [2,0,0,0,0,0,0,2],
              [2,0,0,0,0,0,0,2],
              [2,0,0,0,0,0,0,2],
              [2,2,2,2,2,2,2,2]]

try:
    records = open('records.txt', 'r')      #Si el fichero existe establece el maximo nivel en condicion de los niveles jugados
    lista = records.readlines()
    maximoNivel = len(lista)
        
    records.close()
        
except:
    maximoNivel = 1         #Si no existe quiere decir que no se ha jugado todavia y el maximo nivel es 1
    
try:
    niveles = open('niveles.txt', 'r')
except:
    sys.exit()

colores = ['rojo','red','yellow','white','blue','orange','green','purple',] #almacena strings para poder abrir los diferentes pngs para los coches

nivel = 1
totalNiveles = int(niveles.readline())
botones = []    #lista que contiene los botones,para asi pdoer habilitarlos/deshabilitarlos
cars = []       #contiene las event boxes de los coches para poder destruirlas
coches = {}     #Diccionarioq ue contiene informacion sobre los coches
intentos = 0

sizeRecuadro = 75
sizeBorde = 10
sizeTablero = 6
sizeVentana = sizeRecuadro * sizeTablero + 2 * sizeBorde + sizeRecuadro

ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
ventana.set_position(gtk.WIN_POS_CENTER)
ventana.set_title('Unlock Me!')
ventana.connect('delete_event', Salir)
ventana.set_border_width(sizeBorde)
ventana.modify_bg(gtk.STATE_NORMAL,ventana.get_colormap().alloc_color('#0061a8'))
ventana.set_resizable(False)
ventana.set_icon_from_file("Images/icon.png")

tbox_level = gtk.Entry()  # Textbox para escoger nivel

pantalla = gtk.Fixed()

borde = gtk.Fixed()
imagen_borde = gtk.Image()
imagen_borde.show()
imagen_borde.set_from_file('Images/borde.png')
borde.put(imagen_borde,0,0)
borde.set_size_request(sizeRecuadro*sizeTablero + 2*sizeBorde,sizeRecuadro*sizeTablero + 2*sizeBorde)
pantalla.put(borde,sizeRecuadro + sizeBorde,0)

tablero = gtk.Fixed()
tablero.set_size_request(sizeRecuadro*sizeTablero,sizeRecuadro*sizeTablero)
pantalla.put(tablero,sizeRecuadro + sizeBorde*2,sizeBorde)

mensajeNivel = gtk.Label("¡Bienvenido!")
mensajeNivel.set_style(mensajeNivel.get_style().copy())
pantalla.put(mensajeNivel,int(sizeRecuadro*3.3),sizeRecuadro*6 + sizeBorde*2)

mensajeIntentos = gtk.Label("")
mensajeIntentos.set_style(mensajeIntentos.get_style().copy())
pantalla.put(mensajeIntentos,int(sizeRecuadro + sizeBorde),sizeRecuadro*6 + sizeBorde*4)

mensajeInfo = gtk.Label("")
mensajeInfo.set_style(mensajeInfo.get_style().copy())
pantalla.put(mensajeInfo,int(sizeRecuadro + sizeBorde),sizeRecuadro*6 + sizeBorde*6)

etiquetaNivel = gtk.Label("Niveles")
etiquetaNivel.set_style(etiquetaNivel.get_style().copy())
pantalla.put(etiquetaNivel,sizeBorde,0)

salida = gtk.Window(gtk.WINDOW_TOPLEVEL)
salida.set_position(gtk.WIN_POS_CENTER)
salida.set_title('')
salida.set_size_request(300,150)
salida.set_resizable(False)
    
fondo = gtk.Fixed()
fondo.set_size_request(300,150)
    
seguro = gtk.Label("¿De verdad quieres salir?")
fondo.put(seguro,70,20)
    
no = gtk.Button()
no.set_label('No')
no.set_relief(gtk.RELIEF_NORMAL)
no.set_size_request(80,40)
no.connect("clicked",Seguir)
    
si = gtk.Button()
si.set_label('Sí')
si.set_relief(gtk.RELIEF_NORMAL)
si.set_size_request(80,40)
si.connect("clicked",gtk.main_quit)
    
fondo.put(si,50,60)
fondo.put(no,180,60)
salida.add(fondo)

reset = gtk.Button()
imagen_resetInicial = gtk.Image()
imagen_resetInicial.set_from_file("Images/backInicial.png")
reset.set_image(imagen_resetInicial)
reset.set_relief(gtk.RELIEF_NORMAL)
reset.set_size_request(sizeRecuadro,sizeRecuadro)
reset.set_sensitive(False)
pantalla.put(reset,0,6*sizeRecuadro + sizeBorde*3)

salir = gtk.Button()
imagen_salir = gtk.Image()
imagen_salir.set_from_file("Images/exit.png")
salir.set_image(imagen_salir)
salir.set_relief(gtk.RELIEF_NORMAL)
salir.set_size_request(sizeRecuadro,sizeRecuadro)
salir.set_sensitive(True)
pantalla.put(salir,6*sizeRecuadro + sizeBorde*3 ,6*sizeRecuadro + sizeBorde*3)
salir.connect("clicked",Salir)

ventana.add(pantalla)

Coches()
Botones()
ventana.show_all()
gtk.main()