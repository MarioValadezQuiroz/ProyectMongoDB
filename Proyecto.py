#Cometar el apartado de seguridad del .cfg
#Descomentar el apartado de Replica Set
#Para ejecutar el codigo es necesario tener al menos un nodo Replica Set activo.

#Importamos Librerias
import pymongo
import tkinter as tk
from tkinter import messagebox

# Conexión a la base de datos MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
# Conexión a MongoDB con autenticación
#client = pymongo.MongoClient("mongodb://adminUser:adminPassword@localhost:27017/?authSource=admin")

#Base de datos y Coleccion
db = client["Proyecto3"]
collection = db["users"]

#Interfaz del Programa
# Crear la ventana principal
root = tk.Tk()
root.title("Gestión de Datos")
root.geometry("400x400")

#Funciones validaciones
def solo_letras(char):
    if char.isalpha() or char == " ": #Verifica si existen letras o espacios
        return True
    else:
        #Crear una ventana bloqueadora
        bloqueador = tk.Toplevel(root)
        bloqueador.withdraw()
        bloqueador.grab_set()

        messagebox.showerror("Error de entrada", "Sólo se permiten letras")

        #Liberar el bloqueo una vez se cierre el messagebox
        bloqueador.grab_release()
        bloqueador.destroy()
        return False

def solo_numeros(char):
    if char.isdigit() or char == " ": #Verifica si existen letras o espacios
        return True
    else:
        #Crear una ventana bloqueadora
        bloqueador = tk.Toplevel(root)
        bloqueador.withdraw()
        bloqueador.grab_set()

        messagebox.showerror("Error de entrada", "Sólo se permiten números")

        # Liberar el bloqueo una vez se cierre el messagebox
        bloqueador.grab_release()
        bloqueador.destroy()
        return False

# Funciones CRUD
def crear_registro():
    def guardar_datos():
        nombre = entry_nombre.get().strip()
        apellido = entry_apellido.get().strip()
        edad = entry_edad.get().strip()
        sexo = entry_sexo.get().strip()
        correo = entry_correo.get().strip()
        telefono = entry_telefono.get().strip()

        #Validación de campos vacíos
        if not entry.get():
            bloqueador = tk.Toplevel(root)
            bloqueador.withdraw()
            bloqueador.grab_set()
            messagebox.showerror("Error de entrada", "Todos los campos son obligatorios")
            bloqueador.grab_release()
            bloqueador.destroy()
            return

        try:
            # Usar una transacción para guardar los datos
            with client.start_session() as session:
                with session.start_transaction():
                    collection.insert_one({"nombre": nombre,
                                           "apellido": apellido,
                                           "edad": edad,
                                           "sexo": sexo,
                                           "correo": correo,
                                           "telefono": telefono},
                                          session=session)
            messagebox.showinfo("Información", "Registro creado exitosamente")
            crear_ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear registro: {e}")

    # Ventana para la entrada de datos
    crear_ventana = tk.Toplevel(root)
    crear_ventana.title("Crear Registro")
    crear_ventana.transient(root)  # La ventana modal se muestra frente a la ventana principal
    crear_ventana.grab_set() #La ventana no permite interacción con otras ventanas hasta que sea cerrada

    campos = ["Nombre", "Apellido", "Edad", "Sexo", "Correo", "Teléfono"]
    entradas = []

    for campo in campos:
        tk.Label(crear_ventana, text=campo).pack()
        entry = tk.Entry(crear_ventana)
        entry.pack()
        entradas.append(entry)

    entry_nombre, entry_apellido, entry_edad, entry_sexo, entry_correo, entry_telefono = entradas

    #Declaración de las funciones para validar
    vcmd = root.register(solo_letras)
    vcmd2 = root.register(solo_numeros)
    
    #Referencia de las funciones de validación hacia cada campo, así como eliminación de caracteres no permitidos
    entry_nombre.config(validate="key", validatecommand=(vcmd, '%S'))
    entry_apellido.config(validate="key", validatecommand=(vcmd, '%S'))
    entry_sexo.config(validate="key", validatecommand=(vcmd, '%S'))
    entry_edad.config(validate="key", validatecommand=(vcmd2, '%S'))
    entry_telefono.config(validate="key", validatecommand=(vcmd2, '%S'))


    #Referencia y asignación de la función de guardar datos al botón de guardar 
    btn_guardar = tk.Button(crear_ventana, text="Guardar", command=guardar_datos)
    btn_guardar.pack()

