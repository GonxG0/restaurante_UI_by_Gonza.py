
from tkinter import *
from tkinter import ttk

import tkinter as tk
from PIL import ImageTk, Image
import math

import functools

import os
import pickle


def salir(): #=====================================================================================================================================
    exit()



class ventana_configuracion(): # Ventana donde se crean las configuraciones

    def leer(self): # Se leen o crean las configuraciones
        try:
            with open("Configuracion.pkl", "rb") as read_file:
                self.configuraciones = pickle.load(read_file)
        except FileNotFoundError as error_:
            self.configuraciones =  {}
    
    def grabar(self):  # Se guarda la configuracion que se esta creando
        with open("Configuracion.pkl","wb") as obj_pickle:
            pickle.dump(self.configuraciones, obj_pickle,-1)
    
    def balance(self,dato): # Se cambia la cantidad de mesas y sillas totales y actuales de la configuracion
        print(dato)
        if dato[1] == True:
            self.mesas += int(dato[0])
        else:
            self.sillas += int(dato[0])
        
        if self.sillas < 0:
            self.sillas = 0
            
        if self.mesas < 0:
            self.mesas = 0
            
        self.tks["labels"]["n_mesas"].config(text=f"{self.mesas}")
        self.tks["labels"]["n_sillas"].config(text=f"{self.sillas}")
        self.actualizar()
        
    def config(self,dato): # Se suma o resta, sillas, mesas o cantidades de la distribucion seleccionada self.distribucion[distribucion][silla, mesa o cantidad]
        
        self.distribucion[dato[2]][dato[1]] += int(dato[0])
        
        if self.distribucion[dato[2]][dato[1]] < 0:
            
            self.distribucion[dato[2]][dato[1]] = 0
        
        self.tks["labels"][f"{dato[2]}{dato[1]}"].config(text= f"{self.distribucion[dato[2]][dato[1]]}")
        self.actualizar()
        
    def borrar(self,dato): # Se encarga de borrar la distribucion seleccionada y mueve todas las demas de ser necesario, sin afectar al rendimiento
        
        self.distribucion.pop(dato) # elimina la distribucion del registro
        
        tupla = (
                ("botones","silla-"),   ("botones","silla+"),   ("labels","silla"),
                ("botones","mesa-"),    ("botones","mesa+"),    ("labels","mesa"),
                ("botones","cantidad-"),("botones","cantidad+"),("labels","cantidad"),
                ("botones","borrar"),   ("cajas","nombre")
                )
        
        for palabra in tupla: # olvida y destruye todos los botones, etiquetas y cajas de las distribuciones
            
            self.tks[palabra[0]][f"{dato}{palabra[1]}"].place_forget()
            self.tks[palabra[0]][f"{dato}{palabra[1]}"].destroy()
        
        a = 0
        
        for n in range(len(self.distribucion)+1): # Vuelve a dibujar todos los botones, etiquetas y cajas a excepcion del que se borro
            
            if n != dato:
                
                self.distribucion[n+a]["nombre"] = self.tks[palabra[0]][f"{n}nombre"].get().capitalize()
                
                for palabra in tupla:
                    
                    self.tks[palabra[0]][f"{n}{palabra[1]}"].place_forget()
                    self.tks[palabra[0]][f"{n}{palabra[1]}"].destroy()
                    
                self.crear_distribucion(
                                        self.distribucion[n+a]["mesa"],
                                        self.distribucion[n+a]["silla"],
                                        self.distribucion[n+a]["cantidad"],
                                        self.distribucion[n+a]["nombre"],
                                        n+a
                                        )
            else:
                
                a = -1
                
        if len(self.distribucion) == 0: # Se deablaza el boton de nueva_configuracion
            self.tks["botones"]["nueva_configuracion"].place_forget()
            self.tks["botones"]["nueva_configuracion"].place(x = self.des,y=self.grosor*2.5+ self.des*6+(self.grosor+self.des)*(n), width= self.grosor*12+self.des*3, height = self.grosor)
        
    def actualizar(self): # actualiza los datos de todas las labels, con colores y similares
        total_sillas = self.sillas
        total_mesas = self.mesas
        
        for num in range(len(self.distribucion)):
            self.distribucion[num]["nombre"] = self.tks["cajas"][f"{num}nombre"].get()
        
        for a in self.distribucion:
            
            total_sillas -= a["silla"]*a["cantidad"]
            total_mesas -= a["mesa"]*a["cantidad"]
        
        if total_sillas > 0:
            c_sillas = "green3"
        elif total_sillas < 0:
            c_sillas = "red3"
        else:
            c_sillas = "yellow3"
        
        if total_mesas > 0:
            c_mesas = "green3"
        elif total_mesas < 0:
            c_mesas = "red3"
        else:
            c_mesas = "yellow3"
        
        self.tks["labels"]["s_mesas"].config(text= f"{total_mesas}",bg = "antiquewhite2" ,activebackground= "antiquewhite2",fg=c_mesas)
        self.tks["labels"]["s_sillas"].config(text= f"{total_sillas}",bg = "antiquewhite2" ,activebackground= "antiquewhite2",fg=c_sillas)
        self.tks["labels"]["s_distribuciones"].config(text= f"{len(self.distribucion)}")
        
        problema = "Todo va bien, sigamos asi"
        color = "green3"
        if total_sillas < 0:
            problema = "Faltan sillas o sobran distribuciones"
            color = "red3"
        elif total_mesas < 0:
            problema = "Faltan mesas o sobran distribuciones"
            color = "red3"
        
        if self.tks["cajas"]["nombre_configuracion"].get().capitalize() in self.configuraciones.keys():
            
            problema = "Ya existe una configuracion con ese nombre"
            color = "red3"
            
        for n in self.distribucion:
            
            if n["nombre"] == "":
                
                problema = "Hay una distribucion que no tiene nombre"
                color = "red3"
            
        if len(self.distribucion) == 0:
            
            problema = "No hay distribuciones, crea una"
            color = "red3"
            
        if self.tks["cajas"]["nombre_configuracion"].get().capitalize() == "":
            
            problema = "La configuracion no tiene nombre\n agregale uno"
            color = "red3"
        
        self.tks["labels"]["feedback"].config(text= problema, bg= color,font=("Courier", 13))
    
    def guardar(self): # Guarda las distribuciones en una configuracion con nombre y con un formato especifico a su vez que se destruye la ventana actual, solo permitiendo distribuciones validas
        error = False
        
        for n in self.distribucion:
            
            if n["nombre"] == "":
                error = True
        
        if self.tks["cajas"]["nombre_configuracion"].get().capitalize() in self.configuraciones.keys() or self.tks["cajas"]["nombre_configuracion"].get().capitalize() == "":
             
            error = True
            
        for num in range(len(self.distribucion)):
            self.distribucion[num]["nombre"] = self.tks["cajas"][f"{num}nombre"].get().capitalize()
            
        if len(self.distribucion) == 0:
        
            error = True
        
        if error == False:
            
            self.configuraciones[self.tks["cajas"]["nombre_configuracion"].get().capitalize()] =    {
                                                                                                    "sillas" : self.sillas,
                                                                                                    "mesas" : self.mesas,
                                                                                                    "distribucion" : self.distribucion
                                                                                                    }
            print(self.configuraciones)
            self.grabar()
            self.ventana.destroy() 
            
    
    def __init__(self,sillas = 0, mesas = 0): # Se crea la ventana con todos los botones, etiquetas y cajas
        
        self.leer()
        
        self.sillas = sillas
        self.mesas = mesas
        
        
        ancho = 1205
        alto = 540
        self.des = 5
        self.grosor = 50
        
        self.tks = 	{
                    "botones" : {},
                    "labels" :	{}, 
                    "cajas" :	{}
                    }
        
        self.ventana = Tk()
        self.ventana.title("Crear configuracion")
        self.ventana.config(bg = "gray")
        self.ventana.geometry(f"{ancho}x{alto}")
        
        self.distribucion = []
            
        
        self.tks["labels"]["mesas"] = tk.Label(text= "Mesas",bg = "antiquewhite2" ,activebackground= "antiquewhite2")
        self.tks["labels"]["mesas"].place(x = self.des,y= self.des, width= self.grosor * 3, height = self.grosor)
        self.tks["labels"]["sillas"] = tk.Label(text= "Sillas",bg = "antiquewhite2" ,activebackground= "antiquewhite2")
        self.tks["labels"]["sillas"].place(x = self.des,y= self.des*2+self.grosor, width= self.grosor * 3, height = self.grosor)
        
        self.tks["labels"]["n_mesas"] = tk.Label(text= f"{self.mesas}",bg = "antiquewhite2" ,activebackground= "antiquewhite2")
        self.tks["labels"]["n_mesas"].place(x = self.des*2+self.grosor*3,y= self.des, width= self.grosor, height = self.grosor)
        self.tks["labels"]["n_sillas"] = tk.Label(text= f"{self.sillas}",bg = "antiquewhite2" ,activebackground= "antiquewhite2")
        self.tks["labels"]["n_sillas"].place(x = self.des*2+self.grosor*3,y= self.des*2+self.grosor, width= self.grosor, height = self.grosor)
        
        tupla = (1,10,50,100)
        
        for c,n in enumerate(tupla): # creacion de botones de suma y resta de mesas

            self.tks["botones"]["m+"+str(n)] = tk.Button(text="+"+str(n),command = functools.partial(self.balance,(f"+{n}",True)))
            self.tks["botones"]["m+"+str(n)].config(bg = "antiquewhite2", fg = "black", activebackground = "antiquewhite2",activeforeground = "black")
            self.tks["botones"]["m+"+str(n)].place(x=self.des*3+self.grosor*4+c*(self.grosor+self.des),y=self.des, width=self.grosor, height= (self.grosor))

            self.tks["botones"]["m-"+str(n)] = tk.Button(text="-"+str(n),command = functools.partial(self.balance,(f"-{n}",True)))
            self.tks["botones"]["m-"+str(n)].config(bg = "antiquewhite2", fg = "black", activebackground = "antiquewhite2",activeforeground = "black")
            self.tks["botones"]["m-"+str(n)].place(x=self.des*3+self.grosor*4+c*(self.grosor+self.des)+len(tupla)*(self.grosor+self.des),y=self.des, width=self.grosor, height= (self.grosor))
            
            self.tks["botones"]["s+"+str(n)] = tk.Button(text="+"+str(n),command = functools.partial(self.balance,(f"+{n}",False)))
            self.tks["botones"]["s+"+str(n)].config(bg = "antiquewhite2", fg = "black", activebackground = "antiquewhite2",activeforeground = "black")
            self.tks["botones"]["s+"+str(n)].place(x=self.des*3+self.grosor*4+c*(self.grosor+self.des),y=self.des*2+self.grosor, width=self.grosor, height= (self.grosor))

            self.tks["botones"]["s-"+str(n)] = tk.Button(text="-"+str(n),command = functools.partial(self.balance,(f"-{n}",False)))
            self.tks["botones"]["s-"+str(n)].config(bg = "antiquewhite2", fg = "black", activebackground = "antiquewhite2",activeforeground = "black")
            self.tks["botones"]["s-"+str(n)].place(x=self.des*3+self.grosor*4+c*(self.grosor+self.des)+len(tupla)*(self.grosor+self.des),y=self.des*2+self.grosor, width=self.grosor, height= (self.grosor))
            
            # Se crea la primer distribucion
            self.tks["labels"]["D_nombre"] = tk.Label(text= "Nombre", bg = "antiquewhite2" ,activebackground= "antiquewhite2")
            self.tks["labels"]["D_nombre"].place(x = self.des,y= self.des*4+self.grosor*2+self.des, width= self.grosor*3, height = self.grosor/2)
            
            self.tks["labels"]["D_mesas"] = tk.Label(text= "Mesas", bg = "antiquewhite2" ,activebackground= "antiquewhite2")
            self.tks["labels"]["D_mesas"].place(x = self.des*2+self.grosor*3,y= self.des*4+self.grosor*2+self.des, width= self.grosor*3, height = self.grosor/2)
            
            self.tks["labels"]["D_sillas"] = tk.Label(text= "Sillas", bg = "antiquewhite2" ,activebackground= "antiquewhite2")
            self.tks["labels"]["D_sillas"].place(x = self.des*3+self.grosor*6,y= self.des*4+self.grosor*2+self.des, width= self.grosor*3, height = self.grosor/2)
            
            self.tks["labels"]["D_cantidad"] = tk.Label(text= "Cantidad", bg = "antiquewhite2" ,activebackground= "antiquewhite2")
            self.tks["labels"]["D_cantidad"].place(x = self.des*4+self.grosor*9,y= self.des*4+self.grosor*2+self.des, width= self.grosor*3, height = self.grosor/2)
        

        # Se crean las lineas negras para que la ui quede mas bonita
        self.tks["labels"]["linea1"] = tk.Label(bg = "black" ,activebackground= "black")
        self.tks["labels"]["linea1"].place(x = 0,y= self.des*3+self.grosor*2, width= ancho, height = self.des)
        
        self.tks["labels"]["linea2"] = tk.Label(bg = "black" ,activebackground= "black")
        self.tks["labels"]["linea2"].place(x = (self.grosor+self.des)*13+self.des*3,y= 0, width= self.des, height = alto)
        
        self.tks["labels"]["linea3"] = tk.Label(bg = "black" ,activebackground= "black")
        self.tks["labels"]["linea3"].place(x = (self.grosor+self.des)*13+self.des*4,y= self.grosor*3.5+ self.des*7, width= ancho-(self.grosor+self.des)*13-self.des*4, height = self.des)
        
        self.tks["labels"]["linea4"] = tk.Label(bg = "black" ,activebackground= "black")
        self.tks["labels"]["linea4"].place(x = (self.grosor+self.des)*13+self.des*4,y= self.grosor*5.5+ self.des*11, width= ancho-(self.grosor+self.des)*13-self.des*4, height = self.des)
        
        # Se crean la etiqueta de errores y las etiquetas de sillas, mesas y distribuciones actuales

        self.tks["labels"]["feedback"] = tk.Label(bg = "antiquewhite2" ,activebackground= "antiquewhite2")
        self.tks["labels"]["feedback"].place(x = (self.grosor+self.des)*13+self.des*5,y= self.des, width= (self.des+self.grosor)*8+self.des*4, height = (self.des+self.grosor)*2-self.des*1)
        
        self.tks["labels"]["S_mesas"] = tk.Label(text= "Mesas sobrantes", bg = "antiquewhite2" ,activebackground= "antiquewhite2")
        self.tks["labels"]["S_mesas"].place(x = self.des*8+self.grosor*14,y= self.des*4+self.grosor*2+self.des, width= self.grosor*3, height = self.grosor/2)

        self.tks["labels"]["S_sillas"] = tk.Label(text= "Sillas sobrantes", bg = "antiquewhite2" ,activebackground= "antiquewhite2")
        self.tks["labels"]["S_sillas"].place(x = self.des*9+self.grosor*17,y= self.des*4+self.grosor*2+self.des, width= self.grosor*3, height = self.grosor/2)
        
        self.tks["labels"]["S_distribuciones"] = tk.Label(text= "Total de distribuciones", bg = "antiquewhite2" ,activebackground= "antiquewhite2")
        self.tks["labels"]["S_distribuciones"].place(x = self.des*10+self.grosor*20,y= self.des*4+self.grosor*2+self.des, width= self.grosor*3, height = self.grosor/2)
        
        
        self.tks["labels"]["s_mesas"] = tk.Label(text= f"{self.mesas}",bg = "antiquewhite2" ,activebackground= "antiquewhite2")
        self.tks["labels"]["s_mesas"].place(x = self.des*8+self.grosor*14,y= self.grosor*2.5+ self.des*6, width= self.grosor*3, height = self.grosor)
        
        self.tks["labels"]["s_sillas"] = tk.Label(text= f"{self.sillas}",bg = "antiquewhite2" ,activebackground= "antiquewhite2")
        self.tks["labels"]["s_sillas"].place(x = self.des*9+self.grosor*17,y= self.grosor*2.5+ self.des*6, width= self.grosor*3, height = self.grosor)
        
        self.tks["labels"]["s_distribuciones"] = tk.Label(text= f"{len(self.distribucion)}",bg = "antiquewhite2" ,activebackground= "antiquewhite2")
        self.tks["labels"]["s_distribuciones"].place(x = self.des*10+self.grosor*20,y= self.grosor*2.5+ self.des*6, width= self.grosor*3, height = self.grosor)
        
        # etiqueta y caja para poner nombre el nombre de la configuracion
        
        self.tks["labels"]["nombre_configuracion"] = tk.Label(text= f"Nombre de la configuracion",bg = "antiquewhite2" ,activebackground= "antiquewhite2")
        self.tks["labels"]["nombre_configuracion"].place(x = (self.grosor+self.des)*13+self.des*5,y= self.grosor*3.5+ self.des*9, width= self.grosor*9+self.des*2, height = self.grosor)

        self.tks["cajas"]["nombre_configuracion"] = tk.Entry(bg = "antiquewhite2",	justify="center") 
        self.tks["cajas"]["nombre_configuracion"].place(x = (self.grosor+self.des)*13+self.des*5,y=self.grosor*4.5+ self.des*10, width= self.grosor*9+self.des*2, height = self.grosor)

        # Se crea el primer boton de nueva distribucion

        self.tks["botones"]["nueva_configuracion"] = tk.Button(text="Nueva distribucion",command = self.crear_distribucion)
        self.tks["botones"]["nueva_configuracion"].config(bg = "antiquewhite2", fg = "black", activebackground = "antiquewhite2",activeforeground = "black")
        self.tks["botones"]["nueva_configuracion"].place(x = self.des,y=self.grosor*2.5+ self.des*6+(self.grosor+self.des)*len(self.distribucion), width= self.grosor*12+self.des*3, height = self.grosor)
        
        # boton para guardar la configuracion

        self.tks["botones"]["guardar"] = tk.Button(text="Guardar nueva configuracion",command = self.guardar)
        self.tks["botones"]["guardar"].config(bg = "antiquewhite2", fg = "black", activebackground = "antiquewhite2",activeforeground = "black")
        self.tks["botones"]["guardar"].place(x = (self.grosor+self.des)*13+self.des*5,y=self.grosor*5.5+ self.des*13, width= self.grosor*9+self.des*2, height = self.grosor*3+self.des*9)
        
        
        self.actualizar()
        self.ventana.mainloop()
        
    def crear_distribucion(self,mesa=0,silla=0,cantidad=0,nombre="", numero = None): # se encarga de crear una fila nueva de configuracion
        if len(self.distribucion) == 7:
            return
        if numero == None:
            numero = len(self.distribucion)
            self.distribucion.append({"mesa":mesa,"silla":silla,"cantidad":cantidad,"nombre":nombre})
        else:
            self.distribucion[numero] = {"mesa":mesa,"silla":silla,"cantidad":cantidad,"nombre":nombre}
            
            
            
        self.tks["cajas"][f"{numero}nombre"] = tk.Entry(bg = "antiquewhite2",justify="center") 
        self.tks["cajas"][f"{numero}nombre"].place(x = self.des,y=self.grosor*2.5+ self.des*6+(self.grosor+self.des)*numero, width= self.grosor*3, height = self.grosor)
        self.tks["cajas"][f"{numero}nombre"].insert(0, nombre)
        "=============================================================================================================================================================================="
        self.tks["botones"][f"{numero}mesa-"] = tk.Button(text="-",command = functools.partial(self.config,(f"-{1}","mesa",numero)))
        self.tks["botones"][f"{numero}mesa-"].config(bg = "antiquewhite2", fg = "black", activebackground = "antiquewhite2",activeforeground = "black")
        self.tks["botones"][f"{numero}mesa-"].place(x = self.des*2+self.grosor*3,y=self.grosor*2.5+ self.des*6+(self.grosor+self.des)*numero, width= self.grosor, height = self.grosor)
        
        self.tks["labels"][f"{numero}mesa"] = tk.Label(text= mesa, bg = "antiquewhite2" ,activebackground= "antiquewhite2")
        self.tks["labels"][f"{numero}mesa"].place(x = self.des*2+self.grosor*4,y=self.grosor*2.5+ self.des*6+(self.grosor+self.des)*numero, width= self.grosor, height = self.grosor)
        
        self.tks["botones"][f"{numero}mesa+"] = tk.Button(text="+",command = functools.partial(self.config,(f"+{1}","mesa",numero)))
        self.tks["botones"][f"{numero}mesa+"].config(bg = "antiquewhite2", fg = "black", activebackground = "antiquewhite2",activeforeground = "black")
        self.tks["botones"][f"{numero}mesa+"].place(x = self.des*2+self.grosor*5,y=self.grosor*2.5+ self.des*6+(self.grosor+self.des)*numero, width= self.grosor, height = self.grosor)
        "=============================================================================================================================================================================="
        self.tks["botones"][f"{numero}silla-"] = tk.Button(text="-",command = functools.partial(self.config,(f"-{1}","silla",numero)))
        self.tks["botones"][f"{numero}silla-"].config(bg = "antiquewhite2", fg = "black", activebackground = "antiquewhite2",activeforeground = "black")
        self.tks["botones"][f"{numero}silla-"].place(x = self.des+self.grosor*3+self.des*2+self.grosor*3,y=self.grosor*2.5+ self.des*6+(self.grosor+self.des)*numero, width= self.grosor, height = self.grosor)
        
        self.tks["labels"][f"{numero}silla"] = tk.Label(text= silla, bg = "antiquewhite2" ,activebackground= "antiquewhite2")
        self.tks["labels"][f"{numero}silla"].place(x = self.des+self.grosor*4+self.des*2+self.grosor*3,y=self.grosor*2.5+ self.des*6+(self.grosor+self.des)*numero, width= self.grosor, height = self.grosor)
        
        self.tks["botones"][f"{numero}silla+"] = tk.Button(text="+",command = functools.partial(self.config,(f"+{1}","silla",numero)))
        self.tks["botones"][f"{numero}silla+"].config(bg = "antiquewhite2", fg = "black", activebackground = "antiquewhite2",activeforeground = "black")
        self.tks["botones"][f"{numero}silla+"].place(x = self.des+self.grosor*5+self.des*2+self.grosor*3,y=self.grosor*2.5+ self.des*6+(self.grosor+self.des)*numero, width= self.grosor, height = self.grosor)
        "=============================================================================================================================================================================="
        self.tks["botones"][f"{numero}cantidad-"] = tk.Button(text="-",command = functools.partial(self.config,(f"-{1}","cantidad",numero)))
        self.tks["botones"][f"{numero}cantidad-"].config(bg = "antiquewhite2", fg = "black", activebackground = "antiquewhite2",activeforeground = "black")
        self.tks["botones"][f"{numero}cantidad-"].place(x = self.grosor*3+self.des*2+self.grosor*3+self.des*2+self.grosor*3,y=self.grosor*2.5+ self.des*6+(self.grosor+self.des)*numero, width= self.grosor, height = self.grosor)
        
        self.tks["labels"][f"{numero}cantidad"] = tk.Label(text= cantidad, bg = "antiquewhite2" ,activebackground= "antiquewhite2")
        self.tks["labels"][f"{numero}cantidad"].place(x = self.grosor*4+self.des*2+self.grosor*3+self.des*2+self.grosor*3,y=self.grosor*2.5+ self.des*6+(self.grosor+self.des)*numero, width= self.grosor, height = self.grosor)
        
        self.tks["botones"][f"{numero}cantidad+"] = tk.Button(text="+",command = functools.partial(self.config,(f"+{1}","cantidad",numero)))
        self.tks["botones"][f"{numero}cantidad+"].config(bg = "antiquewhite2", fg = "black", activebackground = "antiquewhite2",activeforeground = "black")
        self.tks["botones"][f"{numero}cantidad+"].place(x = self.grosor*5+self.des*2+self.grosor*3+self.des*2+self.grosor*3,y=self.grosor*2.5+ self.des*6+(self.grosor+self.des)*numero, width= self.grosor, height = self.grosor)
        "=============================================================================================================================================================================="
        self.tks["botones"][f"{numero}borrar"] = tk.Button(text="Borrar",command = functools.partial(self.borrar,numero))
        self.tks["botones"][f"{numero}borrar"].config(bg = "red2", fg = "black", activebackground = "red2",activeforeground = "black")
        self.tks["botones"][f"{numero}borrar"].place(x = self.grosor*6+self.des*3+self.grosor*3+self.des*2+self.grosor*3,y=self.grosor*2.5+ self.des*6+(self.grosor+self.des)*numero, width= self.grosor*2, height = self.grosor)
        "=============================================================================================================================================================================="
        self.tks["botones"]["nueva_configuracion"].place_forget()
        self.tks["botones"]["nueva_configuracion"].place(x = self.des,y=self.grosor*2.5+ self.des*6+(self.grosor+self.des)*(numero+1), width= self.grosor*12+self.des*3, height = self.grosor)
        "=============================================================================================================================================================================="
        if len(self.distribucion) == numero+1:
            self.actualizar()


