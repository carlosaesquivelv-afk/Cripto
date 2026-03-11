# Universidad Nacional Atonoma de Mexico
# Criptografia Grupo:02
# 2026-2
# Andrade Pinto Brandon Mihali
# Esquivel Vargas Carlos Andres
# Pozos Hernandez Angel
# Torres Pimentel Obed


import numpy as np
import math

def crearMatrizCuadrada(Datos):
    """Crea una matriz cuadrada a partir del string, rellenando con 'X'."""
    Datos = Datos.replace(" ", "").upper()
    L = len(Datos)
    n = math.ceil(math.sqrt(L))
    if n == 0: 
        n = 1
    pad_len = n * n - L
    Datos += 'X' * pad_len
    # Se acomoda en una matriz n x n
    matriz = np.array(list(Datos)).reshape((n, n))
    return matriz, n

def crearMatrizCompatible(Datos, tamaño):
    """Crea una matriz compatible para la multiplicación (K * M)."""
    Datos = Datos.replace(" ", "").upper()
    L = len(Datos)
    n = tamaño
    
    # Si el mensaje no llena las columnas, rellenamos con 'X'
    if L % n != 0:
        pad_len = n - (L % n)
        Datos += 'X' * pad_len
        
    # Llenamos la matriz por columnas, por lo que M tendrá 'tamaño' filas
    matriz = np.array(list(Datos)).reshape((-1, n)).T
    return matriz

def codificarMatriz(matriz):
    """Pasa los caracteres a números (A=0, B=1...)."""
    # funcion anidada que codifica un caracter, usada para cada uno de los terminos de la matriz
    def codificar(c):
        c = str(c).upper()
        if not ('A' <= c <= 'Z'):
            raise ValueError(f"Error: Carácter fuera del alfabeto encontrado '{c}'")
        return ord(c) - ord('A') # Resta al ASCII el valor de la latra A para obtener un numero entre 0 y 25
    # procesa cada uno de los terminos de la matriz con la funcion codifica
    return np.vectorize(codificar)(matriz)

def decodificacionMatriz(matriz):
    """Pasa los números (0-25) a caracteres (A-Z)."""
    def decodificar(v):
        try:
            v = int(float(v))
        except ValueError:
            raise ValueError(f"Error: El valor en la matriz no es un número '{v}'")
            
        if not (0 <= v <= 25):
            raise ValueError(f"Error: Número fuera de rango (0-25) encontrado '{v}'")
        return chr(v + ord('A'))
        
    return np.vectorize(decodificar)(matriz)

def determinante(matriz):
    """Obtiene el determinante de la matriz módulo 26."""
    det = round(np.linalg.det(matriz))
    return det % 26

def inversaMatriz(matriz):
    """Calcula la matriz inversa módulo 26."""
    det = determinante(matriz)
    # Verificamos si tiene inversa modular
    if math.gcd(det, 26) != 1:
        raise ValueError("Error: La matriz no tiene inversa módulo 26.")
        
    det_inv = pow(det, -1, 26) # Inverso multiplicativo del determinante
    mat_inv = np.linalg.inv(matriz)
    
    # Matriz adjunta
    adj = np.round(np.linalg.det(matriz) * mat_inv).astype(int)
    inv_mod = (det_inv * adj) % 26
    return inv_mod

def cifradoHill(K, M):
    """Realiza la multiplicación C = K * M (mod 26)."""
    if K.shape[1] != M.shape[0]:
        raise ValueError("Error: Las matrices no se pueden multiplicar debido a sus dimensiones.")
    
    C = np.dot(K, M) % 26
    return C

def descifradoHill(K, C):
    """Realiza la operación M = inversa(K) * C (mod 26)."""
    det = determinante(K)
    if det == 0 or math.gcd(det, 26) != 1:
        raise ValueError("Error: El determinante de la clave es cero")
        
    K_inv = inversaMatriz(K)
    M = np.dot(K_inv, C) % 26
    return M

