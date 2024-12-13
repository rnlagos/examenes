from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import pandas as pd
import random

# Configuración de FastAPI
app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Cargar las preguntas
df = pd.read_csv("data/preguntas.csv")
df['Bloque'] = pd.to_numeric(df['Bloque'], errors='coerce')

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# Variable global para almacenar el tiempo de inicio
tiempo_inicio = None

@app.post("/generar_cuestionario", response_class=HTMLResponse)
async def generar_cuestionario(request: Request, bloques: str = Form(...), num_preguntas: int = Form(...)):
    global tiempo_inicio
    bloques_seleccionados = [int(bloque.strip()) for bloque in bloques.split(",")]
    preguntas_seleccionadas = []

    for bloque in bloques_seleccionados:
        preguntas_bloque = df[df['Bloque'] == bloque]
        if preguntas_bloque.empty:
            return templates.TemplateResponse("home.html", {
                "request": request,
                "error": f"No hay preguntas disponibles para el bloque {bloque}."
            })

        num_preguntas_bloque = min(num_preguntas, len(preguntas_bloque))
        preguntas_seleccionadas += preguntas_bloque.sample(num_preguntas_bloque).to_dict(orient="records")

    # Almacena el tiempo de inicio del cuestionario
    tiempo_inicio = datetime.now()

    return templates.TemplateResponse("quiz.html", {"request": request, "preguntas": preguntas_seleccionadas})

@app.post("/evaluar", response_class=HTMLResponse)
async def evaluar(request: Request, respuestas: str = Form(...), preguntas_json: str = Form(...)):
    from json import loads

    # Convertir preguntas seleccionadas de JSON a lista
    preguntas_seleccionadas = loads(preguntas_json)
    respuestas_usuario = respuestas.split(",")
    aciertos = 0
    errores = 0
    preguntas_falladas = []

    # Evaluar las respuestas
    for user_resp, pregunta in zip(respuestas_usuario, preguntas_seleccionadas):
        respuesta_correcta = pregunta["Correcta"]
        if user_resp.upper() == respuesta_correcta:
            aciertos += 1
        else:
            if user_resp.strip():  # Solo registrar si el usuario respondió algo
                errores += 1
            # Guardar preguntas falladas
            preguntas_falladas.append({
                "Pregunta": pregunta["Pregunta"],
                "Respuesta_correcta": respuesta_correcta,
                "Tu_respuesta": user_resp
            })

    # Calcular puntuación final
    numero_preguntas = len(preguntas_seleccionadas)
    puntuacion = ((aciertos - (errores * 0.25)) / numero_preguntas) * 10

    # Calcular tiempo
    tiempo_fin = datetime.now()
    tiempo_total_segundos = (tiempo_fin - tiempo_inicio).total_seconds()
    minutos = int(tiempo_total_segundos // 60)
    segundos = int(tiempo_total_segundos % 60)
    tiempo_total_formateado = f"{minutos} minutos y {segundos} segundos"

    return templates.TemplateResponse("resultado.html", {
        "request": request,
        "puntuacion": round(puntuacion, 2),
        "aciertos": aciertos,
        "errores": errores,
        "numero_preguntas": numero_preguntas,
        "tiempo_total": tiempo_total_formateado,
        "preguntas_falladas": preguntas_falladas
    })





