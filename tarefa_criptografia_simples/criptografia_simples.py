import math
import hashlib

def totient(n):
    resultado = 0
    for i in range(1, n):
        if math.gcd(i, n) == 1:
            resultado += 1
    return resultado

def cifrar(mensagem, chave):
    phi = totient(chave)
    cifrado = ""
    for char in mensagem:
        valor = ord(char)
        cifrado += chr((valor * phi) % 255)
    return cifrado

def decifrar(mensagem_cifrada, chave):
    phi = totient(chave)
    for inv in range(1, 255):
        if (phi * inv) % 255 == 1:
            break
    
    decifrado = ""
    for char in mensagem_cifrada:
        valor = ord(char)
        decifrado += chr((valor * inv) % 255)
    return decifrado

def calcular_hash(mensagem):
    return hashlib.md5(mensagem.encode()).hexdigest()

def gerar_chave(num1, num2):
    return num1 * num2

def executar_programa():

    num1 = int(input("número 1:"))
    num2 = int(input("número 2: "))
    chave = gerar_chave(num1, num2)

    print(f"Chave gerada: {chave}")
    mensagem = input("Digite uma mensagem: ")

    print("\nCifrando mensagem...")
    mensagem_cifrada = cifrar(mensagem, chave)
    print(f"Mensagem cifrada: {mensagem_cifrada}")

    print("\nDecifrando mensagem...")
    mensagem_decifrada = decifrar(mensagem_cifrada, chave)
    print(f"Mensagem decifrada: {mensagem_decifrada}")

    print("\nGerando hash...")
    hash_original = calcular_hash(mensagem)
    hash_decifrado = calcular_hash(mensagem_decifrada)
    print(f"Hash original: {hash_original}")
    print(f"Hash decifrado: {hash_decifrado}")

    if hash_original == hash_decifrado:
        print("Verificação: SUCESSO! Os hashes são idênticos.")
    else:
        print("Verificação: FALHA! Os hashes são diferentes.")

if __name__ == "__main__":
    executar_programa()
