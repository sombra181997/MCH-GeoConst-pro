# Código simplificado para evitar bloqueos regionales
def generar_lista():
    print("--- Iniciando creación de lista estable (YouTube Live) ---")
    
    # Canales oficiales de noticias y señal en vivo
    canales = [
        {"nombre": "24 Horas Noticias (TVN)", "url": "https://www.youtube.com/@24horas/live"},
        {"nombre": "CHV Noticias", "url": "https://www.youtube.com/@CHVNoticias/live"},
        {"nombre": "T13 En Vivo", "url": "https://www.youtube.com/@teletrece/live"},
        {"nombre": "Meganoticias", "url": "https://www.youtube.com/@meganoticias/live"}
    ]
    
    lista_contenido = ["#EXTM3U\n"]
    
    for c in canales:
        lista_contenido.append(f"#EXTINF:-1, {c['nombre']}\n{c['url']}\n")
        print(f"✅ Agregado: {c['nombre']}")
    
    with open("lista_final.m3u", "w", encoding="utf-8") as f:
        f.writelines(lista_contenido)
    
    print("--- ¡PROCESO TERMINADO EXITOSAMENTE! ---")

if __name__ == "__main__":
    generar_lista()
