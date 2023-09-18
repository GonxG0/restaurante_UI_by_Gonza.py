
import os
import pickle

def limpiar(): #=====================================================================================================================================
	os.system('cls' if os.name == "ce" or os.name == "nt" or os.name == "dos"  else 'clear')

def salir(): #=====================================================================================================================================
    exit()
    
def linea(): #=====================================================================================================================================
    print("="*120)

def crear_eleccion(*tupla,can = 1,tit = None): #=====================================================================================================================================
    eleccion = None
    opciones = []
    if can < 0:
        can = 0
    if can > 0:
        for opcion in tupla:
            opciones.append(opcion[0:can].upper())
    else:
        for opcion in range(len(tupla)):
            opciones.append(f"{opcion}")
    while not eleccion in opciones:
        limpiar()
        if tit != None:
            linea()
            print(tit.center(120))
        linea()
        for n, opcion in enumerate(tupla):
            print(f"[{opciones[n]}] {opcion.capitalize()}")
        linea()    
        eleccion = input("Elija una opcion: ").upper()
    return(opciones.index(eleccion))
        



class restaurante(): #=====================================================================================================================================
    
    def leer(self): #=====================================================================================================================================
        try:
            with open("Configuracion.pkl", "rb") as read_file:
                self.configuraciones = pickle.load(read_file)
        except FileNotFoundError as error_:
            self.configuraciones =  {}
    
    def grabar(self):  #=====================================================================================================================================
        with open("Configuracion.pkl","wb") as obj_pickle:
            pickle.dump(self.configuraciones, obj_pickle,-1)
    
    def crear_configuracion(self): #=====================================================================================================================================
        limpiar()
        linea()
        while not self.mesas.isnumeric():
            self.mesas = input("¿Cuantas mesas dispone el restaurante?: ")
        self.mesas = int(self.mesas)
        while not self.sillas.isnumeric():
            self.sillas = input("¿Cuantas sillas dispone el restaurante?: ")
        self.sillas = int(self.sillas)
        eleccion = -1
        distribucion = {}
        while not eleccion == 2:
            self.sillas_dis = self.sillas
            self.mesas_dis = self.mesas
            for value in distribucion.values():
                self.mesas_dis  -= value["mesas"]  * value["cantidad"]
                self.sillas_dis -= value["sillas"] * value["cantidad"]
            opciones =  (
                        "Modificar distribuciones",
                        "quitar distribuciones",
                        "Finalizar"
                        )
            eleccion = crear_eleccion(*opciones, tit = "¿Como se distribuiran las mesas y sillas el dia de hoy?")
            if eleccion == 0:
                limpiar()
                linea()
                print("Distribucion actual del restaurante".center(120))
                linea()
                print(f"Mesas restantes: {self.mesas_dis}".center(55)+f"Sillas restantes: {self.sillas_dis}".center(55))
                linea()
                cant = ["a","a","",""]
                for key,value in distribucion.items():
                    print(f"[{key}] -- Cantidad: {value['cantidad']} -- Mesas: {value['mesas']} -- Sillas: {value['sillas']}")
                linea()
                while not cant[0].isnumeric():
                    cant[0] = input("Inserte el numero de sillas que va a tener este tipo de distribucion: ")
                cant[0] = int(cant[0])
                while not cant[1].isnumeric():
                    cant[1] = input("Inserte el numero de mesas que va a tener este tipo de distribucion: ")
                cant[1] = int(cant[1])
                cant[2] = input("Inserte el nombre de la distribucion: ")
                while not cant[3].isnumeric():
                    cant[3] = input(f"Inserte la cantidad de distribuciones de tipo [{cant[2]}] que tendra el restaurante : ")
                cant[3] = int(cant[3])       
                if distribucion.get(cant[2],True):
                    distribucion[cant[2]] = {
                                            "sillas":   cant[0],
                                            "mesas":    cant[1],
                                            "cantidad": cant[3]
                                            }                     
            if eleccion == 1 and len(distribucion)>0:
                opciones = []
                for key in distribucion.keys():
                    opciones.append(key)
                eleccion = crear_eleccion(*opciones,tit = "Elija la distribucion a eliminar",can = 0)
                distribucion.pop(opciones[eleccion])
        opciones =  ("Si.", "No, solo por hoy.")
        eleccion = crear_eleccion(*opciones,tit = "¿Desea guardar esta configuracion?")
        if eleccion == 0:
            linea()
            self.nombre = input("Inserte el nombre de dicha configuracion: ")
            self.configuraciones[self.nombre] = {
                                            "sillas" : self.sillas,
                                            "mesas" : self.mesas,
                                            "distribucion" : distribucion
                                            }
            self.grabar()
    
    def __init__(self): #=====================================================================================================================================
        
        ancho = 120

        self.leer()
        self.mesas = "a"
        self.sillas = "a"
        e = None
        opciones =  ("No","Si")
        conf = crear_eleccion(*opciones,tit = "¿Quiere cargar una configuracion?")
        limpiar()
        linea()
        if conf == 1:
            ops = []
            for a in self.configuraciones.keys():
                ops.append(a)
            if len(opciones) == 0:
                conf = 0
                print("No se encontro ninguna configuracion, ¡Vamos a crear una!")
                linea()
                input("\n Enter para continuar")
            else:
                e = crear_eleccion(*ops,tit = "¿Elija una configuracion para utilizar?", can = 0)
        if conf == 0:
            self.crear_configuracion()
        if e == None:
            self.configuracion  = self.configuraciones[self.nombre]
        else:
            self.configuracion = self.configuraciones[ops[e]]
            
        """==============================================================================================="""
        
        self.obj_mesa = []
        for key, dis in self.configuracion['distribucion'].items():
            for a in range(dis["cantidad"]):
                m = dis["mesas"]
                s = dis["sillas"]
                n = key
                self.obj_mesa.append(mesa(n,m,s))
        linea()
        self.menu_principal()
        
    def menu_principal(self):#=====================================================================================================================================
        
        while True:
            
            eleccion = ""
            opciones =  (
                        "Ver estados",
                        "Distribucion",
                        "Historial de pedidos",
                        "Salir"
                        )
            
            limpiar()
            eleccion = crear_eleccion(*opciones, tit= "Menu principal")
            
            if eleccion == 3:
                
                salir()
            
            elif eleccion == 0:
                
                while not eleccion == 3:
                
                    eleccion = ""
                    opciones =  (
                                "Pedidos actuales",
                                "Situacion de las mesas",
                                "Estados de los mozos",
                                "Volver"
                                )
                                
                    limpiar()
                    eleccion = crear_eleccion(*opciones, tit= "Elija el estado que desee ver")
                    
                    if eleccion == 1:
                        
                        limpiar()
                        linea()
                        print(f"Estado".center(15)+f"Tipo".center(15)+f"Sector".center(15)+f"Mozo".center(15)+f"Tiempo ocupada".center(15)+f"Codigo de pedido".center(35))
                        linea()
                        for a in self.obj_mesa:
                            print(a)
                        
                        linea()
                        input("   Enter para continuar ")    
                    
