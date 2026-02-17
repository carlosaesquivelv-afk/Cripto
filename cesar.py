# Universidad Nacional Atonoma de Mexico
# Criptografia Grupo:02
# 2026-2
# Andrade Pinto Brandon Mihali
# Esquivel Vargas Carlos Andres
# Pozos Hernandez Angel
# Torres Pimentel Obed

def cifrado_cesar():
    """
    Realiza el cifrado César para un mensaje dado.
    """
    lenguaje = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    mapeo = {letra: i for i, letra in enumerate(lenguaje)}

    print("L:", end=" ")
    # Imprime las letras del lenguaje
    for letra in lenguaje:
        print(f"{letra:<4}", end="")
    print()

    print("  ", end=" ")
    # Imprime los valores numéricos alineados
    for i in range(len(lenguaje)):
        print(f"{i:<4}", end="")
    print()

    # --- Solicitar datos al usuario ---
    while True:
        try:
            key = int(input("K: "))
            break
        except ValueError:
            print("X Por favor, ingrese un número entero para el key.")

    mensaje = input('Mensaje: ').upper()

    # --- Cifrar el mensaje ---
    mensaje_cifrado = ""
    for caracter in mensaje:
        if caracter in mapeo:
            indice_original = mapeo[caracter]
            nuevo_indice = (indice_original + key) % len(lenguaje)
            caracter_cifrado = lenguaje[nuevo_indice]
            mensaje_cifrado += caracter_cifrado
        else:
            mensaje_cifrado += caracter

    # --- Mostrar el resultado ---
    print(f"C: {mensaje_cifrado}")

# Ejecutar el programa
print("Cifrado Cesar")
cifrado_cesar()