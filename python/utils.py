"""
Utilidades compartidas para los algoritmos de Seam Carving.
Funciones comunes para calcular energía, cargar/guardar imágenes, etc.
"""

import sys
import os


def calcular_energia(energia, seam):
    """Calcula la energía total de un seam."""
    res = 0.0
    for i in range(len(seam)):
        res += energia[i][seam[i]]
    return res


def leer_matriz_energia(ruta):
    """Lee una matriz de energía desde un archivo de texto."""
    try:
        with open(ruta, 'r') as archivo:
            primera_linea = archivo.readline().strip().split()
            filas = int(primera_linea[0])
            columnas = int(primera_linea[1])
            
            energia = []
            for f in range(filas):
                fila = list(map(float, archivo.readline().strip().split()))
                if len(fila) != columnas:
                    raise ValueError(f"Fila {f} tiene {len(fila)} columnas, se esperaban {columnas}")
                energia.append(fila)
            
            return energia
    except FileNotFoundError:
        raise FileNotFoundError(f"No se pudo abrir: {ruta}")


def imprimir_matriz(matriz):
    """Imprime una matriz de forma legible."""
    for fila in matriz:
        for val in fila:
            print(f"{val}\t", end="")
        print()


def imprimir_seam(seam, energia):
    """Imprime el seam encontrado y su energía total."""
    print("Seam encontrado: ", end="")
    total = 0.0
    for f in range(len(seam)):
        print(f"({f},{seam[f]}) ", end="")
        total += energia[f][seam[f]]
    print()
    print(f"Energía total: {total}")


def cargar_imagen(ruta):
    """
    Carga una imagen desde disco (requiere PIL/Pillow).
    Retorna: (matriz_pixeles, ancho, alto)
    """
    try:
        from PIL import Image
    except ImportError:
        raise ImportError("PIL/Pillow no está instalado. Instalar con: pip install Pillow")
    
    try:
        img = Image.open(ruta).convert('RGB')
        ancho, alto = img.size
        pixeles = list(img.getdata())
        pixeles_matriz = []
        for y in range(alto):
            fila = []
            for x in range(ancho):
                # Obtener píxel en formato RGB
                fila.append(pixeles[y * ancho + x])
            pixeles_matriz.append(fila)
        return pixeles_matriz, ancho, alto
    except Exception as e:
        raise Exception(f"Error al cargar imagen {ruta}: {e}")


def calcular_matriz_energia_imagen(pixeles, ancho, alto):
    """Calcula la matriz de energía usando diferencias finitas."""
    energia = [[0.0] * ancho for _ in range(alto)]
    
    for fila in range(alto):
        for col in range(ancho):
            gx = 0.0
            gy = 0.0
            
            if col > 0 and col < ancho - 1:
                r_izq, g_izq, b_izq = pixeles[fila][col - 1]
                r_der, g_der, b_der = pixeles[fila][col + 1]
                gx = (r_der - r_izq)**2 + (g_der - g_izq)**2 + (b_der - b_izq)**2
            
            if fila > 0 and fila < alto - 1:
                r_arr, g_arr, b_arr = pixeles[fila - 1][col]
                r_aba, g_aba, b_aba = pixeles[fila + 1][col]
                gy = (r_aba - r_arr)**2 + (g_aba - g_arr)**2 + (b_aba - b_arr)**2
            
            energia[fila][col] = (gx + gy) ** 0.5
    
    return energia


def eliminar_seam_imagen(pixeles, seam, ancho, alto):
    """Elimina un seam de la imagen."""
    nueva_imagen = [[None] * (ancho - 1) for _ in range(alto)]
    
    for fila in range(alto):
        col_seam = seam[fila]
        
        for col in range(col_seam):
            nueva_imagen[fila][col] = pixeles[fila][col]
        
        for col in range(col_seam + 1, ancho):
            nueva_imagen[fila][col - 1] = pixeles[fila][col]
    
    return nueva_imagen, ancho - 1, alto


def guardar_imagen(pixeles, ruta, ancho, alto):
    """Guarda la imagen en disco (requiere PIL/Pillow)."""
    try:
        from PIL import Image
    except ImportError:
        raise ImportError("PIL/Pillow no está instalado. Instalar con: pip install Pillow")
    
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        img_data = []
        for fila in pixeles:
            for pixel in fila:
                img_data.append(pixel)
        
        img = Image.new('RGB', (ancho, alto))
        img.putdata(img_data)
        img.save(ruta)
    except Exception as e:
        raise Exception(f"Error al guardar imagen {ruta}: {e}")


def modo_numerico(encontrar_seam_func, ruta_entrada, algoritmo, ruta_salida=None):
    """Ejecuta algoritmo en modo numérico."""
    try:
        energia = leer_matriz_energia(ruta_entrada)
        
        print("Matriz de energía:")
        imprimir_matriz(energia)
        print()
        
        seam = encontrar_seam_func(energia)
        imprimir_seam(seam, energia)
        
        if ruta_salida is None:
            ruta_salida = f"../output/numericos/seam_{algoritmo}.txt"
        
        os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
        
        with open(ruta_salida, 'w') as salida:
            for f in range(len(seam)):
                salida.write(f"fila {f} -> columna {seam[f]}\n")
        
        print(f"Resultado guardado en {ruta_salida}\n")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def modo_imagen(encontrar_seam_func, ruta_imagen, algoritmo, iteraciones, ruta_salida=None):
    """Ejecuta algoritmo en modo imagen."""
    try:
        pixeles, ancho, alto = cargar_imagen(ruta_imagen)
        print(f"Imagen cargada: {ancho}x{alto} px\n")
        
        for i in range(iteraciones):
            energia = calcular_matriz_energia_imagen(pixeles, ancho, alto)
            seam = encontrar_seam_func(energia)
            pixeles, ancho, alto = eliminar_seam_imagen(pixeles, seam, ancho, alto)
            
            if (i + 1) % 10 == 0 or i == iteraciones - 1:
                print(f"Iteración {i + 1}/{iteraciones} - Ancho actual: {ancho} px")
        
        if ruta_salida is None:
            ruta_salida = f"output/imagenes/resultado_{algoritmo}.png"
        
        guardar_imagen(pixeles, ruta_salida, ancho, alto)
        print(f"Imagen guardada en {ruta_salida}\n")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
