# === Instalación y verificación de dependencias necesarias ===
import subprocess
import sys

print("un momento estamos instalando todo lo necesario  :3")

def actualizar_pip():

    """
    Intenta actualizar pip a la última versión.
    """

    try:
        print("Actualizando pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("pip actualizado correctamente.")
    except subprocess.CalledProcessError:
        print("Error al actualizar pip.")
actualizar_pip()

# Lista de paquetes externos y módulos estándar requeridos

paquetes = ["Pillow", "matplotlib", "matplotlib-venn"]
modulos_estandar = ["tkinter", "os", "subprocess", "sys"]

# Verifica e instala los paquetes necesarios
for paquete in paquetes:
    try:
        nombre_import = "PIL" if paquete == "Pillow" else paquete
        __import__(nombre_import)
    except ImportError:
        print(f"Instalando {paquete}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", paquete])
            print(f"{paquete} instalado correctamente.")
        except subprocess.CalledProcessError:
            print(f"Error al instalar {paquete}.")

print("listo puedes continuar...")


# === Librerias necesarias ===
import tkinter as tk
import os
from tkinter import messagebox
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib_venn import venn2, venn3
import subprocess
from tkinter import PhotoImage
from PIL import Image

# === Funciones de operaciones entre conjuntos ===
def union(conj1, conj2):
    """Retorna la unión entre dos conjuntos."""
    return conj1.union(conj2)

def interseccion(conj1, conj2):
    """Retorna la intersección entre dos conjuntos."""
    return conj1.intersection(conj2)

def diferencia(conj1, conj2):
    """Retorna la diferencia entre dos conjuntos (conj1 - conj2)."""
    return conj1.difference(conj2)

def diferencia_simetrica(conj1, conj2):
    """Retorna la diferencia simétrica entre dos conjuntos."""
    return conj1.symmetric_difference(conj2)

def complemento(conj, universo):
    """Retorna el complemento del conjunto respecto al universo."""
    return universo.difference(conj)

# === Gestión de conjuntos cargados ===
conjuntos = {}
canvas_diagrama = None
def cargar_conjuntos_desde_archivo(nombre_archivo="conjuntos.txt"):
    """
    Carga conjuntos desde un archivo de texto con formato: nombre:elem1,elem2,...
    """

    try:
        with open(nombre_archivo, "r") as f:
            for linea in f:
                if ":" in linea:
                    nombre, elementos = linea.strip().split(":")
                    conjunto = set(e.strip() for e in elementos.split(",") if e.strip())
                    conjuntos[nombre] = conjunto
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo de conjuntos no encontrado.")
    actualizar_lista_conjuntos()

def actualizar_lista_conjuntos():
    """Actualiza la lista visual de conjuntos en la interfaz."""
    lista.delete(0, tk.END)
    for nombre, elementos in conjuntos.items():
        lista.insert(tk.END, f"{nombre} = {{{', '.join(sorted(elementos))}}}")


# === Funciones relacionadas con el programa en C++ ===
def ejecutar_cpp_en_ventana():
    """Ejecuta el programa C++ en una nueva ventana CMD."""

    try:
        subprocess.Popen(["start", "cmd", "/c", "conjuntos.exe"], shell=True)
        messagebox.showinfo("Ejecutando", "Se ha abierto una ventana para crear conjuntos.\nCompleta el proceso y luego vuelve aquí.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo ejecutar el código C++: {e}")
        
def cargar_desde_cpp():
    """Carga los conjuntos generados desde el programa en C++."""

    try:
        cargar_conjuntos_desde_archivo()
        messagebox.showinfo("Conjuntos Cargados", "Los conjuntos fueron cargados exitosamente desde conjuntos.txt.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar: {e}")

def crear_nuevo_conjunto():
 """Llama al programa en C++ para crear un nuevo conjunto."""

 ejecutar_cpp_en_ventana()

def limpiar_lista_de_conjuntos():
    """Limpia todos los conjuntos cargados."""

    conjuntos.clear()
    lista.delete(0, tk.END)

def eliminar_un_conjunto_especifico_de_la_lista():
    seleccion = lista.curselection()
    """Elimina un conjunto seleccionado de la lista."""
    if seleccion:
        item_texto = lista.get(seleccion[0])
        nombre_conjunto = item_texto.split("=")[0].strip()
        if nombre_conjunto in conjuntos:
            del conjuntos[nombre_conjunto]
            actualizar_lista_conjuntos()
    else:
        messagebox.showwarning("Advertencia", "Selecciona un conjunto para eliminar.")

def salir():
    """Cierra la aplicación."""
    ventana.destroy()

