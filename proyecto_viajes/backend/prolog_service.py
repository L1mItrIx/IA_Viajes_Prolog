
# Conexion con Prolog - pasa el perfil del usuario dinamicamente

import subprocess
import os
from typing import List, Dict
from models import PerfilViajero

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVO_PROLOG = os.path.join(BASE_DIR, 'prolog', 'destinos.pl')
SWIPL_BIN = os.getenv('SWIPL_PATH', 'swipl')

def limpiar_texto(texto: str) -> str:
    return (texto.strip().lower()
        .replace(" ", "_")
        .replace("á", "a").replace("é", "e").replace("í", "i")
        .replace("ó", "o").replace("ú", "u").replace("ñ", "n")
        .replace("Á", "a").replace("É", "e").replace("Í", "i")
        .replace("Ó", "o").replace("Ú", "u"))

def construir_goal(perfil: PerfilViajero, consulta: str) -> str:
    limpiar = (
        "retractall(visitado(_)), "
        "retractall(continente_visitado(_)), "
        "retractall(gusto(_)), "
        "retractall(presupuesto_usuario(_)), "
        "retractall(clima_preferido(_)), "
        "retractall(tipoviaje_preferido(_))"
    )

    nuevos = []

    for p in perfil.paises_visitados:
        nuevos.append(f"assert(visitado({limpiar_texto(p)}))")

    for c in perfil.continentes_visitados:
        nuevos.append(f"assert(continente_visitado({limpiar_texto(c)}))")

    for g in perfil.gustos:
        nuevos.append(f"assert(gusto({limpiar_texto(g)}))")

    nuevos.append(f"assert(presupuesto_usuario({limpiar_texto(perfil.presupuesto)}))")
    nuevos.append(f"assert(clima_preferido({limpiar_texto(perfil.clima_preferido)}))")
    nuevos.append(f"assert(tipoviaje_preferido({limpiar_texto(perfil.tipo_viaje)}))")

    hechos = ", ".join(nuevos)
    return f"{limpiar}, {hechos}, {consulta}"


def obtener_recomendados(perfil: PerfilViajero) -> List[str]:
    try:
        goal = construir_goal(perfil, "findall(D, recomendado(D), L0), sort(L0, L), write(L), nl, halt.")
        comando = [SWIPL_BIN, '-s', ARCHIVO_PROLOG, '-g', goal]
        resultado = subprocess.run(comando, capture_output=True, text=True, timeout=15)

        print(f"SWI retorno: {resultado.returncode}")
        print(f"STDOUT: {resultado.stdout}")
        if resultado.stderr.strip():
            print(f"STDERR: {resultado.stderr}")

        if resultado.stdout.strip():
            texto = resultado.stdout.strip().strip('[]')
            return [p.strip().strip("'") for p in texto.split(',') if p.strip()]
        return []
    except Exception as e:
        print(f"Error recomendados: {e}")
        return []


def obtener_diferentes(perfil: PerfilViajero) -> List[str]:
    try:
        goal = construir_goal(perfil, "findall(D, destino_diferente(D), L0), sort(L0, L), write(L), nl, halt.")
        comando = [SWIPL_BIN, '-s', ARCHIVO_PROLOG, '-g', goal]
        resultado = subprocess.run(comando, capture_output=True, text=True, timeout=15)

        if resultado.stderr.strip():
            print(f"STDERR diferentes: {resultado.stderr}")

        if resultado.stdout.strip():
            texto = resultado.stdout.strip().strip('[]')
            return [p.strip().strip("'") for p in texto.split(',') if p.strip()]
        return []
    except Exception as e:
        print(f"Error diferentes: {e}")
        return []


def consultar_prolog(perfil: PerfilViajero) -> Dict:
    print(f"\n--- Consultando Prolog para: {perfil.nombre} ---")
    print(f"Visitados: {perfil.paises_visitados}")
    print(f"Presupuesto: {perfil.presupuesto} | Clima: {perfil.clima_preferido} | Tipo: {perfil.tipo_viaje}")
    print(f"Gustos: {perfil.gustos}")

    recomendados = obtener_recomendados(perfil)
    diferentes = obtener_diferentes(perfil)

    print(f"Recomendados finales: {recomendados}")

    return {
        "exito": True,
        "recomendados": recomendados[:5],
        "diferentes": diferentes[:3]
    }