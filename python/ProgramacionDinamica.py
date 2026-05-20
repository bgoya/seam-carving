import sys
from utils import (
    calcular_energia,
    leer_matriz_energia,
    imprimir_matriz,
    imprimir_seam,
    modo_numerico,
    modo_imagen
)


def encontrar_seam_pd_aux(energia, memoizacion, i, j):
    n = len(energia)
    m = len(energia[0])
    
    if j < 0 or j >= m:
        return 1e18
    
    if memoizacion[i][j] != -1.0:
        return memoizacion[i][j]
    
    if i == n - 1:
        memoizacion[i][j] = energia[i][j]
        return memoizacion[i][j]
    
    s1 = encontrar_seam_pd_aux(energia, memoizacion, i + 1, j - 1)
    s2 = encontrar_seam_pd_aux(energia, memoizacion, i + 1, j)
    s3 = encontrar_seam_pd_aux(energia, memoizacion, i + 1, j + 1)
    
    memoizacion[i][j] = energia[i][j] + min(s1, min(s2, s3))
    return memoizacion[i][j]


def encontrar_seam_pd(energia):
    if not energia:
        return []
    
    n = len(energia)
    m = len(energia[0])
    
    # Inicializar tabla de memoización
    memoizacion = [[-1.0] * m for _ in range(n)]
    
    # Calcular energías para todas las columnas de la primera fila
    min_col = 0
    for j in range(m):
        encontrar_seam_pd_aux(energia, memoizacion, 0, j)
        if memoizacion[0][j] < memoizacion[0][min_col]:
            min_col = j
    
    # Reconstruir el seam óptimo
    seam_opt = [0] * n
    seam_opt[0] = min_col
    
    for i in range(1, n):
        col = seam_opt[i - 1]
        energia_opt = col
        
        if col > 0 and memoizacion[i][col - 1] < memoizacion[i][energia_opt]:
            energia_opt = col - 1
        
        if col < m - 1 and memoizacion[i][col + 1] < memoizacion[i][energia_opt]:
            energia_opt = col + 1
        
        seam_opt[i] = energia_opt
    
    return seam_opt


def imprimir_uso():
    print("Uso:")
    print("  Modo numérico: python ProgramacionDinamica.py --numerico <archivo>")
    print("  Modo imagen:   python ProgramacionDinamica.py --imagen <archivo> --iteraciones <N>")


def main():
    if len(sys.argv) < 2:
        imprimir_uso()
        sys.exit(1)
    
    modo = None
    ruta_archivo = None
    algoritmo = "pd"
    iteraciones = 1
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg == "--numerico" and i + 1 < len(sys.argv):
            modo = "numerico"
            ruta_archivo = sys.argv[i + 1]
            i += 2
        elif arg == "--imagen" and i + 1 < len(sys.argv):
            modo = "imagen"
            ruta_archivo = sys.argv[i + 1]
            i += 2
        elif arg == "--iteraciones" and i + 1 < len(sys.argv):
            iteraciones = int(sys.argv[i + 1])
            i += 2
        elif arg == "--ayuda" or arg == "--help":
            imprimir_uso()
            sys.exit(0)
        else:
            i += 1
    
    try:
        if modo == "numerico":
            modo_numerico(encontrar_seam_pd, ruta_archivo, algoritmo)
        elif modo == "imagen":
            modo_imagen(encontrar_seam_pd, ruta_archivo, algoritmo, iteraciones)
        else:
            imprimir_uso()
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
