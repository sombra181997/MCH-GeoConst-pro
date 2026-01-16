import json
import time
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Canales a extraer
CANALES = [
    {"nombre": "TVN Chile", "url": "https://www.tvn.cl/envivo/"},
    {"nombre": "Chilevisión", "url": "https://www.chilevision.cl/senal-online"}
]

def configurar_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def extraer_link(driver, nombre, url):
    print(f"\n--- Iniciando captura: {nombre} ---")
    try:
        driver.get(url)
        # Esperamos 80 segundos por los comerciales
        for i in range(80, 0, -1):
            sys.stdout.write(f"\rEsperando {nombre}: {i}s... ")
            sys.stdout.flush()
            time.sleep(1)
        
        logs = driver.get_log('performance')
        for entrada in logs:
            msg = json.loads(entrada['message'])['message']
            if 'Network.requestWillBeSent' in msg['method']:
                # PROTECCIÓN: Verificamos si existe 'request' antes de leerlo
                params = msg.get('params', {})
                if 'request' in params:
                    peticion = params['request'].get('url', '')
                    if ".m3u8" in peticion and ("master" in peticion or "index" in peticion):
                        if "ads" not in peticion:
                            return peticion
    except Exception as e:
        print(f"\nError en {nombre}: {e}")
    return None

# Ejecución principal
driver = configurar_driver()
lista_m3u = ["#EXTM3U\n"]

try:
    for canal in CANALES:
        link = extraer_link(driver, canal['nombre'], canal['url'])
        if link:
            lista_m3u.append(f"#EXTINF:-1, {canal['nombre']}\n{link}\n")
            print(f"\n✅ {canal['nombre']} listo.")
        else:
            print(f"\n❌ No se capturó link para {canal['nombre']}.")
    
    with open("lista_final.m3u", "w", encoding="utf-8") as f:
        f.writelines(lista_m3u)
    print("\n--- ¡LISTA CREADA CON ÉXITO! ---")

finally:
    driver.quit()
