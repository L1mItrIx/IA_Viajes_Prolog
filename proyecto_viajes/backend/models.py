# Berny Cordero Cerdas
# Clases para guardar los datos del usuario y las recomendaciones

from dataclasses import dataclass
from typing import List

@dataclass
class PerfilViajero:
    nombre: str
    paises_visitados: List[str]
    continentes_visitados: List[str]
    presupuesto: str
    clima_preferido: str
    gustos: List[str]
    tipo_viaje: str

@dataclass
class Recomendacion:
    pais: str
    razon: str
    orden: int