from tkinter import *
import csv
from tkinter import ttk, messagebox
from validacion_de_datos import validar_registro_usuario, checkear_bloqueo, buscar_usuario
import os

def ventana_principal():
    ventana_bienvenida = Tk()
    ventana_bienvenida.title("Ficha de Stock")
    ventana_bienvenida.resizable(0, 0)
    ventana_bienvenida.geometry("350x300")
    ventana_bienvenida.config(bg="#87CEFA")
    ventana_bienvenida.rowconfigure(0, weight=50)
    ventana_bienvenida.rowconfigure(3, weight=100)
    ventana_bienvenida.rowconfigure(6, weight=100)
    ventana_bienvenida.columnconfigure(0, weight=1)
    ventana_bienvenida.columnconfigure(3, weight=1)


    Label(ventana_bienvenida, text="Bienvenido a la ficha de Stock y entas.\nSi ya tiene un usuario, presione el botón 'Ingresar',\nde lo contrario, regístrese.").grid(row=1, column=1, columnspan=2, pady=15, sticky=W+E, ipady=5, ipadx=10)

    Button(ventana_bienvenida, text="Ingresar", command= mostrar_ventana_ingreso).grid(row=2, column=1, columnspan=2, sticky=W+E)
    Button(ventana_bienvenida, text="Registrarse", command= mostrar_ventana_registro).grid(row=3, column=1, columnspan=2, sticky=W+E)

    Label(ventana_bienvenida, text="Construída por", fg="#8c8c8c").grid(row=4, column=1, columnspan=2, pady=10, sticky=W+E+S, ipady=5)
    Label(ventana_bienvenida, text="Diego López", justify="left", fg="#8c8c8c").grid(row=5, column=1, columnspan=2, sticky=W+E, ipady=5)
    ventana_bienvenida.mainloop()


def mostrar_ventana_registro():

    # Configuracion ventana
    ventana_registro = Toplevel()
    ventana_registro.title("Registro de usuario")
    #ventana_registro.iconbitmap("./logos/icono.ico")
    ventana_registro.resizable(0, 0)
    ventana_registro.geometry("350x300")
    ventana_registro.config(bg="#87CEFA")
    ventana_registro.rowconfigure(0, weight=1)
    ventana_registro.rowconfigure(4, weight=1)
    ventana_registro.rowconfigure(8, weight=1)
    ventana_registro.columnconfigure(0, weight=1)
    ventana_registro.columnconfigure(3, weight=1)

    # Labels y botones
    Label(ventana_registro, text="Ingrese un usuario:").grid(row=1, column=1, sticky=W+E, pady=5, padx=5)
    Label(ventana_registro, text="Ingrese una clave").grid(row=2, column=1, sticky=W+E, pady=5, padx=5)

    entry_usuario = Entry(ventana_registro)
    entry_usuario.grid(row=1, column=2)

    entry_clave = Entry(ventana_registro)
    entry_clave.grid(row=2, column=2)

    # Menu desplegable
    preguntas = cargar_preguntas()
    desplegable_preguntas = ttk.Combobox(ventana_registro, values=preguntas)
    desplegable_preguntas.set("Seleccione pregunta")
    desplegable_preguntas.grid(row=3, column=1, sticky=W+E, pady=5, padx=5)

    entry_respuesta_pregunta = Entry(ventana_registro)
    entry_respuesta_pregunta.grid(row=3, column=2, sticky=W+E, pady=10, padx=5)

    # Boton para registrar
    Button(ventana_registro, text="Registrar",command= lambda: validar_registro_usuario(entry_usuario.get(), entry_clave.get(), desplegable_preguntas.get(), entry_respuesta_pregunta.get())).grid(row=5, column=1, columnspan=2, sticky=W+E, pady=10)

    # Requisitos
    Label(ventana_registro, text="El identificador debe estar compuesto solo de\nletras, numeros o los caracteres '_' '-' y '.'\ny debe tener minimo 5 y maximo 15 caracteres", justify="left", fg="#8c8c8c").grid(row=6, column=1, columnspan=2, sticky=W+E, pady=5)
    Label(ventana_registro, text="Requisitos de la clave:\n- De 4 a 8 caracteres\t- Al menos un numero\n- Al menos una mayuscula\t- Incluye '_' '-' '#' o '*'\n- Al menos una minuscula\t- Adyacentes no repetidos", justify="left", fg="#8c8c8c").grid(row=7, column=1, columnspan=2)