class mesa(): #=====================================================================================================================================
    
    def __init__(self,n,m,s): #=====================================================================================================================================
        self.mesas = m
        self.sillas = s
        self.nombre = n
        self.estado = "Libre"
        self.sector = "Principal"
        self.mozo = mozo()
        self.pedido = pedido()
        self.tiempo_ocupada = "00:00:00"
    
    def __str__(self): #=====================================================================================================================================
        return (f"{self.estado}".center(15)+f"{self.nombre}".center(15)+f"{self.sector}".center(15)+f"{self.mozo}".center(15)+f"{self.tiempo_ocupada}".center(15)+f"{self.pedido}".center(35,))
        
    def genearar_ticket(self): #=====================================================================================================================================
        
        pass
        

class pedido(): #=====================================================================================================================================
    
    def __init__(self): #=====================================================================================================================================
        pass
    
    def __str__(self): #=====================================================================================================================================
        return (f"Soy un pedido ._.")

class mozo(): #=====================================================================================================================================
    
    def __init__(self): #=====================================================================================================================================
        pass
    
    def __str__(self): #=====================================================================================================================================
        return (f"Soy un mozo :D")
    
    
    
    
                    
# ~ print(dir(dict))
# ~ pausa() 

todo = restaurante()




# 18:00 - 19:00 04/06/2022 135
# 10:40 - 11:00 07/06/2022 155
# 03:00 - 04:15 09/06/2022 195
# 00:00 - 00:00 00/00/0000 000
# 00:00 - 00:00 00/00/0000 000
# 00:00 - 00:00 00/00/0000 000
