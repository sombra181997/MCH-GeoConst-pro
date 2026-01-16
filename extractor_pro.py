import json
import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Canales para probar (Agregué 24 Horas que suele ser más fácil de capturar)
CANALES = [
    {"nombre": "24 Horas Noticias", "url": "https://www.24horas.cl/envivo/"},
    {"nombre": "TVN Chile", "url": "https://www.tvn.cl/envivo/"},
    {"nombre": "Chilevisión", "url": "https://www.chilevision.cl/senal-online"}
]

def configurar_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # Esto hace que el robot parezca un usuario normal de Windows
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def extraer_link(driver, nombre, url):
    print(f"\n--- Buscando señal para: {nombre} ---")
    try:
        driver.get(url)
        # Aumentamos a 100 segundos para dar más tiempo en la nube
        for i in range(100, 0, -1):
            sys.stdout.write(f"\rAnalizando {nombre}: {i}s... ")
            sys.stdout.flush()
            time.sleep(1)
        
        logs = driver.get_log('performance')
        for entrada in logs:
            msg = json.loads(entrada['message'])['message']
            if 'Network.requestWillBeSent' in msg['method']:
                params = msg.get('params', {})
                if 'request' in params:
                    peticion = params['request'].get('url', '')
                    # Buscamos links de video .m3u8
                    if ".m3u8" in peticion and "ads" not in peticion:
                        print(f"\n¡Link encontrado para {nombre}!")
                        return peticion
    except Exception as e:
        print(f"\nError en {nombre}: {e}")
    return None

driver = configurar_driver()
lista_m3u = ["#EXTM3U\n"]

try:
    for canal in CANALES:
        link = extraer_link(driver, canal['nombre'], canal['url'])
        if link:
            lista_m3u.append(f"#EXTINF:-1, {canal['nombre']}\n{link}\n")
        else:
            print(f"\n❌ No se pudo capturar {canal['nombre']} (Posible bloqueo regional)")

    with open("lista_final.m3u", "w", encoding="utf-8") as f:
        f.writelines(lista_m3u)
    print("\n--- PROCESO FINALIZADO ---")

finally:
    driver.quit()
