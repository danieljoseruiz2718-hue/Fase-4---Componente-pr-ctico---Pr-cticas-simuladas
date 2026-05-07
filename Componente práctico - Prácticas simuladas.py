import logging
from abc import ABC, abstractmethod

# 1. CONFIGURACIÓN DE LOGS (Requisito Anexo 3) [cite: 18, 31]
logging.basicConfig(
    filename='registro_software_fj.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 2. EXCEPCIONES PERSONALIZADAS [cite: 17, 19]
class SoftwareFJError(Exception):
    """Clase base para excepciones del sistema."""
    pass

class DatosInvalidosError(SoftwareFJError):
    """Se lanza cuando los datos de entrada no cumplen las reglas."""
    pass

class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando un servicio no puede ser procesado."""
    pass

# 3. CLASES ABSTRACTAS Y ENCAPSULAMIENTO [cite: 21, 22, 23]
class EntidadGeneral(ABC):
    @abstractmethod
    def mostrar_identidad(self):
        pass

class Cliente(EntidadGeneral):
    def __init__(self, id_cliente, nombre, correo):
        # Encapsulamiento de datos personales 
        self.__id_cliente = id_cliente 
        self.nombre = nombre
        self.correo = correo

    def mostrar_identidad(self):
        return f"Cliente: {self.nombre} (ID: {self.__id_cliente})"

class Servicio(ABC):
    def __init__(self, nombre, costo_base):
        self.nombre = nombre
        self.costo_base = costo_base

    @abstractmethod
    def calcular_costo(self, cantidad, **kwargs):
        """Método para polimorfismo y sobrecarga [cite: 24, 26]"""
        pass

# 4. HERENCIA Y POLIMORFISMO: 3 SERVICIOS ESPECIALIZADOS 
class ReservaSala(Servicio):
    def calcular_costo(self, horas, es_vip=False):
        costo = self.costo_base * horas
        return costo * 0.9 if es_vip else costo # Descuento VIP

class AlquilerEquipo(Servicio):
    def calcular_costo(self, dias, seguro=True):
        costo = self.costo_base * dias
        return costo + 15000 if seguro else costo # Parámetro opcional

class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, sesiones):
        return self.costo_base * sesiones

# 5. CLASE RESERVA CON MANEJO AVANZADO DE EXCEPCIONES [cite: 25]
class Reserva:
    def __init__(self, cliente, servicio, cantidad):
        self.cliente = cliente
        self.servicio = servicio
        self.cantidad = cantidad

    def procesar(self):
        try:
            logging.info(f"Iniciando proceso para {self.cliente.nombre}")
            
            # Validación estricta [cite: 12, 19]
            if self.cantidad <= 0:
                raise DatosInvalidosError("La cantidad/duración debe ser mayor a cero.")
            
            costo_final = self.servicio.calcular_costo(self.cantidad)
            print(f"ÉXITO: Reserva de {self.servicio.nombre} para {self.cliente.nombre}. Total: ${costo_final}")
            logging.info(f"Reserva exitosa: {self.servicio.nombre} - Costo: {costo_final}")

        except DatosInvalidosError as e:
            # Encadenamiento de excepciones [cite: 17]
            logging.error(f"Error de datos: {e}")
            print(f"ERROR CONTROLADO: {e}")
            raise SoftwareFJError("No se pudo completar la reserva por datos inconsistentes.") from e
            
        except Exception as e:
            logging.error(f"Error inesperado: {e}")
            print("ERROR TÉCNICO: El sistema ha sido estabilizado.")
            
        finally:
            # Garantiza la estabilidad del sistema [cite: 11, 17]
            print("Finalizando trámite de operación.\n")

# 6. SIMULACIÓN DE 10 OPERACIONES (Válidas e Inválidas) [cite: 32]
def ejecutar_simulacion():
    print("--- INICIANDO SISTEMA SOFTWARE FJ ---\n")
    
    # Datos iniciales
    c1 = Cliente("001", "Daniel", "dan@mail.com")
    c2 = Cliente("002", "Natasha", "nat@mail.com")
    
    s1 = ReservaSala("Sala A", 50000)
    s2 = AlquilerEquipo("Laptop", 25000)
    s3 = AsesoriaEspecializada("Asesoría Java", 80000)

    operaciones = [
        (c1, s1, 3),   # 1. Válida
        (c2, s2, -1),  # 2. Inválida (Cantidad negativa)
        (c1, s3, 2),   # 3. Válida
        (None, s1, 1), # 4. Inválida (Sin cliente - Error grave)
        (c2, s1, 5),   # 5. Válida
        (c1, s2, 0),   # 6. Inválida (Cantidad cero)
        (c2, s3, 4),   # 7. Válida
        (c1, s1, 10),  # 8. Válida
        (c2, s2, 2),   # 9. Válida
        (c1, s3, 1),   # 10. Válida
    ]

    for cliente, servicio, cantidad in operaciones:
        try:
            reserva = Reserva(cliente, servicio, cantidad)
            reserva.procesar()
        except Exception:
            # El programa continúa funcionando a pesar de errores graves [cite: 32]
            continue

if __name__ == "__main__":
    ejecutar_simulacion()