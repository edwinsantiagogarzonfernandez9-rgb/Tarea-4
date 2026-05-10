from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from excepciones import CedulaInvalidaError, CampoVacioError, CedulaDuplicadaError, ClienteError
from logger import registrar_log, guardar_cliente_en_log, cargar_clientes_desde_log


class Cliente:
    def __init__(self, cedula, nombre, telefono):
        self._cedula   = self._validar_cedula(cedula)
        self._nombre   = nombre.strip()
        self._telefono = telefono.strip()

    def _validar_cedula(self, v):
        v = v.strip()
        if len(v) < 5:
            raise CedulaInvalidaError("La cédula debe tener al menos 5 caracteres.")
        return v

    @property
    def cedula(self):    return self._cedula
    @property
    def nombre(self):    return self._nombre
    @property
    def telefono(self):  return self._telefono

    def fila(self):
        return (self._cedula, self._nombre, self._telefono)


class Repositorio:
    def __init__(self):
        self._datos: dict[str, Cliente] = {}

    def agregar(self, c: Cliente):
        if c.cedula in self._datos:
            raise CedulaDuplicadaError(f"Ya existe un cliente con cédula {c.cedula}.")
        self._datos[c.cedula] = c

    def eliminar(self, cedula: str):
        if cedula not in self._datos:
            raise ClienteError("Cliente no encontrado.")
        del self._datos[cedula]

    def contiene(self, cedula: str) -> bool:
        return cedula in self._datos


class ClienteApp():
    def __init__(self):
        self.repositorio = Repositorio()

        self.loop = tk.Tk()
        self.loop.title("Software FJ - Clientes")
        self.loop.geometry("500x400")
        self.loop.resizable(False, False)
        self.loop.configure(bg="#36506A")
        self.loop.attributes("-alpha", 0.95)

        tk.Button(self.loop, text="← Volver", font=("Arial", 10),
                  bg="#7A3535", fg="#FFFFFF", command=self.volver
                  ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        tk.Label(self.loop, text="Registro de Clientes",
                 font=("Arial", 18, "bold"), bg="#36506A", fg="#FFFFFF"
                 ).grid(row=1, column=0, columnspan=2, pady=20)

        tk.Label(self.loop, text="Cédula:", font=("Arial", 15),
                 bg="#36506A", fg="#FFFFFF").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.cedula_entry = tk.Entry(self.loop, font=("Arial", 15), bg="#FFFFFF", fg="#000000")
        self.cedula_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self.loop, text="Nombre:", font=("Arial", 15),
                 bg="#36506A", fg="#FFFFFF").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.nombre_entry = tk.Entry(self.loop, font=("Arial", 15), bg="#FFFFFF", fg="#000000")
        self.nombre_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self.loop, text="Teléfono:", font=("Arial", 15),
                 bg="#36506A", fg="#FFFFFF").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.telefono_entry = tk.Entry(self.loop, font=("Arial", 15), bg="#FFFFFF", fg="#000000")
        self.telefono_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        tk.Button(self.loop, text="Registrar", font=("Arial", 10, "bold"),
                  bg="#455B46", fg="#FFFFFF", command=self.registrar_cliente
                  ).grid(row=5, column=1, pady=10)

        self.tabla = ttk.Treeview(self.loop,
                                  columns=("Cédula", "Nombre", "Teléfono"),
                                  show="headings")
        self.tabla.heading("Cédula",   text="Cédula")
        self.tabla.heading("Nombre",   text="Nombre")
        self.tabla.heading("Teléfono", text="Teléfono")
        self.tabla.column("Cédula",   width=150)
        self.tabla.column("Nombre",   width=180)
        self.tabla.column("Teléfono", width=150)
        self.tabla.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self._cargar_clientes_guardados()
        self.loop.mainloop()

    def _cargar_clientes_guardados(self):
        for cedula, nombre, telefono in cargar_clientes_desde_log():
            try:
                cliente = Cliente(cedula, nombre, telefono)
                self.repositorio.agregar(cliente)
                self.tabla.insert("", END, values=cliente.fila())
            except (CedulaInvalidaError, CedulaDuplicadaError):
                pass

    def registrar_cliente(self):
        try:
            cedula   = self.cedula_entry.get().strip()
            nombre   = self.nombre_entry.get().strip()
            telefono = self.telefono_entry.get().strip()

            if not cedula or not nombre or not telefono:
                raise CampoVacioError("Todos los campos son obligatorios.")

            if self.repositorio.contiene(cedula):
                raise CedulaDuplicadaError(f"Ya existe un cliente con cédula {cedula}.")

            cliente = Cliente(cedula, nombre, telefono)
            self.repositorio.agregar(cliente)

            guardar_cliente_en_log(cliente.cedula, cliente.nombre, cliente.telefono)
            registrar_log(f"Cliente registrado: {cliente.cedula} | {cliente.nombre} | {cliente.telefono}")

            messagebox.showinfo("Éxito", "Cliente registrado exitosamente.")

            self.cedula_entry.delete(0, END)
            self.nombre_entry.delete(0, END)
            self.telefono_entry.delete(0, END)

            self.tabla.insert("", END, values=cliente.fila())

        except (CedulaInvalidaError, CampoVacioError, CedulaDuplicadaError) as e:
            registrar_log(f"ERROR: {e}")
            messagebox.showerror("Error", str(e))

    def volver(self):
        self.loop.destroy()
        from main import Main  
        Main()


if __name__ == "__main__":
    app = ClienteApp()