def leer_registros():
    # Ventana para mostrar los registros
    leer_ventana = tk.Toplevel(root)
    leer_ventana.title("Leer Registros")
    leer_ventana.transient(root)  # La ventana modal se muestra frente a la ventana principal
    leer_ventana.grab_set() #La ventana no permite interacción con otras ventanas hasta que sea cerrada

    registros = collection.find()

    for registro in registros:
        tk.Label(leer_ventana, text=f"Nombre: {registro['nombre']}, "
                                    f"Apellido: {registro['apellido']}, "
                                    f"Edad: {registro['edad']}, "
                                    f"Sexo: {registro['sexo']}, "
                                    f"Correo: {registro['correo']}, "
                                    f"Teléfono: {registro['telefono']}").pack()

def actualizar_registro():
    def guardar_cambios():
        query = {"nombre": entry_nombre_actual.get()}
        nuevos_datos = {"$set": {"nombre": entry_nombre_nuevo.get(),
                                 "apellido": entry_apellido_nuevo.get(),
                                 "edad": entry_edad_nueva.get(),
                                 "sexo": entry_sexo_nuevo.get(),
                                 "correo": entry_correo_nuevo.get(),
                                 "telefono": entry_telefono_nuevo.get()}}

        try:
            # Usar una transacción para actualizar los datos
            with client.start_session() as session:
                with session.start_transaction():
                    collection.update_one(query, nuevos_datos, session=session)
            messagebox.showinfo("Información", "Registro actualizado exitosamente")
            actualizar_ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar registro: {e}")

    # Ventana para la entrada de datos
    actualizar_ventana = tk.Toplevel(root)
    actualizar_ventana.title("Actualizar Registro")
    actualizar_ventana.transient(root)  # La ventana modal se muestra frente a la ventana principal
    actualizar_ventana.grab_set() #La ventana no permite interacción con otras ventanas hasta que sea cerrada

    campos = [("Nombre Actual", "Nuevo Nombre"),
              ("Nuevo Apellido", "Nueva Edad"),
              ("Nuevo Sexo", "Nuevo Correo"),
              ("Nuevo Teléfono", )]
    entradas = []

    for par in campos:
        for campo in par:
            tk.Label(actualizar_ventana, text=campo).pack()
            entry = tk.Entry(actualizar_ventana)
            entry.pack()
            entradas.append(entry)

    (entry_nombre_actual, entry_nombre_nuevo,
     entry_apellido_nuevo, entry_edad_nueva,
     entry_sexo_nuevo, entry_correo_nuevo,
     entry_telefono_nuevo) = entradas

    btn_guardar = tk.Button(actualizar_ventana, text="Guardar Cambios", command=guardar_cambios)
    btn_guardar.pack()

def eliminar_registro():
    def confirmar_eliminar():
        nombre = entry_nombre.get()

        try:
            # Usar una transacción para eliminar los datos
            with client.start_session() as session:
                with session.start_transaction():
                    collection.delete_one({"nombre": nombre}, session=session)
            messagebox.showinfo("Información", "Registro eliminado exitosamente")
            eliminar_ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar registro: {e}")

    # Ventana para la entrada de datos
    eliminar_ventana = tk.Toplevel(root)
    eliminar_ventana.title("Eliminar Registro")
    eliminar_ventana.transient(root)  # La ventana modal se muestra frente a la ventana principal
    eliminar_ventana.grab_set() #La ventana no permite interacción con otras ventanas hasta que sea cerrada

    tk.Label(eliminar_ventana, text="Nombre").pack()
    entry_nombre = tk.Entry(eliminar_ventana)
    entry_nombre.pack()

    btn_eliminar = tk.Button(eliminar_ventana, text="Eliminar", command=confirmar_eliminar)
    btn_eliminar.pack()

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

