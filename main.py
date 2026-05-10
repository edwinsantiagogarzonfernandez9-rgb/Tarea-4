from tkinter import *
import tkinter as tk
from cliente import ClienteApp
from servicio import ServicioApp
from reserva import ReservaApp
class Main():
    def __init__(self):
        self.loop = tk.Tk()
        self.loop.title("Software FJ")
        self.loop.geometry("400x310")
        self.loop.resizable(False, False)
        self.loop.configure(bg="#36506A")
        self.loop.attributes("-alpha", 0.95)
        tk.Label(self.loop, text="Software FJ",
                 font=("Segoe UI", 18, "bold"), bg="#36506A", fg="#FFFFFF"
                 ).pack(pady=(30, 5))
        tk.Label(self.loop, text="Sistema de Gestión",
                 font=("Segoe UI", 10), bg="#36506A", fg="#AECBD6"
                 ).pack(pady=(0, 25))
        tk.Button(self.loop, text="👤  Clientes",
                  font=("Segoe UI", 11, "bold"),
                  bg="#455B46", fg="#FFFFFF",
                  width=18, cursor="hand2",
                  command=self.abrir_clientes
                  ).pack(pady=6)
        tk.Button(self.loop, text="🔧  Servicios",
                  font=("Segoe UI", 11, "bold"),
                  bg="#455B46", fg="#FFFFFF",
                  width=18, cursor="hand2",
                  command=self.abrir_servicios
                  ).pack(pady=6)
        tk.Button(self.loop, text="📅  Reservas",
                  font=("Segoe UI", 11, "bold"),
                  bg="#455B46", fg="#FFFFFF",
                  width=18, cursor="hand2",
                  command=self.abrir_reservas
                  ).pack(pady=6)
        tk.Button(self.loop, text="✖  Salir",
                  font=("Segoe UI", 10),
                  bg="#7A3535", fg="#FFFFFF",
                  width=18, cursor="hand2",
                  command=self.loop.destroy
                  ).pack(pady=6)
        self.loop.mainloop()
    def abrir_clientes(self):
        self.loop.destroy()
        ClienteApp()

    def abrir_servicios(self):
        self.loop.destroy()
        ServicioApp()

    def abrir_reservas(self):
        self.loop.destroy()
        ReservaApp()
if __name__ == "__main__":
    app = Main()