def cargar_preguntas():
    """
    Funcion modularizada,que carga las preguntas del archivo y devuelve la coleccion.
    """
    with open("./archivos csv/preguntas.csv") as file:
        preguntas = []
        reader = csv.reader(file)
        for row in reader:
            preguntas.append(row[1])
    return preguntas

def mostrar_ventana_ingreso():
    """
    Diego López: Ventana de acceso en la que se colocan todos los
    datos del usuario ingresante para su posterior checkeo.

    Martin Ferreyra: Modificaciones visuales.
    """

    # Configuracion ventana
    ventana_ingreso = Toplevel()
    ventana_ingreso.title("Identificación para acceso")
    #ventana_ingreso.iconbitmap("./logos/icono.ico")
    ventana_ingreso.resizable(0, 0)
    ventana_ingreso.geometry("350x200")
    ventana_ingreso.config(bg="#87CEFA")
    ventana_ingreso.rowconfigure(0, weight=1)
    ventana_ingreso.rowconfigure(3, weight=1)
    ventana_ingreso.rowconfigure(6, weight=1)
    ventana_ingreso.columnconfigure(0, weight=1)
    ventana_ingreso.columnconfigure(3, weight=1)

    # Labels y entrys
    Label(ventana_ingreso, text="Ingrese su usuario:").grid(row=1, column=1, sticky=W+E, pady=5, ipadx=10, ipady=1)
    entry_usuario_ingreso = Entry(ventana_ingreso)
    entry_usuario_ingreso.grid(row=1, column=2, sticky=E, padx=5)

    Label(ventana_ingreso, text="Ingrese su clave:").grid(row=2, column=1, sticky=W+E, pady=5, ipadx=10, ipady=1)
    entry_clave_ingreso = Entry(ventana_ingreso, show="*")
    entry_clave_ingreso.grid(row=2, column=2, sticky=E, padx=5)

    Button(ventana_ingreso, text="Ingresar", command=lambda: validar_ingreso(ventana_ingreso, entry_usuario_ingreso.get(), entry_clave_ingreso.get())).grid(row=4, column=1, columnspan=2, sticky=W+E)
    Button(ventana_ingreso, text="He olvidado mi contraseña", command= ventana_recuperar_clave).grid(row=5, column=1, columnspan=2, sticky=W+E, pady=5)
    
    # Vincula la tecla Enter al botón
    entry_clave_ingreso.bind("<Return>", lambda event=None: validar_ingreso(ventana_ingreso, entry_usuario_ingreso.get(), entry_clave_ingreso.get()))

