import pandas as pd
import requests
from time import sleep

# 📂 1. Cargar tu archivo Excel
df = pd.read_excel("entidades_publicas_santander.xlsx")

# 📌 Ajusta los nombres de columna según tu archivo
col_nombre = "NombreEntidad"   # Ejemplo: "NombreEntidad"
col_municipio = "Municipio"    # Ejemplo: "Municipio"

# 🔑 2. Inserta tu API Key de Geoapify
API_KEY = "dc9ae8ae402a4e3ca6363450db732f08"

# 🗺️ 3. Crear columnas nuevas
df["latitud"] = None
df["longitud"] = None
df["direccion_completa"] = None

# 🌍 4. Función para consultar Geoapify
def geocode(query):
    url = f"https://api.geoapify.com/v1/geocode/search?text={query}&format=json&apiKey={API_KEY}"
    response = requests.get(url).json()
    if "results" in response and len(response["results"]) > 0:
        result = response["results"][0]
        return result["lat"], result["lon"], result["formatted"]
    return None, None, None

# 🔄 5. Iterar sobre cada entidad
for i, row in df.iterrows():
    query = f"{row[col_nombre]}, {row[col_municipio]}, Colombia"
    try:
        lat, lon, address = geocode(query)
        df.at[i, "latitud"] = lat
        df.at[i, "longitud"] = lon
        df.at[i, "direccion_completa"] = address
        if lat and lon:
            print(f"✔ {query} → {lat}, {lon}")
        else:
            print(f"❌ No encontrado: {query}")
    except Exception as e:
        print(f"⚠ Error en {query}: {e}")
    
    # ⏸️ Pausa de 0.5 seg para no saturar el API
    sleep(0.5)

# 💾 6. Guardar archivo enriquecido
df.to_excel("Entidades_Publicas_Geoapify.xlsx", index=False)

print("✅ Proceso terminado. Archivo guardado como 'Entidades_Publicas_Geoapify.xlsx'")
