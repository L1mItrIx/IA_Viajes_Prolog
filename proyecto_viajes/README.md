# Proyecto Viajes - Guia Completa para Entenderlo y Ejecutarlo

Este proyecto es un asistente web de planificacion de viajes que combina:

- FastAPI (backend web en Python)
- Prolog (motor de reglas logicas para recomendar destinos)
- Ollama (IA local opcional para redactar explicaciones)

La idea clave es:

1. El usuario llena un formulario.
2. Python convierte ese perfil en hechos para Prolog.
3. Prolog decide los destinos segun reglas.
4. Python arma una respuesta HTML con recomendaciones y explicaciones.

## 1) Estructura del proyecto

```text
backend/
  ai_service.py
  main.py
  models.py
  plan_service.py
  prolog_service.py
  requirements.txt
  static/
    styles.css
  templates/
    index.html
    plan.html
prolog/
  destinos.pl
```

## 2) Que hace cada archivo

### backend/main.py
Es la aplicacion FastAPI principal.

- Ruta GET /: muestra el formulario (index.html).
- Ruta POST /plan: recibe datos del usuario, construye el perfil, consulta Prolog y renderiza plan.html.

Tambien monta archivos estaticos en /static.

### backend/models.py
Define estructuras de datos (dataclasses):

- PerfilViajero: datos de entrada del usuario.
- Recomendacion: resultado final por destino (pais, razon, orden).

### backend/prolog_service.py
Puente entre Python y SWI-Prolog.

Responsabilidades:

- Limpiar texto de entrada (acentos, espacios, mayusculas).
- Construir un goal de Prolog con assert/retractall.
- Ejecutar SWI-Prolog por subprocess.
- Parsear salida para obtener listas de destinos.

Funciones importantes:

- obtener_recomendados(perfil)
- obtener_diferentes(perfil)
- consultar_prolog(perfil)

### prolog/destinos.pl
Base de conocimiento y reglas.

Tiene:

- Hechos de destinos (continente, costo, clima, experiencia, etc.).
- Hechos dinamicos del usuario (visitado, gusto, presupuesto_usuario...).
- Reglas de recomendacion:
  - presupuesto_aceptable
  - no_visitado
  - coincide_clima
  - coincide_gusto
  - recomendado
  - destino_diferente

### backend/plan_service.py
Convierte destinos recomendados en un plan con texto explicativo.

- Usa una descripcion base por pais (diccionario INFO_PAISES).
- Intenta enriquecer la razon con IA local (Ollama).
- Si Ollama falla, usa texto fallback local.

### backend/ai_service.py
Cliente HTTP simple para Ollama local.

- URL por defecto: http://localhost:11434
- Modelo por defecto: llama3.1

Variables de entorno opcionales:

- OLLAMA_URL
- OLLAMA_MODEL

### backend/templates/index.html y plan.html
Vistas HTML simples con placeholders como {{nombre}}.

No hay Jinja2; el reemplazo de placeholders se hace manualmente en main.py.

## 3) Flujo completo (de extremo a extremo)

1. Usuario abre / y llena formulario.
2. FastAPI recibe POST /plan.
3. Se parsean listas separadas por coma:
   - paises_visitados
   - continentes_visitados
   - gustos
4. Se construye PerfilViajero.
5. Python llama consultar_prolog(perfil).
6. Prolog evalua reglas y devuelve destinos.
7. Python genera explicaciones por destino (IA local o fallback).
8. Se renderiza plan.html con el resultado.

## 4) Como ejecutar el proyecto (Windows + VS Code)

Asegurate de estar en la raiz del proyecto (donde estan backend y prolog).

### Opcion recomendada (sin depender de Activate.ps1)

```powershell
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
cd backend
..\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Abre en navegador:

- http://127.0.0.1:8000

### Opcion clasica (activando venv)

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
cd backend
uvicorn main:app --reload
```

Si PowerShell bloquea scripts:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Luego vuelve a ejecutar Activate.ps1.

## 5) Requisitos externos importantes

### SWI-Prolog
El backend llama al ejecutable swipl.

- Si swipl esta en PATH: funciona directo.
- Si no esta en PATH: define variable SWIPL_PATH con ruta completa al ejecutable.

Ejemplo PowerShell:

```powershell
$env:SWIPL_PATH = "C:\\Program Files\\swipl\\bin\\swipl.exe"
```

### Ollama (opcional)
Si esta levantado, genera explicaciones mas naturales.
Si no esta levantado, el proyecto sigue funcionando con fallback.

## 6) Diagnostico rapido de errores comunes

### Error: UnauthorizedAccess al ejecutar Activate.ps1
Solucion:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

O usa directamente .venv\Scripts\python.exe sin activar.

### Error: No module named ...
Instala dependencias en el Python correcto:

```powershell
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

### Error de Prolog / swipl no encontrado
Instala SWI-Prolog o define SWIPL_PATH.

### La pagina carga pero no hay recomendaciones
Revisa:

- Formato de entradas (ejemplo: costa_rica,panama)
- Que los valores coincidan con el vocabulario esperado por Prolog
- Logs de la terminal del servidor

## 7) Valores esperados por el sistema

Para obtener mejores resultados, usa palabras compatibles con la base Prolog.

Ejemplos utiles:

- Presupuesto: bajo, medio, alto
- Clima: tropical, templado, frio, desertico
- Gustos: gastronomia, historia, vidanocturna, ecoturismo, aventura, tecnologia, relajacion
- Continentes: america, europa, asia, africa, oceania

## 8) Comandos utiles de desarrollo

### Instalar/actualizar dependencias

```powershell
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

### Correr servidor

```powershell
cd backend
..\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

### Parar servidor
En la terminal activa: Ctrl + C

## 9) Mejoras futuras recomendadas

- Migrar render_template manual a Jinja2 para plantillas mas robustas.
- Agregar validaciones de entrada mas estrictas.
- Agregar pruebas unitarias para servicios Python y reglas Prolog.
- Manejar errores de Prolog con mensajes mas amigables en UI.
- Agregar endpoint de healthcheck.

## 10) Resumen corto

El motor de decision es Prolog.
Python conecta todo.
Ollama solo mejora texto (no decide destinos).
Si tienes Python + dependencias + SWI-Prolog, el proyecto ya puede funcionar.