def imprimirMatrices(K, M, C, modo):
    """Imprime las matrices con sus respectivos encabezados y operadores centrados."""
    # Determinamos los encabezados dependiendo del modo
    titulo1 = "K" if modo.upper() == 'C' else "K^(-1)"
    titulo2 = "M" if modo.upper() == 'C' else "C"
    titulo3 = "C" if modo.upper() == 'C' else "M"

    def crear_bloque(mat):
        # Convertimos la matriz a strings para medir el tamaño
        str_mat = [[str(x) for x in row] for row in mat]
        
        # Obtenemos el ancho máximo de cada columna
        col_widths = [max(len(str_mat[r][c]) for r in range(len(str_mat))) for c in range(len(str_mat[0]))]
        
        # Ancho interno = suma de los anchos de las columnas + los espacios entre ellas
        width_inner = sum(col_widths) + len(col_widths) - 1
        ancho_total = width_inner + 4 # +4 por los caracteres de los bordes y sus espacios internos (ej. '│ ' y ' │')
        
        lineas = []
        # Borde superior vacío
        lineas.append("┌" + " " * (width_inner + 2) + "┐")
        
        # Filas de datos formateadas
        for r in range(len(str_mat)):
            row_str = " ".join(str_mat[r][c].rjust(col_widths[c]) for c in range(len(str_mat[0])))
            lineas.append(f"│ {row_str} │")
            
        # Borde inferior vacío
        lineas.append("└" + " " * (width_inner + 2) + "┘")
        
        return lineas, ancho_total

    # Creamos las líneas para cada matriz y obtenemos sus anchos
    lineas_k, w_k = crear_bloque(K)
    lineas_m, w_m = crear_bloque(M)
    lineas_c, w_c = crear_bloque(C)

    # Igualamos alturas agregando espacios (útil si M y C tienen dimensiones diferentes a K)
    max_h = max(len(lineas_k), len(lineas_m), len(lineas_c))
    
    def rellenar(lineas, ancho, altura_max):
        pad_top = (altura_max - len(lineas)) // 2
        pad_bot = altura_max - len(lineas) - pad_top
        return [" " * ancho] * pad_top + lineas + [" " * ancho] * pad_bot

    lineas_k = rellenar(lineas_k, w_k, max_h)
    lineas_m = rellenar(lineas_m, w_m, max_h)
    lineas_c = rellenar(lineas_c, w_c, max_h)

    # Imprimir los encabezados centrados sobre cada matriz
    # Los espacios coinciden con el tamaño de los operadores
    sep_op1 = "   "
    sep_op2 = "            "
    print(f"{titulo1:^{w_k}}{sep_op1}{titulo2:^{w_m}}{sep_op2}{titulo3:^{w_c}}")

    # Imprimir línea por línea las matrices
    mid_idx = max_h // 2
    for i in range(max_h):
        # Insertamos los operadores justo en la mitad de la altura de la matriz
        if i == mid_idx:
            op1 = " * "
            op2 = " (mod 26) = "
        else:
            op1 = "   "
            op2 = "            "
            
        print(lineas_k[i] + op1 + lineas_m[i] + op2 + lineas_c[i])

if __name__ == '__main__':
    print("\n" + "="*29 + "[ CIFRADO HILL ]" + "="*29)
    
    while True:
        opcion = input("\nQuiere cifrar o descifrar? (C/D), Enter para salir: ").strip().upper()
        
        if opcion == '':
            print("\nSaliendo del programa...\n")
            break
            
        if opcion not in ['C', 'D']:
            print("Opción no válida. Ingresa 'C', 'D' o presiona Enter para salir.")
            continue # Salta al ciclo siguiente para volver a preguntar la opcion en caso de no ser valida la que se ingreso
            
        if opcion == 'C': 
            print("\n" + "-"*31 +"[ CIFRANDO ]" + "-"*31 + "\n")
            mensaje = input("Ingresa el Mensaje (M): ")
        if opcion == 'D': 
            print("\n" + "-"*29 +"[ DESCIFRANDO ]" + "-"*30 + "\n")
            mensaje = input("Ingresa el Mensaje Cifrado (C): ")
        
        # Validación de la clave K
        while True:
            clave = input("Ingresa la Clave (K): ")
            K_chars, size = crearMatrizCuadrada(clave)
            
            try:
                K_num = codificarMatriz(K_chars)
                # Validamos si tiene inversa
                det = determinante(K_num)
                if math.gcd(det, 26) != 1:
                    print("\nError: La clave K no tiene inversa módulo 26. Ingresa una clave diferente.")
                    continue
                break # Si tiene inversa, salimos del loop de validación
            except ValueError as e:
                print(e)
                print("Por favor, ingresa una clave válida que contenga solo letras.")
        
        M_chars = crearMatrizCompatible(mensaje, size)
        
        try:
            M_num = codificarMatriz(M_chars)
            
            if opcion == 'C':
                # Cálculos
                C_num = cifradoHill(K_num, M_num)
                C_chars = decodificacionMatriz(C_num)
                
                # Imprimir Matrices en Caracteres
                print("\nMatrices en caracteres:")
                imprimirMatrices(K_chars, M_chars, C_chars, 'C')
                
                # Imprimir Matrices en Números
                print("\nMatrices numéricas:")
                imprimirMatrices(K_num, M_num, C_num, 'C')
                
                # Imprime texto cifrado (leyendo columnas)
                texto_final = "".join(C_chars.T.flatten())
                print(f"\nEl texto cifrado (C) es: {texto_final}")
                
            elif opcion == 'D':
                # Cálculos
                K_inv_num = inversaMatriz(K_num)
                K_inv_chars = decodificacionMatriz(K_inv_num) # Inversa en letras
                
                M_result_num = descifradoHill(K_num, M_num) # Aquí M_num es en realidad C_num según el concepto
                M_result_chars = decodificacionMatriz(M_result_num)
                
                # Imprimir Matrices en Caracteres (Pasando K inversa)
                print("\nMatrices en caracteres:")
                imprimirMatrices(K_inv_chars, M_chars, M_result_chars, 'D')
                
                # Imprimir Matrices en Números
                print("\nMatrices numéricas:")
                imprimirMatrices(K_inv_num, M_num, M_result_num, 'D')
                
                # Imprime texto descifrado
                texto_final = "".join(M_result_chars.T.flatten())
                print(f"\nEl texto descifrado (M) es: {texto_final}")
                
        except ValueError as e:
            print(f"Ocurrió un error en el procesamiento: {e}")