# === Visualización en Diagramas de Venn ===
def generar_diagrama():
    """
    Genera un diagrama de Venn (2 o 3 conjuntos seleccionados).
    """

    sel = lista.curselection()
    nombres_sel = [lista.get(i).split('=')[0].strip() for i in sel]
    if len(nombres_sel) not in [2, 3]:
        messagebox.showwarning("Atención", "Selecciona 2 o 3 conjuntos para generar un diagrama de Venn.")
        return
    conj_list = [conjuntos[nombre] for nombre in nombres_sel]
    global canvas_diagrama
    for widget in frame_centro.winfo_children():
        widget.destroy()
    fig, ax = plt.subplots(figsize=(5.5, 4))
    if len(conj_list) == 2:
        venn2(conj_list, set_labels=nombres_sel)
    else:
        venn3(conj_list, set_labels=nombres_sel)
    plt.title("Diagrama de Venn")
    canvas_diagrama = FigureCanvasTkAgg(fig, master=frame_centro)
    canvas_diagrama.draw()
    canvas_diagrama.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# === Mostrar resultados de operaciones ===
def mostrar_resultado(op):
    """
    Muestra el resultado de la operación de conjuntos seleccionada.
    """

    sel = lista.curselection()
    nombres_sel = [lista.get(i).split('=')[0].strip() for i in sel]

    resultado = set()
    operacion = ""
    valido = True

    if op in ["Unión", "Intersección", "Diferencia", "Diferencia Simétrica"]:
        if len(nombres_sel) < 2:
            messagebox.showwarning("Atención", "Selecciona dos conjuntos para esta operación.")
            return
        A, B = conjuntos[nombres_sel[0]], conjuntos[nombres_sel[1]]
        if op == "Unión":
            resultado = union(A, B)
            print(f"{A} ∪ {B} = {{{', '.join(sorted(resultado))}}}")
        elif op == "Intersección":
            resultado = interseccion(A, B)
            print(f"{A} ∩ {B} = {{{', '.join(sorted(resultado))}}}")
        elif op == "Diferencia":
            resultado = diferencia(A, B)
            print(f"{A} - {B} = {{{', '.join(sorted(resultado))}}}")
        elif op == "Diferencia Simétrica":
            resultado = diferencia_simetrica(A, B)
            print(f"{A} △ {B} = {{{', '.join(sorted(resultado))}}}")

        operacion = f"{nombres_sel[0]} {op} {nombres_sel[1]}"

    elif op == "Complemento":
        if len(nombres_sel) != 1:
            messagebox.showwarning("Atención", "Selecciona solo un conjunto para el complemento.")
            return
        c = nombres_sel[0]
        universo = set().union(*conjuntos.values())
        resultado = complemento(conjuntos[c], universo)
        operacion = f"Complemento de {c}"
    else:
        valido = False

    if valido:
        texto_resultado.delete("1.0", tk.END)
        texto_resultado.insert(tk.END, f"{operacion} = {{ {', '.join(sorted(resultado))} }}")

        for widget in frame_centro.winfo_children():
            widget.destroy()
        fig, ax = plt.subplots(figsize=(5.5, 4))
        if op == "Complemento":
            venn2([universo, conjuntos[c]], set_labels=("Universal", c))
        else:
            venn2([A, B], set_labels=(nombres_sel[0], nombres_sel[1]))
        plt.title(operacion)
        global canvas_diagrama
        canvas_diagrama = FigureCanvasTkAgg(fig, master=frame_centro)
        canvas_diagrama.draw()
        canvas_diagrama.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# === Interfaz gráfica principal ===
