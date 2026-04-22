
# Este modulo genera las explicaciones para cada pais recomendado
# La IA generativa se consume desde ai_service.py.

from typing import List, Dict
from ai_service import generar_texto
from models import PerfilViajero, Recomendacion

INFO_PAISES = {
    "nicaragua":     "tiene mucha naturaleza, volcanes y es muy accesible",
    "guatemala":     "tiene cultura maya e historia colonial muy interesante",
    "honduras":      "tiene arrecifes de coral y playas tropicales",
    "el_salvador":   "tiene playas bonitas y aventura accesible",
    "belice":        "tiene naturaleza unica y ecoturismo de calidad",
    "tailandia":     "es famoso por gastronomia, templos y playas",
    "vietnam":       "tiene historia fascinante y paisajes muy bonitos",
    "indonesia":     "tiene islas tropicales con mucha naturaleza",
    "india":         "tiene historia antigua y gastronomia muy variada",
    "malasia":       "tiene selvas tropicales y ecoturismo accesible",
    "kenia":         "tiene safaris y fauna africana unica",
    "tanzania":      "tiene parques naturales y aventura increible",
    "marruecos":     "tiene desierto del Sahara y cultura arabe",
    "egipto":        "tiene las piramides y civilizacion milenaria",
    "espana":        "tiene historia, gastronomia y vida nocturna",
    "portugal":      "tiene historia de navegacion y gastronomia rica",
    "grecia":        "tiene historia clasica y playas del mediterraneo",
    "japon":         "mezcla tecnologia avanzada con cultura antigua",
    "china":         "tiene la Gran Muralla y mucha historia imperial",
    "peru":          "tiene Machu Picchu y la cultura inca",
    "colombia":      "tiene biodiversidad tropical y cultura vibrante",
    "brasil":        "tiene carnaval, playas famosas y la amazonia",
    "australia":     "tiene fauna unica y mucha naturaleza salvaje",
}


def normalizar_texto_ia(texto: str) -> str:
    limpio = " ".join(texto.strip().split())

    for prefijo in ["hola", "¡hola", "estimada", "estimado", "querido", "querida"]:
        if limpio.lower().startswith(prefijo):
            partes = limpio.split(" ", 1)
            limpio = partes[1] if len(partes) > 1 else limpio
            break

    oraciones = [o.strip() for o in limpio.replace("!", ".").split(".") if o.strip()]
    if len(oraciones) > 2:
        limpio = ". ".join(oraciones[:2]) + "."

    return limpio

def generar_explicacion(pais: str, perfil: PerfilViajero, numero: int) -> str:
    descripcion = INFO_PAISES.get(pais, "es un destino con experiencias unicas")
    nombre_pais = pais.replace("_", " ").title()
    gustos = " y ".join(perfil.gustos[:2]) if perfil.gustos else "nuevas experiencias"

    prompt = (
        "Eres un asistente de viajes. Redacta SOLO 2 oraciones en espanol. "
        "No uses saludos, no uses exclamaciones, no uses listas, no inventes datos. "
        "Primera oracion: describe el destino y su valor principal. "
        "Segunda oracion: debe iniciar exactamente con 'Prolog lo recomienda' y justificar por perfil. "
        f"Destino: {nombre_pais}. "
        f"Descripcion base: {descripcion}. "
        f"Perfil del viajero: nombre={perfil.nombre}, presupuesto={perfil.presupuesto}, "
        f"clima={perfil.clima_preferido}, gustos={', '.join(perfil.gustos) if perfil.gustos else 'nuevas experiencias'}, "
        f"tipo_viaje={perfil.tipo_viaje}, numero_recomendacion={numero}. "
        f"La justificacion debe decir por que encaja con {gustos}, presupuesto y clima."
    )

    texto_ia = generar_texto(prompt)
    if texto_ia:
        texto_ia = normalizar_texto_ia(texto_ia)
        if "prolog lo recomienda" not in texto_ia.lower():
            texto_ia += (
                f" Prolog lo recomienda para {perfil.nombre} porque encaja con su interes en {gustos}, "
                f"su presupuesto {perfil.presupuesto} y su clima preferido {perfil.clima_preferido}."
            )
        return texto_ia

    return (
        f"{nombre_pais} {descripcion}. "
        f"Prolog lo recomendo para {perfil.nombre} porque coincide con "
        f"su interes en {gustos}, su presupuesto {perfil.presupuesto} "
        f"y su preferencia de clima {perfil.clima_preferido}. "
        f"Ademas este pais no esta en su historial de viajes."
    )

def generar_plan(perfil: PerfilViajero, resultado: Dict) -> List[Recomendacion]:
    plan = []
    for i, pais in enumerate(resultado.get("recomendados", []), start=1):
        explicacion = generar_explicacion(pais, perfil, i)
        plan.append(Recomendacion(pais=pais, razon=explicacion, orden=i))
    return plan

def mostrar_plan(plan: List[Recomendacion], perfil: PerfilViajero):
    print("\n" + "="*55)
    print(f"  PLAN DE VIAJE PARA: {perfil.nombre.upper()}")
    print("="*55)
    print(f"  Presupuesto: {perfil.presupuesto}")
    print(f"  Clima preferido: {perfil.clima_preferido}")
    print(f"  Gustos: {', '.join(perfil.gustos)}")
    print("="*55)

    if not plan:
        print("\n  No se encontraron destinos con esos criterios.")
        return

    print(f"\n  Prolog encontro {len(plan)} destinos recomendados:\n")
    for rec in plan:
        nombre = rec.pais.replace("_", " ").title()
        print(f"  {rec.orden}. {nombre}")
        print(f"     {rec.razon}")
        print()

    print("="*55)
    print("  IA: local (costo $0) | Motor: SWI-Prolog 10.0.2")
    print("="*55)