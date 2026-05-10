from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from excepciones import ReservaCanceladaError, CostoInvalidoError, ReservaError
from logger import registrar_log, cargar_servicios_desde_log, cargar_clientes_desde_log


class Reserva:
    def __init__(self, servicio, cantidad,cliente=None):
        self._servicio = servicio
        self._cantidad = cantidad
        self._cliente = cliente
    @property
    def servicio(self): return self._servicio
    @property
    def cantidad(self): return self._cantidad
    @property
    def cliente(self): return self._cliente
class ReservaApp():
    def __init__(self):
        self.reservas = []

        self.loop = tk.Tk()
        self.loop.title("Gestión de Reservas")
        self.loop.geometry("500x500")
        self.loop.resizable(False, False)
        self.loop.configure(bg="#36506A")
        self.loop.attributes("-alpha", 0.95)

        tk.Button(self.loop, text="← Volver", font=("Segoe UI", 10),
                  bg="#7A3535", fg="#FFFFFF", command=self.volver
                  ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        tk.Label(self.loop, text="Gestión de Reservas",
                 font=("Arial", 18, "bold"), bg="#36506A", fg="#FFFFFF"
                 ).grid(row=1, column=0, columnspan=2, pady=20)

        # ── Servicio (cargado desde logs.txt) ──────────────
        tk.Label(self.loop, text="Servicio:", font=("Arial", 15),
                 bg="#36506A", fg="#FFFFFF"
                 ).grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self._servicios = cargar_servicios_desde_log()   # [(nombre, precio), ...]
        nombres = [s[0] for s in self._servicios]

        self.servicio_var = tk.StringVar()

        if nombres:
            self.servicio_var.set(nombres[0])
        else:
            self.servicio_var.set("Sin servicios registrados")
            nombres = ["Sin servicios registrados"]

        self.servicio_option = tk.OptionMenu(self.loop, self.servicio_var, *nombres)
        self.servicio_option.config(font=("Arial", 12), bg="#FFFFFF", fg="#000000", width=20)
        self.servicio_option.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        # ───────────────────────────────────────────────────

        tk.Label(self.loop, text="Cantidad:", font=("Arial", 15),
                 bg="#36506A", fg="#FFFFFF").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.cantidad_entry = tk.Entry(self.loop, font=("Arial", 15), bg="#FFFFFF", fg="#000000")
        self.cantidad_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        tk.Label(self.loop, text="Cliente:", font=("Arial", 15), bg="#36506A", fg="#FFFFFF"
                 ).grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self._clientes = cargar_clientes_desde_log()   
        nombres = [c[1] for c in self._clientes]

        self.cliente_var = tk.StringVar()

        if nombres:
            self.cliente_var.set(nombres[0])
        else:
            self.cliente_var.set("Sin clientes registrados")
            nombres = ["Sin clientes registrados"]

        self.cliente_option = tk.OptionMenu(self.loop, self.cliente_var, *nombres)
        self.cliente_option.config(font=("Arial", 12), bg="#FFFFFF", fg="#000000", width=20)
        self.cliente_option.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        tk.Button(self.loop, text="Crear Reserva", font=("Arial", 10, "bold"),
                  bg="#455B46", fg="#FFFFFF", command=self.crear_reserva
                  ).grid(row=5, column=1, pady=10)

        # ── Tabla de reservas ───────────────────────────────
        self.tabla = ttk.Treeview(self.loop,
                                  columns=("Servicio", "Cantidad", "Cliente", "Estado"),
                                  show="headings")
        self.tabla.heading("Servicio",  text="Servicio")
        self.tabla.heading("Cantidad",  text="Cantidad")
        self.tabla.heading("Cliente",   text="Cliente")
        self.tabla.column("Servicio",   width=100)
        self.tabla.column("Cantidad",   width=100)
        self.tabla.column("Cliente",    width=100)
        self.tabla.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.loop.mainloop()

    def crear_reserva(self):
        try:
            servicio_nombre = self.servicio_var.get()
            cantidad_str = self.cantidad_entry.get()
            cliente_nombre = self.cliente_var.get()

            if servicio_nombre == "Sin servicios registrados":
                raise ReservaError("No hay servicios disponibles para reservar.")
            if cliente_nombre == "Sin clientes registrados":
                raise ReservaError("No hay clientes disponibles para asociar a la reserva.")
            if not cantidad_str.strip():
                raise ReservaError("La cantidad no puede estar vacía.")
            if not cantidad_str.isdigit() or int(cantidad_str) <= 0:
                raise ReservaError("La cantidad debe ser un número entero positivo.")

            cantidad = int(cantidad_str)

            reserva = Reserva(servicio_nombre, cantidad, cliente_nombre)
            self.reservas.append(reserva)

            self.tabla.insert("", "end", values=(reserva.servicio, reserva.cantidad, reserva.cliente))
            registrar_log(f"Reserva creada: Servicio='{reserva.servicio}', Cantidad={reserva.cantidad}, Cliente='{reserva.cliente}'")

        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero.")
        except ReservaError as e:
            registrar_log(f"ERROR ReservaError: {e}")
            messagebox.showerror("Error", str(e))
        except ReservaCanceladaError as e:
            registrar_log(f"ERROR ReservaCancelada: {e}")
            messagebox.showerror("Error", str(e))

    def volver(self):
        self.loop.destroy()
        from main import Main
        Main()


if __name__ == "__main__":
    app = ReservaApp()