def iniciar_programa_principal():
    """
    Inicializa y ejecuta la interfaz gráfica del programa.
    """

    global ventana, lista, frame_centro, texto_resultado, canvas_diagrama

    ventana = tk.Tk()
    ventana.title("Teoría de Conjuntos")
    ventana.geometry("1000x580")
    tk.Label(ventana, text="Teoría de Conjuntos", font=("Arial", 20, "bold"), fg="red", bg="yellow").pack(fill=tk.X)

    # Panel Izquierdo - Lista de conjuntos
    frame_izq = tk.Frame(ventana)
    frame_izq.place(x=10, y=50, width=220, height=300)
    tk.Label(frame_izq, text="Conjuntos Guardados", font=("Arial", 12, "bold"), borderwidth=2, relief="groove").pack(fill=tk.X)
    lista = tk.Listbox(frame_izq, selectmode=tk.MULTIPLE)
    lista.pack(fill=tk.BOTH, expand=True)

    # Panel Central - Diagrama
    frame_centro = tk.Frame(ventana, bg="skyblue")
    frame_centro.place(x=240, y=50, width=500, height=300)

    # Panel Derecho - Resultado de operaciones
    frame_der = tk.Frame(ventana)
    frame_der.place(x=750, y=50, width=220, height=300)
    tk.Label(frame_der, text="Resultado de la operación", font=("Arial", 12, "bold"), borderwidth=2, relief="groove").pack(fill=tk.X)
    texto_resultado = tk.Text(frame_der, wrap=tk.WORD, height=15)
    texto_resultado.pack(fill=tk.BOTH, expand=True)

    # Botones principales
    tk.Button(ventana, text="Actualizar Lista de Conjuntos", command=cargar_desde_cpp, bg="blue", fg="white").place(x=240, y=360)
    tk.Button(ventana, text="Generar diagrama", command=generar_diagrama, bg="red", fg="white").place(x=450, y=360)
    tk.Button(ventana, text="Crear nuevo conjunto", command=crear_nuevo_conjunto, bg="green", fg="white").place(x=615, y=360)
    tk.Button(ventana, text="Limpiar", command=limpiar_lista_de_conjuntos, bg="red", fg="white").place(x=80, y=400)
    tk.Button(ventana, text="Eliminar un conjunto en especifico", command=eliminar_un_conjunto_especifico_de_la_lista, bg="yellow", fg="black").place(x=20, y=360)
    tk.Label(ventana, text="Operaciones Disponibles", bg="yellow", font=("Arial", 15, "bold")).place(x=380, y=420)
    tk.Button(ventana, text="Salir del programa", command=salir, bg="red", fg="white").place(x=880, y=530)

    # Botones de operaciones de conjuntos
    tk.Button(ventana, text="UNIÓN", bg="lightgreen", width=18, command=lambda: mostrar_resultado("Unión")).place(x=230, y=460)
    tk.Button(ventana, text="INTERSECCIÓN", bg="lightgreen", width=18, command=lambda: mostrar_resultado("Intersección")).place(x=410, y=460)
    tk.Button(ventana, text="DIFERENCIA", bg="lightgreen", width=18, command=lambda: mostrar_resultado("Diferencia")).place(x=590, y=460)
    tk.Button(ventana, text="DIFERENCIA SIMÉTRICA", bg="lightgreen", width=18, command=lambda: mostrar_resultado("Diferencia Simétrica")).place(x=320, y=520)
    tk.Button(ventana, text="COMPLEMENTO", bg="lightgreen", width=18, command=lambda: mostrar_resultado("Complemento")).place(x=510, y=520)

    ventana.mainloop()


# === Cuadro de presentacion del grupo ===
import tkinter as tk
from PIL import Image, ImageTk

def mostrar_splash_screen(callback):
    """
    Muestra una pantalla de presentación antes de abrir la interfaz principal.
    """

    splash = tk.Tk()
    splash.title("Proyecto Estructuras Lógicas")
    splash.resizable(False, False)

 # Centrado y dimencones de la ventana de presentacion
    ancho_ventana = 600
    alto_ventana = 300
    pantalla_ancho = splash.winfo_screenwidth()
    pantalla_alto = splash.winfo_screenheight()
    x = (pantalla_ancho - ancho_ventana) // 2
    y = (pantalla_alto - alto_ventana) // 2
    splash.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
    splash.configure(bg="#0C6913") 

   # Imagen y mensaje del proyecto
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_imagen = os.path.join(ruta_base, "logomeso.jpg")
    imagen = Image.open(ruta_imagen)
    imagen = imagen.resize((250, 100))  
    imagen_tk = ImageTk.PhotoImage(imagen)

    etiqueta_imagen = tk.Label(splash, image=imagen_tk, bg="#0C6913")
    etiqueta_imagen.image = imagen_tk 
    etiqueta_imagen.pack(pady=(10, 0))  

    mensaje = (
        "ESTRUCTURAS LÓGICAS\n"
        "PROYECTO: Programa de creación, operación y graficación de conjuntos.\n\n"
        "INTEGRANTES:\n"
        "🟢 Wendy Yamileth López Quijivix         - Carnet No. 202508081\n"
        "🟢 Emily Dayana Del Carmen Cabrera   - Carnet No. 202508083\n"
        "🟢 Miguel Abraham Mendoza López      - Carnet No. 202508086"
    )

    etiqueta_texto = tk.Label(
        splash,
        text=mensaje,
        font=("Helvetica", 13, "bold"),
        fg="black",
        bg="white",
        justify="left",
        wraplength=550
    )
    etiqueta_texto.pack(pady=(10, 0))  


    # Cierra el Cuadro de presentacion del grupo y lanza el programa principal
    def cerrar_y_abrir():
        splash.destroy()
        callback()

    splash.after(10000, cerrar_y_abrir)
    splash.bind("<Key>", lambda event: cerrar_y_abrir())

    splash.mainloop()

# === Lanzamiento del programa ===
mostrar_splash_screen(iniciar_programa_principal)