class main_menu(): # Menu para crear o seleccionar distribucion
    
    def leer(self): # Se leen las configuraciones o se crean
        try:
            with open("Configuracion.pkl", "rb") as read_file:
                self.configuraciones = pickle.load(read_file)
        except FileNotFoundError as error_:
            self.configuraciones =  {}
    def nueva(self): # Vamos a la ventana de crear configuracion
        self.ventana.destroy()
        ventana_configuracion()
        
    def conf(self): # Vamos a la ventana de seleccion de configuraciones
        self.ventana.destroy()
        menu_configuraciones()
        
    def __init__(self): # Se crean los valores del menu principal y los botones
        
        self.leer()
        
        ancho = 300
        alto = 290
        self.des = 5
        self.grosor = 200
        
        self.tks = 	{
                    "botones" : {},
                    "labels" :	{}, 
                    "cajas" :	{}
                    }
        
        self.ventana = Tk()
        self.ventana.title("Inicio")
        self.ventana.config(bg = "gray")
        self.ventana.geometry(f"{ancho}x{alto}")
        
        self.tks["botones"]["cargar"] = tk.Button(text="Cargar distribucion",command = self.conf)
        self.tks["botones"]["cargar"].config(bg = "antiquewhite2", fg = "black", activebackground = "antiquewhite2",activeforeground = "black")
        self.tks["botones"]["cargar"].place(x = self.des,y=self.des, width= ancho-self.des*2, height = 90)
        
        self.tks["botones"]["nueva_configuracion"] = tk.Button(text="Crear distribucion",command = self.nueva)
        self.tks["botones"]["nueva_configuracion"].config(bg = "antiquewhite2", fg = "black", activebackground = "antiquewhite2",activeforeground = "black")
        self.tks["botones"]["nueva_configuracion"].place(x = self.des,y=self.des*2+90, width= ancho-self.des*2, height = 90)

        self.tks["botones"]["salir"] = tk.Button(text="Salir",command = salir)
        self.tks["botones"]["salir"].config(bg = "antiquewhite2", fg = "black", activebackground = "antiquewhite2",activeforeground = "black")
        self.tks["botones"]["salir"].place(x = self.des,y=self.des*3+90*2, width= ancho-self.des*2, height = 90)

        self.ventana.mainloop()


