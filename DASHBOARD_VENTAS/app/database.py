#Aquí colocamos todo lo relacionado con Pandas y la lectura/creación del archivo CSV.

from pathlib import Path
import pandas as pd

# Ubicación del dataset (sube un nivel desde app/ para guardarse en la raíz del proyecto)
ARCHIVO = Path(__file__).resolve().parent.parent / "ventas.csv"


def crear_dataset():
    if not ARCHIVO.exists():
        datos = {
            "mes": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio"],
            "ventas": [1200, 1800, 1500, 2300, 2800, 3500],
            "clientes": [25, 32, 29, 40, 46, 58],
        }
        df = pd.DataFrame(datos)
        df.to_csv(ARCHIVO, index=False)


def obtener_datos():
  crear_dataset()
  return pd.read_csv(ARCHIVO)