import sys
from utils import (
    calcular_energia,
    leer_matriz_energia,
    imprimir_matriz,
    imprimir_seam,
    modo_numerico,
    modo_imagen
)


def encontrar_seam_fuerza_bruta_aux(energia, sol, opt):
    i = len(sol) - 1
    j = sol[-1]
    
    if j < 0 or j >= len(energia[0]):
        return []
    
    if i == len(energia) - 1:
        energia_seam = calcular_energia(energia, sol)
        if opt[0] == -1 or energia_seam < opt[0]:
            opt[0] = energia_seam
            return sol.copy()
        return []
    
    sol.append(j - 1)
    s1 = encontrar_seam_fuerza_bruta_aux(energia, sol, opt)
    sol.pop()
    
    sol.append(j)
    s2 = encontrar_seam_fuerza_bruta_aux(energia, sol, opt)
    sol.pop()
    
    sol.append(j + 1)
    s3 = encontrar_seam_fuerza_bruta_aux(energia, sol, opt)
    sol.pop()
    
    if s3:
        return s3
    elif s2:
        return s2
    elif s1:
        return s1
    
    return []


def encontrar_seam_fuerza_bruta(energia):
    if not energia:
        return []
    
    m = len(energia[0])
    seam_opt = []
    energia_opt = [-1]
    
    for i in range(m):
        seam_loc = encontrar_seam_fuerza_bruta_aux(energia, [i], energia_opt)
        if seam_loc:
            seam_opt = seam_loc
    
    return seam_opt


def imprimir_uso():
    print("Uso:")
    print("  Modo numérico: python FuerzaBruta.py --numerico <archivo>")
    print("  Modo imagen:   python FuerzaBruta.py --imagen <archivo> --iteraciones <N>")


def main():
    if len(sys.argv) < 2:
        imprimir_uso()
        sys.exit(1)
    
    modo = None
    ruta_archivo = None
    algoritmo = "fb"
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
            modo_numerico(encontrar_seam_fuerza_bruta, ruta_archivo, algoritmo)
        elif modo == "imagen":
            modo_imagen(encontrar_seam_fuerza_bruta, ruta_archivo, algoritmo, iteraciones)
        else:
            imprimir_uso()
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
