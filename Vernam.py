# Universidad Nacional Atonoma de Mexico
# Criptografia Grupo:02
# 2026-2
# Andrade Pinto Brandon Mihali
# Esquivel Vargas Carlos Andres
# Pozos Hernandez Angel
# Torres Pimentel Obed

import random
import string

def generar_clave(tamano):
    """Genera una clave aleatoria de letras (mayúsculas y minúsculas)."""
    letras = string.ascii_letters
    return ''.join(random.choice(letras) for _ in range(tamano))

def a_binario(val):
    """Convierte un entero a representación binaria de 8 bits."""
    return bin(val)[2:].zfill(8)

def a_hex(val):
    """Convierte un valor a hexadecimal de 2 dígitos."""
    return hex(val)[2:].upper().zfill(2)

def obtener_char_seguro(cod_ascii):
    """Retorna el carácter si es printable, de lo contrario un espacio en blanco."""
    try:
        if 0 <= cod_ascii <= 1114111:
            c = chr(cod_ascii)
            return c if c.isprintable() else " "
    except:
        pass
    return " "

def print_table(datos, modo):
    """Muestra la tabla con el orden de columnas solicitado por el usuario."""
    header0 = " Clave |          |     |          |   Mensaje   | Resultado de |   Mensaje  |      "
    header1 = "  (K)  |  Bin_K   | XOR |  Bin_C   | Cifrado (C) |  XOR (Bin_M) | Caracter M | Hex_M"
    header2 = "  (K)  |  Bin_K   | XOR |  Bin_M   |     (M)     |  XOR (Bin_C) | Cifrado(C) | Hex_C"
    print("\n" + "-" * len(header0))
    print(header0)
    if modo == "D": print(header1)
    if modo == "C": print(header2) 
    print("-" * len(header0))
    for d in datos:
        # Formateo de columnas para que queden alineadas
        k_char = d['k_char']
        bin_k = d['bin_k']
        bin_c = d['bin_c']
        c_char = d['c_char']
        bin_m = d['bin_m']
        m_char = d['m_char']
        hex_m = d['hex_m']
        hex_c = d['hex_c']
        if modo == "D":
            print(f"   {k_char}   | {bin_k} |  ^  | {bin_c} |      {c_char}      |   {bin_m}   |     {m_char}      |  {hex_m}")
        if modo == "C":
            print(f"   {k_char}   | {bin_k} |  ^  | {bin_m} |      {m_char}      |   {bin_c}   |     {c_char}      |  {hex_c}")
    print("-" * len(header0))

def ejecutar_cifrado(): 
    print("\n----------------------- Cifrado ---------------------------")
    mensaje_texto = input("Ingrese Mensaje (M): ")
    clave = generar_clave(len(mensaje_texto))
    print(f"Clave generada (K): {clave}")

    datos = []
    for m_char, k_char in zip(mensaje_texto, clave):
        m_val = ord(m_char)
        k_val = ord(k_char)
        c_val = m_val ^ k_val
        
        datos.append({
            'k_char': k_char, 'bin_k': a_binario(k_val),
            'm_char': m_char, 'bin_m': a_binario(m_val),
            'bin_c': a_binario(c_val), 'c_char': obtener_char_seguro(c_val),
            'hex_c': a_hex(c_val), 'ascii_c': c_val, 'ascii_m': m_val, 'hex_m': a_hex(m_val)
        })

    if input("\nDesea ver el proceso del cifrado (Y/N): ").upper() == 'Y':
        print_table(datos, 'C')

    print("\n--- RESULTADO FINAL (CIFRADO) ---")
    print(f"Mensaje (M):        {mensaje_texto}")
    print(f"Mensaje (ASCII):    {' '.join(str(d['ascii_m']) for d in datos)}")
    print(f"Mensaje (Hex):      {' '.join(d['hex_m'] for d in datos)}")
    print(f"Clave (K):          {clave}")
    print(f"Cifrado (ASCII):    {' '.join(str(d['ascii_c']) for d in datos)}")
    print(f"Cifrado (Hex):      {' '.join(d['hex_c'] for d in datos)}")
    print(f"Cifrado (Caracter): {''.join(d['c_char'] for d in datos)}")

def ejecutar_descifrado():
    print("\n---------------------- Descifrado --------------------------")
    modo = input("Ingresar el mensaje como texto (T) o con valores ASCII (A): ").upper()
    
    c_vals = []
    if modo == 'A':
        entrada = input("Ingrese los valores ASCII del cifrado separados por espacios: ")
        try:
            c_vals = [int(x) for x in entrada.split()]
        except ValueError:
            print("Error: Ingrese solo números válidos.")
            return
    else:
        entrada = input("Ingrese el texto cifrado (C): ")
        c_vals = [ord(c) for c in entrada]

    while True:
        clave = input(f"Ingrese la Clave (K) de {len(c_vals)} caracteres: ")
        if len(clave) == len(c_vals):
            break
        print(f"Error: La clave debe tener exactamente {len(c_vals)} caracteres.")

    datos = []
    mensaje_recuperado = ""
    for c_val, k_char in zip(c_vals, clave):
        k_val = ord(k_char)
        m_val = c_val ^ k_val  # Operación inversa: C XOR K = M
        m_char = obtener_char_seguro(m_val)
        mensaje_recuperado += m_char
        
        datos.append({
            'k_char': k_char, 'bin_k': a_binario(k_val),
            'm_char': m_char, 'bin_m': a_binario(m_val),
            'bin_c': a_binario(c_val), 'c_char': obtener_char_seguro(c_val),
            'hex_c': a_hex(c_val), 'ascii_c': c_val, 'ascii_m': m_val, 'hex_m': a_hex(m_val)
        })

    if input("\nDesea ver el proceso del descifrado (Y/N): ").upper() == 'Y':
        print_table(datos, 'D')

    print("\n--- RESULTADO FINAL (DESCIFRADO) ---")
    print(f"Mensaje (M):        {mensaje_recuperado}")
    print(f"Mensaje (ASCII):    {' '.join(str(d['ascii_m']) for d in datos)}")
    print(f"Mensaje (Hex):      {' '.join(d['hex_m'] for d in datos)}")
    print(f"Clave (K):          {clave}")
    print(f"Cifrado (ASCII):    {' '.join(str(d['ascii_c']) for d in datos)}")
    print(f"Cifrado (Hex):      {' '.join(d['hex_c'] for d in datos)}")
    print(f"Cifrado (Caracter): {''.join(d['c_char'] for d in datos)}")

def main():
    while True:
        print("\n----------------------Cifrado Vernam--------------------")
        opcion = input("Desea cifrar o descifrar un mensaje (C/D): ").upper()

        if opcion == 'C':
            ejecutar_cifrado()
        elif opcion == 'D':
            ejecutar_descifrado()
        else:
            print("Opción no válida.")

        salir = input("\n¿Desea salir presionando S o quiere volver a cifrar/descifrar (S/Enter)? ").upper()
        if salir == 'S':
            print("Finalizando programa...")
            break

if __name__ == "__main__":
    main()