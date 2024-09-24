import random
import tkinter as tk
from tkinter import ttk

# Funciones del algoritmo genético (importadas o definidas aquí)

# Configuración básica de la ventana
root = tk.Tk()  
root.title("Algoritmo Genético para el Problema de la Mochila")

# Datos de objetos
objetos = [('A', 3, 60), ('B', 2, 40), ('C', 4, 50), ('D', 1, 30)]

# Parámetros del algoritmo
tamaño_poblacion = 10
p_cruce = 0.8
p_mutacion = 0.1
generaciones = 50

#verifica basado en cada individuo, si el paso supera el tope de la maleta, sino returna el valor
def funcion_aptitud(individuo):
    peso = sum(ind[1] * x for ind, x in zip(objetos, individuo))
    valor = sum(ind[2] * x for ind, x in zip(objetos, individuo))
    if peso > int(capacidad_inp.get()):
        return 0  # Penalización por exceder el peso
    return valor

#retona probalidad de seleccion, basado en lo que retorna la funcion aptitud
def seleccion(poblacion):
    aptitudes = [funcion_aptitud(ind) for ind in poblacion]
    total_aptitud = sum(aptitudes)
    prob_seleccion = [apt / total_aptitud for apt in aptitudes]
    return random.choices(poblacion, weights=prob_seleccion, k=2)

#recibe 2 individuos, de los cuales cruza la mitad del primero con mitad del segundo para crear 2 individuos
def cruce(ind1, ind2):
    if random.random() < p_cruce:
        punto = random.randint(1, len(objetos) - 2)
        #:punto representa el punto de corte de los individuos
        nuevo_ind1 = ind1[:punto] + ind2[punto:]
        nuevo_ind2 = ind2[:punto] + ind1[punto:]
        return [nuevo_ind1, nuevo_ind2]
    return [ind1, ind2]

#se recibe un individuo, y badado en un indice se le cambia un valor
def mutacion(individuo):
    if random.random() < p_mutacion:
        #se obtiene un valor basado en el indice
        idx = random.randint(0, len(individuo) - 1)
        individuo[idx] = 1 - individuo[idx]
    return individuo

def obtener_valor_y_peso(mejor, objetos):
    peso_total = sum(obj[1] * m for obj, m in zip(objetos, mejor) if m == 1)
    valor_total = sum(obj[2] * m for obj, m in zip(objetos, mejor) if m == 1)
    
    return peso_total, valor_total

def run_algorithm():
    # Inicializar población
    poblacion = [[random.randint(0, 1) for _ in objetos] for _ in range(tamaño_poblacion)]
    print(poblacion)
    print("capacidad leida:", int(capacidad_inp.get()))
    # Ejecución del algoritmo genético
    for _ in range(generaciones):
        nueva_poblacion = []
        while len(nueva_poblacion) < tamaño_poblacion:
            #selecciona 2 opciones de la población inicial
            padres = seleccion(poblacion)
            hijos = cruce(*padres)
            nueva_poblacion.extend(mutacion(hijo) for hijo in hijos)
            #print("Agregando población:", nueva_poblacion)
        poblacion = nueva_poblacion

        # Resultado
        # print("Nueva población:", poblacion)
        mejor = max(poblacion, key=funcion_aptitud)
        print("Mejor solución:", mejor)
        peso_total, valor_total = obtener_valor_y_peso(mejor,objetos)
        mejor_str = ', '.join(str(x) for x in mejor)  
        descripcion_mejor = f"Mejor solución: [{mejor_str}], Peso total: {peso_total}, Valor total: {valor_total}"
        resultado_var.set(descripcion_mejor)
        print("Valor:", funcion_aptitud(mejor))

#Widgets de la interfaz de usuario
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Entrada para la capacidad de la mochila
capacidad_lbl = ttk.Label(frame, text="Capacidad de la Mochila (kg):")
capacidad_lbl.grid(row=0, column=0, sticky=tk.W)
capacidad_inp = ttk.Entry(frame)
capacidad_inp.grid(row=0, column=1, sticky=(tk.W, tk.E))

# Botón para ejecutar el algoritmo
run_btn = ttk.Button(frame, text="Ejecutar Algoritmo", command=run_algorithm)
run_btn.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))

# Etiqueta para mostrar el resultado
resultado_var = tk.StringVar()
resultado_lbl = ttk.Label(frame, textvariable=resultado_var)
resultado_lbl.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))

# Hacer que la columna de entrada se expanda con la ventana
frame.columnconfigure(1, weight=1)

root.mainloop()