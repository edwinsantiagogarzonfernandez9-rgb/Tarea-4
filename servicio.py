from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox

from excepciones import CedulaInvalidaError, CampoVacioError, CedulaDuplicadaError
from logger import registrar_log, guardar_servicio_en_log, cargar_servicios_desde_log


class Servicio: # Representa un servicio con nombre y precio
    def __init__(self, nombre, precio):
        self._nombre = nombre
        self._precio = precio

    @property
    def nombre(self): return self._nombre
    @property
    def precio(self): return self._precio


class ServicioApp(): # Aplicación principal para gestionar servicios
    def __init__(self):
        self.servicios = {}
        self.loop = tk.Tk()
        self.loop.title("Software FJ - Servicios")
        self.loop.geometry("400x400")
        self.loop.resizable(False, False)
        self.loop.configure(bg="#36506A")
        self.loop.attributes("-alpha", 0.95)

        tk.Button(self.loop, text="← Volver", font=("Arial", 10),
                  bg="#7A3535", fg="#FFFFFF", command=self.volver
                  ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        tk.Label(self.loop, text="Registro de Servicios",
                 font=("Arial", 20, "bold"), bg="#36506A", fg="#FFFFFF"
                 ).grid(row=1, column=0, columnspan=2, pady=20)

        tk.Label(self.loop, text="Nombre:", font=("Arial", 15),
                 bg="#36506A", fg="#FFFFFF").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.nombre_entry_entry = tk.Entry(self.loop, font=("Arial", 15), bg="#FFFFFF", fg="#000000")
        self.nombre_entry_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self.loop, text="Precio:", font=("Arial", 15),
                 bg="#36506A", fg="#FFFFFF").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.precio_entry = tk.Entry(self.loop, font=("Arial", 15), bg="#FFFFFF", fg="#000000")
        self.precio_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        tk.Button(self.loop, text="Registrar", font=("Arial", 15, "bold"),
                  bg="#455B46", fg="#FFFFFF", command=self.registrar_servicio
                  ).grid(row=4, column=1, pady=10)

        self.tabla = ttk.Treeview(self.loop,
                                  columns=("Nombre", "Precio"),
                                  show="headings")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Precio", text="Precio")
        self.tabla.column("Nombre",  width=180)
        self.tabla.column("Precio",  width=150)
        self.tabla.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self._cargar_servicios_guardados()
        self.loop.mainloop()

    def _cargar_servicios_guardados(self):# Carga los servicios guardados desde el log y los muestra en la tabla
        for nombre, precio in cargar_servicios_desde_log():
            try:
                servicio = (nombre, precio)
                self.servicios[nombre] = servicio
                self.tabla.insert("", END, values=servicio)
            except (CedulaInvalidaError, ValueError):
                pass

    def registrar_servicio(self):# Registra un nuevo servicio con el nombre y precio ingresados, lo agrega a la lista de servicios, lo muestra en la tabla y lo guarda en el log
        try:
            nombre = self.nombre_entry_entry.get().strip()
            precio = self.precio_entry.get().strip()

            if not nombre or not precio:
                raise CampoVacioError("Todos los campos son obligatorios.")

            if nombre in self.servicios:
                raise CedulaDuplicadaError(f"Ya existe un servicio con el nombre '{nombre}'.")

            if precio.count(".") > 1:
                raise ValueError("El precio no puede tener más de un punto decimal.")
            if not precio.replace(".", "", 1).isdigit() or float(precio) <= 0:
                raise ValueError("El precio debe ser un número positivo.")

            servicio = Servicio(nombre, float(precio))
            self.servicios[servicio.nombre] = servicio

            guardar_servicio_en_log(servicio.nombre, servicio.precio)
            registrar_log(f"Servicio registrado: {servicio.nombre} | {servicio.precio}")

            messagebox.showinfo("Éxito", "Servicio registrado exitosamente.")

            self.nombre_entry_entry.delete(0, END)
            self.precio_entry.delete(0, END)

            self.tabla.insert("", END, values=(servicio.nombre, servicio.precio))

        except (CampoVacioError, CedulaDuplicadaError, ValueError) as e:
            registrar_log(f"ERROR: {e}")
            messagebox.showerror("Error", str(e))

    def volver(self): # Cierra la ventana de servicios y vuelve al menú principal
        self.loop.destroy()
        from main import Main
        Main()


if __name__ == "__main__":
    app = ServicioApp()