class menu_configuraciones(): # menu para seleccionar configuraciones
    
    def leer(self): # Se leen las configuraciones
        try:
            with open("Configuracion.pkl", "rb") as read_file:
                self.configuraciones = pickle.load(read_file)
        except FileNotFoundError as error_:
            self.configuraciones =  {}
    
    def actualizar(self): # Segun la configuracion seleccionada, se muestra como es con todas sus distribuciones
        
        for o in self.lista:
            
            o.destroy()
        
        self.lista = []
        
        if not self.combo.get() == "":
            
            for n,a in enumerate(self.configuraciones[self.combo.get()]["distribucion"]):
                
                self.lista.append(tk.Label(text= "", bg = "antiquewhite2" ,activebackground= "antiquewhite2"))
                self.lista[n].place(x=self.des, y=self.des*2+self.grosor*n+self.grosor, width =self.ancho-self.des*2, height=self.grosor)
                
                self.lista[n].config(text=f"{a}")
                
                print(a)
    
    def __init__(self): # Se crea la geometria de la ventana con su combo
        
        self.leer()
        
        self.lista = []

        self.ancho = 500
        self.alto = 400
        self.des = 15
        self.grosor = 20
        
        self.tks = 	{
                    "botones" : {},
                    "labels" :	{}, 
                    "cajas" :	{}
                    }
        
        self.ventana = Tk()
        self.ventana.title("Elegir configuracion")
        self.ventana.config(bg = "gray")
        self.ventana.geometry(f"{self.ancho}x{self.alto}")
        
        self.combo = ttk.Combobox(values=list(self.configuraciones.keys()), state='readonly')
        self.combo.place(x=self.des, y=self.des, width =self.ancho-self.des*2, height=self.grosor)
        self.combo.bind('<<ComboboxSelected>>', lambda _ : self.actualizar())

        self.tks["botones"]["OK"] = tk.Button(self.ventana,text="OK",command = self.ok)
        self.tks["botones"]["OK"].config(bg = "antiquewhite2", fg = "black", activebackground = "antiquewhite2",activeforeground = "black")
        self.tks["botones"]["OK"].place(x = self.des, y = self.alto-self.des-self.grosor*2, width = self.ancho-self.des*2,height= self.grosor*2)

        self.ventana.mainloop()

    def ok(self): #=====================================================================================================================================
        
        if not self.combo.get() == "":

            global distribucion, nombre 

            nombre = self.combo.get()
            distribucion = self.configuraciones[self.combo.get()]["distribucion"]

            self.ventana.destroy()
            menu_aplicacion()



