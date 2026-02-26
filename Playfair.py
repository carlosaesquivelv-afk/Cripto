# Universidad Nacional Atonoma de Mexico
# Criptografia Grupo:02
# 2026-2
# Andrade Pinto Brandon Mihali
# Esquivel Vargas Carlos Andres
# Pozos Hernandez Angel
# Torres Pimentel Obed

def crear_matriz(llave):
    # 1. Limpiamos la llave: mayúsculas, J por I y quitamos espacios en blanco
    llave = llave.upper().replace("J", "I").replace(" ", "")
    
    alfabeto = "ABCDEFGHIKLMNOPQRSTUVWXYZ" # Alfabeto de 25 letras (sin J)
    alfabeto_llave = ""
    
    # 2. Construir secuencia única: letras de la llave + resto del alfabeto
    for letra in llave + alfabeto:
        if letra not in alfabeto_llave and letra in alfabeto:
            alfabeto_llave += letra
            
    # 3. Convertir la lista plana en una matriz de 5x5
    matriz = [list(alfabeto_llave[i:i+5]) for i in range(0, 25, 5)]
    return matriz

def obtener_Digrafos(mensaje):
    # 1. Limpieza: Mayúsculas, sin espacios y J por I
    mensaje = mensaje.upper().replace(" ", "").replace("J", "I")
    
    digrafos = []
    i = 0
    
    while i < len(mensaje):
        letra1 = mensaje[i]
        
        # Caso A: Si es la última letra del mensaje (no hay par)
        if i + 1 == len(mensaje):
            digrafos.append(letra1 + "X")
            i += 1
        else:
            letra2 = mensaje[i + 1]
            
            # Caso B: Si las dos letras seguidas son iguales
            if letra1 == letra2:
                digrafos.append(letra1 + "X")
                i += 1 # Solo avanzamos uno para no perder la letra repetida
            
            # Caso C: Son letras diferentes
            else:
                digrafos.append(letra1 + letra2)
                i += 2 # Avanzamos dos para el siguiente par
                
    return digrafos
        
def printMatriz(matriz):
    print("\n------- TABLERO PLAYFAIR -------")
    for fila in matriz:
        # Si la letra es 'I', mostramos 'I/J', si no, la letra normal
        fila_visual = [("I/J" if letra == "I" else letra) for letra in fila]
        # Ajustamos el espaciado (center) para que el "I/J" no mueva las columnas
        print("  ".join([celda.center(5) for celda in fila_visual]))
    print("---------------------------------\n")

def buscar_posicion(matriz, letra):
    # Buscamos la fila y columna de la letra (recordando que J es I)
    objetivo = "I" if letra == "J" else letra
    for r in range(5):
        for c in range(5):
            if matriz[r][c] == objetivo:
                return r, c
    return None

def Playfair(matriz, mensaje):
    digrafos = obtener_Digrafos(mensaje)
    texto_cifrado = ""
    
    for par in digrafos:
        # 1. Obtener coordenadas de ambas letras
        r1, c1 = buscar_posicion(matriz, par[0])
        r2, c2 = buscar_posicion(matriz, par[1])
        
        # REGLA 1: Misma Fila (se mueven a la derecha)
        if r1 == r2:
            texto_cifrado += matriz[r1][(c1 + 1) % 5]
            texto_cifrado += matriz[r2][(c2 + 1) % 5]
            
        # REGLA 2: Misma Columna (se mueven hacia abajo)
        elif c1 == c2:
            texto_cifrado += matriz[(r1 + 1) % 5][c1]
            texto_cifrado += matriz[(r2 + 1) % 5][c2]
            
        # REGLA 3: Rectángulo (intercambian columnas)
        else:
            texto_cifrado += matriz[r1][c2]
            texto_cifrado += matriz[r2][c1]
            
    return texto_cifrado

def descifrado_Playfair(matriz, msj_cifrado):
    digrafos = obtener_Digrafos(msj_cifrado)
    
    texto_descifrado = ""
    
    for par in digrafos:
        r1, c1 = buscar_posicion(matriz, par[0])
        r2, c2 = buscar_posicion(matriz, par[1])
        
        # REGLA 1: Misma Fila -> Mover a la IZQUIERDA (retroceder columna)
        if r1 == r2:
            texto_descifrado += matriz[r1][(c1 - 1) % 5]
            texto_descifrado += matriz[r2][(c2 - 1) % 5]
            
        # REGLA 2: Misma Columna -> Mover hacia ARRIBA (retroceder fila)
        elif c1 == c2:
            texto_descifrado += matriz[(r1 - 1) % 5][c1]
            texto_descifrado += matriz[(r2 - 1) % 5][c2]
            
        # REGLA 3: Rectángulo -> Intercambio de columnas
        else:
            texto_descifrado += matriz[r1][c2]
            texto_descifrado += matriz[r2][c1]
            
    return texto_descifrado

if __name__ == "__main__":
    print("--------------- Cifrado Playfair ---------------\n\n")
    M = input("Ingresa el mensaje M: ")
    K = input("  Ingresa la clave K: ")
    matriz = crear_matriz(K)
    printMatriz(matriz)
    C = Playfair(matriz, M)
    print("Digrafos: ", obtener_Digrafos(M))
    print("Playfair: ", obtener_Digrafos(C))
    print("\nMensaje Cifrado C: ", C)

    print("\n\n-------------- Descifrado Playfair -------------\n\n")
    print("Mensaje Cifrado: ", C)
    print("          Clave: ", K)
    msjDescifrado = descifrado_Playfair(matriz, C)
    print("\n\nDigrafos del mensaje cifrado: ", obtener_Digrafos(C))
    print("                    Playfair: ", obtener_Digrafos(msjDescifrado))
    print("\n\nMensaje Descifrado: ", msjDescifrado)
