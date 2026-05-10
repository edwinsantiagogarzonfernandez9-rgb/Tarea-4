class ClienteError(Exception):
    """Excepción base para errores del módulo de clientes."""
    pass
class CampoVacioError(ClienteError):
    """Se lanza cuando un campo obligatorio está vacío."""
    pass
class CedulaInvalidaError(ClienteError):
    """Se lanza cuando la cédula no cumple los requisitos mínimos."""
    pass
class CedulaDuplicadaError(ClienteError):
    """Se lanza cuando ya existe un cliente con la misma cédula."""
    pass
class ReservaError(Exception):
    """Excepción base para errores del módulo de reservas."""
    pass
class ReservaCanceladaError(ReservaError):
    """Se lanza cuando se intenta procesar una reserva que ha sido cancelada."""
    pass
class CostoInvalidoError(ReservaError):
    """Se lanza cuando el costo calculado es negativo o no tiene sentido."""
    pass