class menu_aplicacion():

    def __init__(self):

        self.ancho = 550
        self.alto = 400
        self.des = 5
        self.grosor = 40
        


        self.tks = 	{
                    "botones" : {},
                    "labels" :	{}, 
                    "cajas" :	{}
                    }
        
        print(distribucion)

        self.ventana = Tk()
        self.ventana.title(F"Menu ({nombre})")
        self.ventana.config(bg = "gray")
        self.ventana.geometry(f"{self.ancho}x{self.alto}")

        self.botones = 0

        self.tks["botones"]["Mesas"] = tk.Button(self.ventana,text="Mesas",command = "")
        self.tks["botones"]["Mesas"].config(bg = "antiquewhite2", fg = "black", activebackground = "antiquewhite2",activeforeground = "black")
        self.tks["botones"]["Mesas"].place(x = self.des, y = self.des+(self.des+self.grosor)*self.botones, width = 120,height= self.grosor)
        self.botones += 1
        self.tks["botones"]["Mozos"] = tk.Button(self.ventana,text="Mozos",command = "")
        self.tks["botones"]["Mozos"].config(bg = "antiquewhite2", fg = "black", activebackground = "antiquewhite2",activeforeground = "black")
        self.tks["botones"]["Mozos"].place(x = self.des, y = self.des+(self.des+self.grosor)*self.botones, width = 120,height= self.grosor)
        self.botones += 1
        self.tks["botones"]["Pedidos"] = tk.Button(self.ventana,text="Pedidos",command = "")
        self.tks["botones"]["Pedidos"].config(bg = "antiquewhite2", fg = "black", activebackground = "antiquewhite2",activeforeground = "black")
        self.tks["botones"]["Pedidos"].place(x = self.des, y = self.des+(self.des+self.grosor)*self.botones, width = 120,height= self.grosor)
        self.botones += 1
        self.tks["botones"]["cuentas"] = tk.Button(self.ventana,text="Cuentas",command = "")
        self.tks["botones"]["cuentas"].config(bg = "antiquewhite2", fg = "black", activebackground = "antiquewhite2",activeforeground = "black")
        self.tks["botones"]["cuentas"].place(x = self.des, y = self.des+(self.des+self.grosor)*self.botones, width = 120,height= self.grosor)
        self.botones += 1
        self.tks["botones"]["configuracion"] = tk.Button(self.ventana,text="Configuracion",command = "")
        self.tks["botones"]["configuracion"].config(bg = "antiquewhite2", fg = "black", activebackground = "antiquewhite2",activeforeground = "black")
        self.tks["botones"]["configuracion"].place(x = self.des, y = self.des+(self.des+self.grosor)*self.botones, width = 120,height= self.grosor)
        self.botones += 1
        self.tks["botones"]["Salir"] = tk.Button(self.ventana,text="Salir",command = salir)
        self.tks["botones"]["Salir"].config(bg = "antiquewhite2", fg = "black", activebackground = "antiquewhite2",activeforeground = "black")
        self.tks["botones"]["Salir"].place(x = self.des, y = self.des+(self.des+self.grosor)*self.botones, width = 120,height= self.grosor)
       
        self.girar = True

        self.crear_listboxes()
    
        self.scrollbar.config(command=lambda *args: [self.listbox.yview(*args) for self.listbox in self.listboxes])
        #self.scrollbar.bind("<MouseWheel>", bloquear_scroll)
        self.scrollbar.place(x=120+ self.des*3+self.recorrido, y=self.des, height=(self.des+self.grosor)*(self.botones+1)-self.des)
        #self.scrollbar.place(x=120+ self.des*3+self.recorrido, y=self.des*2+(self.grosor-10), height=(self.des+self.grosor)*self.botones-self.des+10)

        self.ventana.mainloop()

    def crear_listboxes(self): # Crea las listboxes, los botones para ordenarlas y la scrolbar

        self.mesas = []
        numero = 1
        for dis in distribucion:
            for mesa in range(int(dis["cantidad"])):

                self.mesas.append([numero,dis["nombre"],dis["silla"],dis["mesa"],"Libre", "Juan"])
                numero += 1
        self.total_datos = len(self.mesas[0]) 

        self.ordenar()

        print(self.mesas_datos)

        self.scrollbar = ttk.Scrollbar(self.ventana,orient=tk.VERTICAL)
        
        # Se establecen los datos que van a haber y sus tamaños (se pueden agregar datos perfectamente)
        tipo = ("N°","tipo","sillas","mesas","estado","mozo")
        tamaño = (30,100,50,50,50,70)
        self.recorrido = 0
        self.listboxes = []
        

        def bloquear_scroll(event):
            # Evita que el evento de rueda del mouse se propague
            return "break"

        for i in range(self.total_datos): #crea todas las listboxe, segun la totalidad de datos
            self.listbox = tk.Listbox(self.ventana, yscrollcommand=self.scrollbar.set, justify=tk.CENTER)
            self.listbox.pack()
            self.listbox.place(x=120+ self.des*2+self.recorrido, y=self.des*2+(self.grosor-10), width=tamaño[i], height=(self.des+self.grosor)*self.botones-self.des+10)
            self.listbox.delete(0, "end")
            self.listbox.insert(tk.END, *self.mesas_datos[i])
            self.listbox.bind("<MouseWheel>", bloquear_scroll)  # Bloquear la rueda del mouse en la lista
            self.listboxes.append(self.listbox)
            

            self.tks["botones"][f"orden_{tipo[i]}"] = tk.Button(self.ventana,text=tipo[i].capitalize(),command = functools.partial(self.ordenar,i))
            self.tks["botones"][f"orden_{tipo[i]}"].config(bg = "chartreuse3", fg = "black", activebackground = "chartreuse3",activeforeground = "black")
            self.tks["botones"][f"orden_{tipo[i]}"].place(x = 120+ self.des*2+self.recorrido, y = self.des, width = tamaño[i],height= (self.grosor-10))

            self.recorrido += tamaño[i]
            
    def orden(self,e): #funcion para que sort ordene segun parametro
	
	    return(e[self.cual])

    def ordenar(self,cual=0): #ordena la lista de mesas segun parametro
        print("llegue")
        self.cual = cual
        if self.girar == False:
            self.girar = True
        else:
            self.girar = False
        self.mesas.sort(reverse=self.girar,key=self.orden)

        #Transforma la lista para que las listbox puedan leerla
        self.mesas_datos = []
        for n in range(len(self.mesas[0])):

            self.mesas_datos.append([])

        for mesa in self.mesas:

            for n,dato in enumerate(mesa):

                self.mesas_datos[n].append(dato)

        #si las lisboxs existen, las actualiza
        try:
            for i in range(self.total_datos):
                self.listboxes[i].delete(0, "end")
                self.listboxes[i].insert(tk.END, *self.mesas_datos[i])
        except:
            pass


while True:

    main_menu()









