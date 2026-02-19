# Universidad Nacional Atonoma de Mexico
# Criptografia Grupo:02
# 2026-2
# Andrade Pinto Brandon Mihali
# Esquivel Vargas Carlos Andres
# Pozos Hernandez Angel
# Torres Pimentel Obed

def cifrado_vigenere():
    """
    Realiza el cifrado y descifrado de Vigenère para un mensaje y una clave dados en español.
    """
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    mapeo = {letra: i for i, letra in enumerate(alfabeto)}

    # Solicitar clave y mensaje
    print("---------------------CIFRADO VIGENERE---------------------")
    mensaje = input("Mensaje (M): ").upper().replace(" ", "")
    clave_original = input("clave (K): ").upper().replace(" ", "")

    # Validar que la clave y el mensaje solo contengan letras del alfabeto
    if not all(c in alfabeto for c in clave_original):
        print("❌ Error: La clave debe contener solo letras del alfabeto.")
        return
    if not all(c in alfabeto for c in mensaje):
        print("❌ Error: El mensaje debe contener solo letras del alfabeto.")
        return

    # Extender la clave para que coincida con la longitud del mensaje
    #Generador de clave
    clave = (clave_original * (len(mensaje) // len(clave_original))) + clave_original[:len(mensaje) % len(clave_original)]

    # --- Impresión del proceso de Cifrado ---
    print("\n--- PROCESO DE CIFRADO ---")
    print("A:", end=" ")
    for letra in alfabeto:
        print(f"{letra:<4}", end="")
    print()
    print("  ", end=" ")
    for i in range(len(alfabeto)):
        print(f"{i:<4}", end="")
    print()
    
    print("-" * (len(alfabeto) * 4 + 3))

    # Clave (K) y sus valores
    print("Km:", end=" ")
    for letra_clave in clave:
        print(f"{letra_clave:<4}", end="")
    print()
    print("  ", end=" ")
    for letra_clave in clave:
        print(f"{mapeo[letra_clave]:<4}", end="")
    print()

    print("-" * (len(alfabeto) * 4 + 3))

    # Mensaje (M) y sus valores
    print("M:", end=" ")
    for letra_mensaje in mensaje:
        print(f"{letra_mensaje:<4}", end="")
    print()
    print("  ", end=" ")
    valores_mensaje = [mapeo[letra] for letra in mensaje]
    for valor in valores_mensaje:
        print(f"{valor:<4}", end="")
    print()

    print("-" * (len(alfabeto) * 4 + 3))

    # Suma de valores
    print("  ", end=" ")
    valores_clave = [mapeo[letra] for letra in clave]
    suma_valores = [(valores_mensaje[i] + valores_clave[i]) for i in range(len(mensaje))]
    for suma in suma_valores:
        print(f"{suma:<4}", end="")
    print(" suma")

    # Módulo (26)
    print("  ", end=" ")
    mod_valores = [suma % len(alfabeto) for suma in suma_valores]
    for mod in mod_valores:
        print(f"{mod:<4}", end="")
    print(" mod(26)")

    print("-" * (len(alfabeto) * 4 + 3))

    # Mensaje Cifrado (C)
    print("C:", end=" ")
    mensaje_cifrado = ""
    for mod in mod_valores:
        letra_cifrada = alfabeto[mod]
        mensaje_cifrado += letra_cifrada
        print(f"{letra_cifrada:<4}", end="")
    print()
    
    # --- PROCESO DE DESCIFRADO ---
    
    print("\n--- PROCESO DE DESCIFRADO ---")
    
    # Mensaje Cifrado (C) y sus valores
    print("C:", end=" ")
    for letra_cifrada in mensaje_cifrado:
        print(f"{letra_cifrada:<4}", end="")
    print()
    print("  ", end=" ")
    for mod in mod_valores:
        print(f"{mod:<4}", end="")
    print()
    
    print("-" * (len(alfabeto) * 4 + 3))
    
    # Clave (K) y sus valores
    print("K:", end=" ")
    for letra_clave in clave:
        print(f"{letra_clave:<4}", end="")
    print()
    print("  ", end=" ")
    for letra_clave in clave:
        print(f"{mapeo[letra_clave]:<4}", end="")
    print()
    
    print("-" * (len(alfabeto) * 4 + 3))
    
    # Resta de valores
    print("  ", end=" ")
    resta_valores = [(mod_valores[i] - valores_clave[i]) for i in range(len(mensaje_cifrado))]
    for resta in resta_valores:
        print(f"{resta:<4}", end="")
    print(" resta")
    
    # Módulo (26) de la resta
    print("  ", end=" ")
    descifrado_mod_valores = [resta % len(alfabeto) for resta in resta_valores]
    for mod in descifrado_mod_valores:
        print(f"{mod:<4}", end="")
    print(" mod(26)")
    
    print("-" * (len(alfabeto) * 4 + 3))
    
    # Mensaje Original (M)
    print("M:", end=" ")
    mensaje_descifrado = ""
    for mod in descifrado_mod_valores:
        letra_original = alfabeto[mod]
        mensaje_descifrado += letra_original
        print(f"{letra_original:<4}", end="")
    print()

# Ejecutar el programa
cifrado_vigenere()