from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import sys

# 1. Configuración para capturar el tráfico de red
opciones = webdriver.ChromeOptions()
opciones.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

print("--- INICIANDO RADAR DE TRÁFICO IPTV ---")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=opciones)

url = "https://www.tvn.cl/envivo/"

try:
    print(f"Entrando a: {url}")
    driver.get(url)
    
    print("\n[!] Tienes 90 segundos. CIERRA LOS ANUNCIOS Y DALE PLAY SI ES NECESARIO.")
    
    encontrado = False
    # Escaneamos el tráfico durante 90 segundos
    for i in range(90, 0, -1):
        sys.stdout.write(f"\rEscaneando tráfico de red... {i}s restantes   ")
        sys.stdout.flush()
        
        # Extraemos los logs de rendimiento (el tráfico)
        logs = driver.get_log('performance')
        
        for entrada in logs:
            mensaje = json.loads(entrada['message'])['message']
            
            # Buscamos en las peticiones de red
            if 'Network.requestWillBeSent' in mensaje['method']:
                url_peticion = mensaje['params']['request']['url']
                
                # Buscamos el link .m3u8 que tenga el token
                if ".m3u8" in url_peticion and ("master" in url_peticion or "index" in url_peticion):
                    link_final = url_peticion
                    
                    # Guardamos el archivo
                    with open("lista_definitiva.m3u", "w", encoding="utf-8") as f:
                        f.write("#EXTM3U\n#EXTINF:-1, Canal Capturado\n" + link_final + "\n")
                    
                    print(f"\n\n¡LOGRADO! El radar capturó el link en el aire.")
                    print(f"Link: {link_final[:70]}...")
                    encontrado = True
                    break
        
        if encontrado:
            break
        time.sleep(1)

    if not encontrado:
        print("\n\nEl radar no detectó el flujo .m3u8. Revisa si el video se reprodujo.")

finally:
    driver.quit()
    print("Proceso finalizado.")