def ventana_recuperar_clave():
    """
    Martin Ferreyra: Se abre una pestaña correspondiente a la recuperacion de clave,
    el usuario ingresado para la recuperacion tiene que existir y no estar bloqueado.
    """

    # Configuracion ventana
    ventana_recuperacion = Toplevel()
    ventana_recuperacion.title("Recuperación clave")
    ventana_recuperacion.iconbitmap("./logos/icono.ico")
    ventana_recuperacion.resizable(0, 0)
    ventana_recuperacion.geometry("350x250")
    ventana_recuperacion.config(bg="#87CEFA")
    ventana_recuperacion.rowconfigure(0, weight=1)
    ventana_recuperacion.rowconfigure(4, weight=1)
    ventana_recuperacion.rowconfigure(6, weight=1)
    ventana_recuperacion.columnconfigure(0, weight=1)
    ventana_recuperacion.columnconfigure(1, weight=1)
    ventana_recuperacion.columnconfigure(2, weight=1)
    ventana_recuperacion.columnconfigure(3, weight=1)

    # Labels y entrys
    Label(ventana_recuperacion, text="Si ha olvidado su contraseña,\npor favor complete todos los campos.").grid(row=1, column=1, columnspan=2, sticky=W+E, pady=5, ipady=5)
    Label(ventana_recuperacion, text="Ingrese su usuario:").grid(row=2, column=1, sticky=W+E, pady=5, ipady=1)
    
    entry_usuario_recuperacion = Entry(ventana_recuperacion)
    entry_usuario_recuperacion.grid(row=2, column=2, sticky=W+E, padx=5)

    
    # Desplegable de preguntas
    
    preguntas = cargar_preguntas()
    desplegable_preguntas = ttk.Combobox(ventana_recuperacion, values=preguntas)
    desplegable_preguntas.set("Seleccione pregunta")
    desplegable_preguntas.grid(row=3, column=1, sticky=W+E, pady=5, padx=5)

    entry_respuesta_pregunta = Entry(ventana_recuperacion)
    entry_respuesta_pregunta.grid(row=3, column=2, sticky=W+E, pady=10, padx=5)

    Button(ventana_recuperacion, text="Recuperar", command= lambda: recuperar_clave(entry_usuario_recuperacion.get(), desplegable_preguntas.get(), entry_respuesta_pregunta.get())).grid(row=5, column=1, columnspan=2, sticky=W+E)


def recuperar_clave(id_usuario, id_pregunta, respuesta_recuperacion):
    """
    Martin Ferreyra: Funcion ejecutada en el intento de recuperacion de clave
    en la ventana 'Recuperacion de clave' que maneja los distintos escenarios,
    es decir: Si se dio un usuario valido, si la pregunta o respuesta de
    recuperacion son incorrectas, si el usuario se encuentra bloqueado, etc. 
    """

    if id_usuario:
        usuario = buscar_usuario(id_usuario)

        if usuario:
            bloqueado = checkear_bloqueo(id_usuario)

            if not bloqueado:

                if usuario[2] == id_pregunta and usuario[3] == respuesta_recuperacion:
                    messagebox.showinfo("Éxito", f"Su constraseña es: {usuario[1]}")
                    actualizar_intentos_recuperacion(usuario, reinicio=True)
                else:
                    messagebox.showerror("Error", "Respuesta incorrecta")
                    actualizar_intentos_recuperacion(usuario)
            else:
                messagebox.showerror("Error", "Usuario bloqueado")
        
        else:
            messagebox.showerror("Error", "Verifique los datos")
    
    else:
        messagebox.showerror("Error", "Verifique los datos")


def actualizar_intentos_recuperacion(datos_usuario, reinicio=False):
    """
    Martin Ferreyra: En caso de introducitse un usuario valido en la ventana de
    'Recuperacion de clave', esta funcion evalua actualiza los intentos de
    recuperacion, sumando uno o reiniciando la cuenta de intentos.
    """

    registro_existente = False

    # Abrir los registros existentes de intentos de recuperacion
    with open("./archivos csv/recuperacion.csv", "r+") as datos_recuperaciones:
        reader = csv.reader(datos_recuperaciones)

        # Abrir nuevo archivo en donde se registra la informacion existente mas la actualizacion
        with open("./archivos csv/actualizacion.csv", "x+", newline='') as actualizacion:
            writer = csv.writer(actualizacion)

            # Recorrer lineas de registros existentes
            for row in reader:
                if row and row[0] == datos_usuario[0] and int(row[1]) <= 3:
                    if reinicio:
                        writer.writerow([datos_usuario[0],0])
                    else:
                        writer.writerow([datos_usuario[0],int(row[1]) + 1])
                    registro_existente = True

                elif row and row[0] == datos_usuario[0] and int(row[1]) > 3:
                    messagebox.showerror("Error", "Usuario Bloqueado")
                    writer.writerow([datos_usuario[0],int(row[1]) + 1])
                    registro_existente = True
                else:
                    writer.writerow(row)
            
            # Si el usuario no existia en el archivo, se agrega
            if not registro_existente:
                writer.writerow([datos_usuario[0],1])
            
    os.remove("./archivos csv/recuperacion.csv")
    os.rename("./archivos csv/actualizacion.csv", "./archivos csv/recuperacion.csv")



