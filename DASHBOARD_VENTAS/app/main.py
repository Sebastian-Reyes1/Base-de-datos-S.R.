#Aquí inicializamos FastAPI() y llamamos a las funciones de los demás archivos.

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response
from app.database import obtener_datos
from app.services import generar_grafico

# Crear API
app = FastAPI(title="Dashboard de Ventas")


# ENDPOINT 1: DATOS DEL CSV
@app.get("/datos")
def datos():
  df = obtener_datos()
  return df.to_dict(orient="records")


# ENDPOINT 2: ESTADÍSTICAS
@app.get("/estadisticas")
def estadisticas():
  df = obtener_datos()

  return {
      "total_ventas": float(df["ventas"].sum()),
      "promedio_ventas": float(df["ventas"].mean()),
      "total_clientes": int(df["clientes"].sum()),
      "mejor_mes": str(df.at[df["ventas"].idxmax(), "mes"]),
  }


# ENDPOINT 3: GRÁFICO DE BARRAS
@app.get("/grafico/barras")
def grafico_barras():
  imagen = generar_grafico("barras")
  return Response(content=imagen, media_type="image/png")


# ENDPOINT 4: GRÁFICO DE LÍNEAS
@app.get("/grafico/lineas")
def grafico_lineas():
  imagen = generar_grafico("lineas")
  return Response(content=imagen, media_type="image/png")


# ENDPOINT 5: DASHBOARD WEB
@app.get("/", response_class=HTMLResponse)
def dashboard():
  df = obtener_datos()

  total = df["ventas"].sum()
  promedio = df["ventas"].mean()
  clientes = df["clientes"].sum()

  html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Dashboard de Ventas</title>
        <style>
            body {{ font-family: Arial; background: #f0f4f8; padding: 30px; }}
            h1 {{ color: #1e3a5f; }}
            .indicadores {{ display: flex; gap: 20px; flex-wrap: wrap; }}
            .tarjeta {{ background: white; padding: 25px; border-radius: 12px; box-shadow: 0 3px 8px #ddd; flex: 1; min-width: 160px; }}
            .graficos {{ display: flex; flex-wrap: wrap; gap: 20px; margin-top: 25px; }}
            .graficos img {{ width: 100%; max-width: 580px; border-radius: 10px; background: white; }}
        </style>
    </head>
    <body>
        <h1>Dashboard de Ventas</h1>
        <p>Análisis de datos con Python y FastAPI (Modularizado)</p>
        <div class="indicadores">
            <div class="tarjeta"><h3>Ventas totales</h3><h2>${total:,.2f}</h2></div>
            <div class="tarjeta"><h3>Promedio mensual</h3><h2>${promedio:,.2f}</h2></div>
            <div class="tarjeta"><h3>Clientes registrados</h3><h2>{clientes}</h2></div>
        </div>
        <div class="graficos">
            <img src="/grafico/barras">
            <img src="/grafico/lineas">
        </div>
        <p>
            <a href="/datos">Ver Dataset</a> |
            <a href="/estadisticas">Ver estadísticas</a> |
            <a href="/docs">Documentación API</a>
        </p>
    </body>
    </html>
    """
  return HTMLResponse(content=html)
