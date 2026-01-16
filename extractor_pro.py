from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import sys

# Lista de canales a extraer
CANALES = [
    {"nombre": "TVN Chile", "url": "https://www.tvn.cl/envivo/"},
    {"nombre": "Chilevisión", "url": "https://www.chilevision.cl/senal-online"},
    # Puedes agregar más canales aquí siguiendo el mismo formato
]

opciones = webdriver.ChromeOptions()
opciones.add_argument('--headless') # En GitHub DEBE ser headless (invisible)
opciones.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

def extraer_link(driver, nombre, url):
    print(f"\n--- Procesando: {nombre} ---")
    driver.get(url)
    
    # Esperamos 90 segundos para asegurar que pasen los anuncios
    for i in range(90, 0, -1):
        sys.stdout.write(f"\rEsperando anuncios de {nombre}: {i}s...   ")
        sys.stdout.flush()
        time.sleep(1)
    
    logs = driver.get_log('performance')
    for entrada in logs:
        msg = json.loads(entrada['message'])['message']
        if 'Network.requestWillBeSent' in msg['method']:
            peticion = msg['params']['request']['url']
            if ".m3u8" in peticion and ("master" in peticion or "index" in peticion):
                if "ads" not in peticion:
                    return peticion
    return None

# Inicio del proceso
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=opciones)

lista_m3u = ["#EXTM3U\n"]

try:
    for canal in CANALES:
        link = extraer_link(driver, canal['nombre'], canal['url'])
        if link:
            lista_m3u.append(f"#EXTINF:-1, {canal['nombre']}\n{link}\n")
            print(f"\n✅ ¡{canal['nombre']} capturado!")
        else:
            print(f"\n❌ No se encontró link para {canal['nombre']}")

    # Guardar todos los resultados en el archivo final
    with open("lista_final.m3u", "w", encoding="utf-8") as f:
        f.writelines(lista_m3u)
    print("\n--- PROCESO TERMINADO: Lista generada con éxito ---")

finally:
    driver.quit()