def validar_ingreso(ventana_ingreso, id_usuario, clave):
    """
    Diego López: Funcion que valida el ingreso del usuario si sus datos, es decir,
    su id_usuario y su clave, son las mismas que en el archivo usuarios.csv.

    Martin Ferreyra: Agregado el escenario en el que el usuario introducido sea
    un usuario bloqueado, cuyo caso se niega el acceso con una advertencia.
    """
    usuario = buscar_usuario(id_usuario)

    if usuario:
        if checkear_bloqueo(id_usuario):
            messagebox.showerror("Error", "Usuario bloqueado")
        
        elif usuario[1] == clave:
            messagebox.showinfo("Éxito", "Ingreso exitoso")
            ventana_ingreso.destroy()
            mostrar_ventana_stock(id_usuario)

        else:
            messagebox.showerror("Error", "Ingreso fallido. Verifique sus credenciales")
    
    else:
        messagebox.showerror("Error", "Ingreso fallido. Verifique sus credenciales")

def agregar_producto(id_usuario, nombre, precio, cantidad):
    try:
        # Verificar si los campos numéricos son válidos
        precio = float(precio)
        cantidad = int(cantidad)

        # Agregar el producto con la fecha al archivo CSV
        with open("./archivos csv/inventario.csv", "a", newline='') as archivo:
            writer = csv.writer(archivo)
            writer.writerow([id_usuario, nombre, precio, cantidad])

        guardar_inventario({nombre: cantidad}, id_usuario)  # Add this line

        messagebox.showinfo("Éxito", "Producto agregado con éxito")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos para precio y cantidad.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al agregar el producto: {e}")




