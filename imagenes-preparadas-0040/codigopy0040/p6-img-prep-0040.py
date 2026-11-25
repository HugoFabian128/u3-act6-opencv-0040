# Nombre: Hugo Fabian
# NC: 0040

import cv2
import numpy as np
import os
import csv
from PIL import Image
import pillow_avif  # Habilita el soporte para .avif

# 1. Subir dos niveles desde 'imagenes-preparadas-0040/codigopy0040' hasta la raíz 'U3-ACT6-OPENCV-0040'
directorio_script = os.path.dirname(os.path.abspath(__file__))
raiz_proyecto = os.path.abspath(os.path.join(directorio_script, "..", ".."))

carpeta_original = os.path.join(raiz_proyecto, "img-original-0040")
carpeta_preparadas = os.path.join(raiz_proyecto, "imagenes-preparadas-0040")
carpeta_resultados = os.path.join(raiz_proyecto, "resultados-img-0040")

ANCHO_DESTINO = 224
ALTO_DESTINO = 224

os.makedirs(carpeta_preparadas, exist_ok=True)
os.makedirs(carpeta_resultados, exist_ok=True)

# Nombres exactos de tus subcarpetas y archivos
archivos_por_categoria = {
    "imagen-cereza": [
        "cereza1.jpg",
        "cereza2.jpg",
        "cereza3.jpeg",
        "cereza4.jpg",
        "cereza5.png"
    ],
    "imagen-uva": [
        "uva-fruto.jpg",
        "uva2.jpg",
        "uva3.jpeg",
        "uva4.png",
        "uva5.avif"
    ]
}

reporte = []
imagenes_procesadas = 0
imagenes_aprobadas = 0

print("👤 Alumno: Hugo Fabian | NC: 0040")
print(f"📂 Raíz del proyecto detectada: {raiz_proyecto}\n")

# 2. Recorrer cada categoría y su lista específica de archivos
for categoria, lista_archivos in archivos_por_categoria.items():
    ruta_origen = os.path.join(carpeta_original, categoria)
    ruta_destino = os.path.join(carpeta_preparadas, categoria)
    
    os.makedirs(ruta_destino, exist_ok=True)
    
    for nombre_archivo in lista_archivos:
        ruta_imagen = os.path.join(ruta_origen, nombre_archivo)
        nombre_sin_ext = os.path.splitext(nombre_archivo)[0]
        
        print(f"📸 Procesando [{categoria}]: {nombre_archivo}")
        
        if not os.path.exists(ruta_imagen):
            print(f"   ⚠️ Error: No se encontró {ruta_imagen}")
            reporte.append([categoria, nombre_archivo, "NO ENCONTRADO", "-", "-", "-", "-", "-", "-", "REVISAR"])
            continue
            
        # 3. Leer la imagen (primero con OpenCV; si falla por ser .avif, usa Pillow)
        imagen = cv2.imread(ruta_imagen)
        if imagen is None:
            try:
                img_pil = Image.open(ruta_imagen).convert("RGB")
                # Convertir formato RGB de Pillow al formato BGR de OpenCV
                imagen = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
            except Exception:
                imagen = None

        if imagen is None:
            print(f"   ❌ Error: No se pudo leer la imagen.")
            reporte.append([categoria, nombre_archivo, "ERROR", "-", "-", "-", "-", "-", "-", "REVISAR"])
            continue
            
        imagenes_procesadas += 1
        alto_orig, ancho_orig, canales = imagen.shape
        print(f"   📏 Dimensiones originales: {ancho_orig} x {alto_orig}")
        
        # 4. Redimensionar y guardar SOLO la imagen JPG
        imagen_redimensionada = cv2.resize(imagen, (ANCHO_DESTINO, ALTO_DESTINO), interpolation=cv2.INTER_AREA)
        print(f"   📐 Dimensiones nuevas: {ANCHO_DESTINO} x {ALTO_DESTINO}")
        
        ruta_jpg = os.path.join(ruta_destino, f"{nombre_sin_ext}.jpg")
        cv2.imwrite(ruta_jpg, imagen_redimensionada)
        
        # 5. Calcular normalización en memoria
        imagen_normalizada = imagen_redimensionada.astype(np.float32) / 255.0
        val_min = float(np.min(imagen_normalizada))
        val_max = float(np.max(imagen_normalizada))
        print(f"   🔢 Rango normalizado: {val_min:.3f} a {val_max:.3f}")
        
        # 6. Evaluar automáticamente el resultado
        dimensiones_correctas = (imagen_redimensionada.shape[0] == ALTO_DESTINO and 
                                 imagen_redimensionada.shape[1] == ANCHO_DESTINO)
        rango_correcto = (val_min >= 0.0 and val_max <= 1.0)
        archivo_guardado = os.path.isfile(ruta_jpg)
        
        if dimensiones_correctas and rango_correcto and archivo_guardado:
            estado = "APROBADA"
            imagenes_aprobadas += 1
            print(f"   ✅ Evaluación: APROBADA\n")
        else:
            estado = "REVISAR"
            print(f"   ⚠️ Evaluación: REVISAR\n")
            
        # 7. Guardar datos en la lista para el reporte final
        reporte.append([
            categoria, nombre_archivo, "OK", ancho_orig, alto_orig,
            ANCHO_DESTINO, ALTO_DESTINO, round(val_min, 3), round(val_max, 3), estado
        ])

# 8. Generar el reporte en formato CSV
ruta_reporte = os.path.join(carpeta_resultados, "reporte_preparacion.csv")
with open(ruta_reporte, "w", newline="", encoding="utf-8") as archivo:
    escritor = csv.writer(archivo)
    escritor.writerow([
        "Categoría", "Archivo original", "Lectura", 
        "Ancho original", "Alto original", "Ancho preparado", "Alto preparado", 
        "Valor mínimo norm.", "Valor máximo norm.", "Evaluación"
    ])
    escritor.writerows(reporte)

# 9. Resumen final en consola
print("=" * 45)
print("🎉 RESUMEN DE LA PRÁCTICA - HUGO FABIAN (NC: 0040)")
print("=" * 45)
print(f"Imágenes procesadas: {imagenes_procesadas}")
print(f"Imágenes aprobadas:  {imagenes_aprobadas}")
print(f"Imágenes a revisar:  {imagenes_procesadas - imagenes_aprobadas}")
print(f"\n📁 Reporte guardado en: {ruta_reporte}")
print("✅ PRÁCTICA TERMINADA EXITOSAMENTE")