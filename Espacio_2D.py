
from tkinter import *
from tkinter import ttk

import tkinter as tk
from PIL import ImageTk, Image
import math
import random




class espacio():
    
    areas = []
    
    def __init__(self):
        
        pass
        
    def agregar_espacio(self,espacio):
        
        global ventana
        
        if espacio.tipo == "rectangulo":
            
            for e in self.areas:
                
                if e.x > espacio.x and e.y > espacio.y: #Arriba - Izquierda
                    
                    if espacio.x + espacio.ancho > e.x and espacio.y + espacio.alto > e.y:
                        
                        print("estoy [Arriba - Izquierda] y tengo algo adentro")
                        
                        tks["labels"][f"{e}"].place_forget()
                        
                        tks["labels"][f"{e}xd"] = tk.Label(ventana,text= f"{e}xd",bg = f"red" ,activebackground= f"red")
                        tks["labels"][f"{e}xd"].place(x = e.x,y= e.y, width= (espacio.x+espacio.ancho), height = (espacio.y+espacio.alto))
                        
                        tks["labels"][f"{e}"].place(x = e.x,y= e.y, width= e.ancho, height = e.alto)
                        
                elif e.x > espacio.x and e.y < espacio.y: #Abajo - Izquierda
                    
                    print("a")
                    
                elif e.x < espacio.x and e.y > espacio.y: #Arriba - Derecha
                    
                    print("2")
                    
                elif e.x < espacio.x and e.y < espacio.y: #Abajo - Derecha
                    
                    if e.x + e.ancho > espacio.x and e.y + e.alto > espacio.y:
                        
                        print("estoy [Abajo - Derecha] y tengo algo adentro")
                
                
            
                
        
        
        self.areas.append(espacio)
        
        
        

class rectangulo():
    
    tipo = "rectangulo"
    
    def __init__(self,x = 0 ,y = 0 ,ancho = 0 ,alto = 0):
    
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        




# ~ esp.agregar_espacio(rectangulo(300,300,150,150))




ancho = 500
alto = 500
des = 5
grosor = 50

tks = 	{
        "botones" : {},
        "labels" :	{}, 
        "cajas" :	{}
        }
global ventana
ventana = Tk()
ventana.title("No se")
ventana.config(bg = "gray")
ventana.geometry(f"{ancho}x{alto}")

esp = espacio()

for a in esp.areas:
    
    c = random.randint(1,3)
    
    tks["labels"][f"{a}"] = tk.Label(text= f"{a}",bg = f"antiquewhite{c}" ,activebackground= f"antiquewhite{c}")
    tks["labels"][f"{a}"].place(x = a.x,y= a.y, width= a.ancho, height = a.alto)
    print(a)

esp.agregar_espacio(rectangulo(300,300,150,150))
esp.agregar_espacio(rectangulo(100,100,300,300))

ventana.mainloop()