def mostrar_ventana_stock(id_usuario):

    inventario = cargar_inventario()
    ventana_stock = Toplevel()
    ventana_stock.title("Inventario de Productos")
    # ventana_stock.iconbitmap("./logos/logo.ico")
    ventana_stock.resizable(0, 0)
    ventana_stock.geometry("500x400")
    ventana_stock.config(bg="#00FA9A")

    # Etiquetas y campos de entrada para la información del producto
    Label(ventana_stock, text="Nombre del Producto:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
    entry_nombre_producto = Entry(ventana_stock)
    entry_nombre_producto.grid(row=0, column=1, padx=10, pady=10)

    Label(ventana_stock, text="Precio del Producto:").grid(row=1, column=0, padx=10, pady=10, sticky=W)
    entry_precio_producto = Entry(ventana_stock)
    entry_precio_producto.grid(row=1, column=1, padx=10, pady=10)

    Label(ventana_stock, text="Cantidad en Stock:").grid(row=2, column=0, padx=10, pady=10, sticky=W)
    entry_cantidad_stock = Entry(ventana_stock)
    entry_cantidad_stock.grid(row=2, column=1, padx=10, pady=10)

    # Botón para agregar el producto
    Button(ventana_stock, text="Agregar Producto", command=lambda: agregar_producto(id_usuario, entry_nombre_producto.get(), entry_precio_producto.get(), entry_cantidad_stock.get())).grid(row=3, column=0, columnspan=2, pady=10)

    # Botón para ver el inventario
    Button(ventana_stock, text="Ver Inventario", command=lambda: ver_inventario()).grid(row=4, column=0, columnspan=2, pady=10)
    
    #Botón para realizar venta
    Button(ventana_stock, text="Realizar Venta", command=lambda: mostrar_ventana_ventas(id_usuario)).grid(row=5, column=0, columnspan=2, pady=10)

    # Etiquetas y botones adicionales según sea necesario

def ver_inventario():
    # Lógica para mostrar el inventario en una nueva ventana
    ventana_inventario = Toplevel()
    ventana_inventario.title("Inventario Actual")

    try:
        with open("./archivos csv/inventario.csv", newline='') as archivo:
            reader = csv.reader(archivo)

            # Ignorar la primera fila si es un encabezado
            next(reader, None)

            for i, fila in enumerate(reader, start=1):
                Label(ventana_inventario, text=f"Fila {i}: {fila}").pack()
    except Exception as e:
        print(f"Error al cargar el inventario: {e}")


def mostrar_ventana_inicio():
    
    ventana_bienvenida = Tk()
    ventana_bienvenida.title("Ficha de Stock")
    ventana_bienvenida.resizable(1,1)
    ventana_bienvenida.geometry("350x350")
    ventana_bienvenida.config(bg="white")

    miFrame = Frame()
    miFrame.grid()
    miFrame.config(bg="white")
    miFrame.config(width="650", height="650")

def mostrar_ventana_ventas(id_usuario):

    ventana_ventas = Toplevel()
    ventana_ventas.title("Realizar Venta")
    ventana_ventas.resizable(0, 0)
    ventana_ventas.geometry("400x250")
    ventana_ventas.config(bg="#00FA9A")

    # Etiquetas y campos de entrada para la información de la venta
    Label(ventana_ventas, text="Nombre del Producto:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
    entry_nombre_producto_venta = Entry(ventana_ventas)
    entry_nombre_producto_venta.grid(row=0, column=1, padx=10, pady=10)

    Label(ventana_ventas, text="Cantidad a Vender:").grid(row=1, column=0, padx=10, pady=10, sticky=W)
    entry_cantidad_venta = Entry(ventana_ventas)
    entry_cantidad_venta.grid(row=1, column=1, padx=10, pady=10)

    # Botón para realizar la venta
    Button(ventana_ventas, text="Realizar Venta", command=lambda: realizar_venta(id_usuario, entry_nombre_producto_venta.get(), entry_cantidad_venta.get())).grid(row=2, column=0, columnspan=2, pady=10)

# Puedes agregar más funciones según sea necesario


def realizar_venta(id_usuario, nombre_producto_venta, cantidad_venta):
    try:
        cantidad_venta = int(cantidad_venta)
        inventario = cargar_inventario()
        guardar_inventario(inventario, id_usuario)

        if nombre_producto_venta in inventario:
            stock_actual = inventario[nombre_producto_venta]

            if stock_actual >= cantidad_venta:
                inventario[nombre_producto_venta] -= cantidad_venta
                guardar_inventario(inventario, id_usuario)
                messagebox.showinfo("Éxito", f"Venta realizada: {cantidad_venta} {nombre_producto_venta}")
            else:
                messagebox.showerror("Error", "Stock insuficiente para realizar la venta")
        else:
            messagebox.showerror("Error", "El producto no existe en el inventario")

    except Exception as e:
        print(f"Error al realizar la venta: {e}")

# Puedes agregar más funciones según sea necesario

def cargar_inventario():
    inventario = {}
    try:
        with open("./archivos csv/inventario.csv", newline='') as archivo:
            reader = csv.reader(archivo)
            next(reader, None)  # Ignorar la primera fila si es un encabezado
            for fila in reader:
                nombre_producto = fila[1]
                cantidad_stock = int(fila[3])
                inventario[nombre_producto] = cantidad_stock
    except Exception as e:
        print(f"Error al cargar el inventario: {e}")

    return inventario

def guardar_inventario(inventario, id_usuario):
    try:
        with open("./archivos csv/inventario.csv", "r", newline='') as archivo:
            reader = csv.reader(archivo)
            rows = list(reader)

        with open("./archivos csv/inventario.csv", "w", newline='') as archivo:
            writer = csv.writer(archivo)
            for row in rows:
                if row and row[0] == id_usuario and row[1] in inventario:
                    row[3] = str(inventario[row[1]])
                writer.writerow(row)
    except Exception as e:
        print(f"Error al guardar el inventario: {e}")



ventana_principal()