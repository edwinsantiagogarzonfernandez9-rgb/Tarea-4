from datetime import datetime
import os

log_file = os.path.join(os.path.dirname(__file__), "logs.txt")


def registrar_log(mensaje: str):
    hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{hora}] {mensaje}\n")


def guardar_cliente_en_log(cedula, nombre, telefono):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"DATO|{cedula}|{nombre}|{telefono}\n")
def guardar_servicio_en_log(nombre, precio):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"SERVICIO|{nombre}|{precio}\n")


def cargar_clientes_desde_log():
    if not os.path.exists(log_file):
        return []
    clientes = []
    vistos = set()
    with open(log_file, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if linea.startswith("DATO|"):
                partes = linea.split("|")
                if len(partes) == 4:
                    _, cedula, nombre, telefono = partes
                    if cedula not in vistos:
                        vistos.add(cedula)
                        clientes.append((cedula, nombre, telefono))
    return clientes
def cargar_servicios_desde_log():
    if not os.path.exists(log_file):
        return []
    servicios = []
    vistos = set()
    with open(log_file, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if linea.startswith("SERVICIO|"):
                partes = linea.split("|")
                if len(partes) == 3:
                    _, nombre, precio = partes
                    if nombre not in vistos:
                        vistos.add(nombre)
                        servicios.append((nombre, precio))
    return servicios