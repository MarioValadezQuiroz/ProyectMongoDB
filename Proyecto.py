#Importamos Librerias
import pymongo
import tkinter as tk
from tkinter import messagebox

# Conexión a la base de datos MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
# Conexión a MongoDB con autenticación
#client = pymongo.MongoClient("mongodb://adminUser:adminPassword@localhost:27017/?authSource=admin")

db = client["Proyecto3"]
collection = db["users"]

#Interfaz del Programa
# Crear la ventana principal
root = tk.Tk()
root.title("Gestión de Datos")
root.geometry("400x400")

# Funciones CRUD
def crear_registro():
    def guardar_datos():
        nombre = entry_nombre.get()
        edad = entry_edad.get()
        sexo = entry_sexo.get()

        # Aquí puedes añadir más campos según sea necesario

        # Usar una transacción para guardar los datos
        with client.start_session() as session:
            with session.start_transaction():
                collection.insert_one({"nombre": nombre, "edad": edad, "sexo": sexo}, session=session)

        messagebox.showinfo("Información", "Registro creado exitosamente")

    # Ventana para la entrada de datos
    crear_ventana = tk.Toplevel(root)
    crear_ventana.title("Crear Registro")

    tk.Label(crear_ventana, text="Nombre").pack()
    entry_nombre = tk.Entry(crear_ventana)
    entry_nombre.pack()

    tk.Label(crear_ventana, text="Edad").pack()
    entry_edad = tk.Entry(crear_ventana)
    entry_edad.pack()

    tk.Label(crear_ventana, text="Sexo").pack()
    entry_sexo = tk.Entry(crear_ventana)
    entry_sexo.pack()

    btn_guardar = tk.Button(crear_ventana, text="Guardar", command=guardar_datos)
    btn_guardar.pack()

    pass


def leer_registros():
    # Ventana para mostrar los registros
    leer_ventana = tk.Toplevel(root)
    leer_ventana.title("Leer Registros")

    registros = collection.find()

    for registro in registros:
        tk.Label(leer_ventana, text=f"Nombre: {registro['nombre']}, "
                                    f"Edad: {registro['edad']}, Sexo: {registro['sexo']}").pack()

    pass


def actualizar_registro():
    def guardar_cambios():
        query = {"nombre": entry_nombre_actual.get()}
        nuevos_datos = {"$set": {"nombre": entry_nombre_nuevo.get(), "edad": entry_edad_nueva.get(),
                                 "sexo": entry_sexo_nuevo.get()}}

        # Usar una transacción para actualizar los datos
        with client.start_session() as session:
            with session.start_transaction():
                collection.update_one(query, nuevos_datos, session=session)

        messagebox.showinfo("Información", "Registro actualizado exitosamente")

    # Ventana para la entrada de datos
    actualizar_ventana = tk.Toplevel(root)
    actualizar_ventana.title("Actualizar Registro")

    tk.Label(actualizar_ventana, text="Nombre Actual").pack()
    entry_nombre_actual = tk.Entry(actualizar_ventana)
    entry_nombre_actual.pack()

    tk.Label(actualizar_ventana, text="Nuevo Nombre").pack()
    entry_nombre_nuevo = tk.Entry(actualizar_ventana)
    entry_nombre_nuevo.pack()

    tk.Label(actualizar_ventana, text="Nueva Edad").pack()
    entry_edad_nueva = tk.Entry(actualizar_ventana)
    entry_edad_nueva.pack()

    tk.Label(actualizar_ventana, text="Nuevo Sexo").pack()
    entry_sexo_nuevo = tk.Entry(actualizar_ventana)
    entry_sexo_nuevo.pack()

    btn_guardar = tk.Button(actualizar_ventana, text="Guardar Cambios", command=guardar_cambios)
    btn_guardar.pack()

    pass


def eliminar_registro():
    def confirmar_eliminar():
        nombre = entry_nombre.get()

        # Usar una transacción para eliminar los datos
        with client.start_session() as session:
            with session.start_transaction():
                collection.delete_one({"nombre": nombre}, session=session)

        messagebox.showinfo("Información", "Registro eliminado exitosamente")

    # Ventana para la entrada de datos
    eliminar_ventana = tk.Toplevel(root)
    eliminar_ventana.title("Eliminar Registro")

    tk.Label(eliminar_ventana, text="Nombre").pack()
    entry_nombre = tk.Entry(eliminar_ventana)
    entry_nombre.pack()

    btn_eliminar = tk.Button(eliminar_ventana, text="Eliminar", command=confirmar_eliminar)
    btn_eliminar.pack()

    pass

# Botones en la pantalla de inicio
btn_crear = tk.Button(root, text="Crear", command=crear_registro)
btn_crear.pack()

btn_leer = tk.Button(root, text="Leer", command=leer_registros)
btn_leer.pack()

btn_actualizar = tk.Button(root, text="Actualizar", command=actualizar_registro)
btn_actualizar.pack()

btn_eliminar = tk.Button(root, text="Eliminar", command=eliminar_registro)
btn_eliminar.pack()

root.mainloop()

