# Berny Cordero Cerdas
# Aplicacion principal con FastAPI

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from html import escape
from models import PerfilViajero
from prolog_service import consultar_prolog
from plan_service import generar_plan

app = FastAPI(title="Asistente de Planificacion de Viajes")

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def render_template(template_name: str, context: dict[str, str] | None = None) -> str:
    template_path = TEMPLATES_DIR / template_name
    contenido = template_path.read_text(encoding="utf-8")

    for key, value in (context or {}).items():
        contenido = contenido.replace(f"{{{{{key}}}}}", value)

    return contenido


@app.get("/", response_class=HTMLResponse)
def pagina_principal():
    return render_template("index.html")


@app.post("/plan", response_class=HTMLResponse)
async def generar_plan_viaje(
    nombre: str = Form(...),
    paises_visitados: str = Form(""),
    continentes_visitados: str = Form("america"),
    presupuesto: str = Form("medio"),
    clima_preferido: str = Form("tropical"),
    gustos: str = Form("historia"),
    tipo_viaje: str = Form("cultural")
):
    paises = [p.strip() for p in paises_visitados.split(',') if p.strip()]
    continentes = [c.strip() for c in continentes_visitados.split(',') if c.strip()] or ["america"]
    lista_gustos = [g.strip() for g in gustos.split(',') if g.strip()] or ["historia"]

    perfil = PerfilViajero(
        nombre=nombre,
        paises_visitados=paises,
        continentes_visitados=continentes,
        presupuesto=presupuesto,
        clima_preferido=clima_preferido,
        gustos=lista_gustos,
        tipo_viaje=tipo_viaje
    )

    try:
        resultado = consultar_prolog(perfil)
        plan = generar_plan(perfil, resultado)
    except Exception as e:
        print("Error:", e)
        plan = []

    # Construir HTML de tags del perfil
    tags_html = '<span class="tag">Presupuesto: ' + escape(presupuesto) + '</span>'
    tags_html += '<span class="tag">Clima: ' + escape(clima_preferido) + '</span>'
    tags_html += '<span class="tag">Tipo: ' + escape(tipo_viaje) + '</span>'
    for g in lista_gustos:
        tags_html += '<span class="tag">' + escape(g) + '</span>'

    # Construir HTML de destinos
    destinos_html = ""
    for rec in plan:
        nombre_pais = rec.pais.replace("_", " ").title()
        destinos_html += '<div class="destino-card">'
        destinos_html += '<div class="destino-num">Destino #' + str(rec.orden) + '</div>'
        destinos_html += '<div class="destino-nombre">🌍 ' + escape(nombre_pais) + '</div>'
        destinos_html += '<div class="destino-razon">' + escape(rec.razon) + '</div>'
        destinos_html += '</div>'

    if not destinos_html:
        destinos_html = '<div class="no-resultado">No se encontraron destinos. Intente con otros criterios.</div>'

    return render_template(
        "plan.html",
        {
            "nombre": escape(nombre),
            "total": str(len(plan)),
            "tags_html": tags_html,
            "destinos_html": destinos_html,
        },
    )