class ClienteError(Exception): # Excepción base para errores del módulo de clientes
    """Excepción base para errores del módulo de clientes."""
    pass
class CampoVacioError(ClienteError): # Excepción para campos vacíos
    """Se lanza cuando un campo obligatorio está vacío."""
    pass
class CedulaInvalidaError(ClienteError): # Excepción para cédulas inválidas
    """Se lanza cuando la cédula no cumple los requisitos mínimos."""
    pass
class CedulaDuplicadaError(ClienteError): # Excepción para cédulas duplicadas
    """Se lanza cuando ya existe un cliente con la misma cédula."""
    pass
class ReservaError(Exception): # Excepción base para errores del módulo de reservas
    """Excepción base para errores del módulo de reservas."""
    pass
class ReservaCanceladaError(ReservaError): # Excepción para reservas canceladas
    """Se lanza cuando se intenta procesar una reserva que ha sido cancelada."""
    pass
class CostoInvalidoError(ReservaError): # Excepción para costos inválidos
    """Se lanza cuando el costo calculado es negativo o no tiene sentido."""
    pass
