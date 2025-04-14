
---

# 🔐 Criptografia com Totiente de Euler

Este projeto é uma implementação simples de criptografia baseada no **Totiente de Euler**, com suporte para **cifragem, decifragem e verificação de integridade** via hash MD5.

---

## 📜 Descrição

O programa permite que o usuário:

1. **Informe dois números inteiros** para gerar uma chave de criptografia.
2. **Digite uma mensagem** para ser cifrada.
3. Veja a **mensagem cifrada e decifrada**.
4. Confira a **verificação de integridade** usando hashes MD5.

---

## 🧮 Como Funciona

- **Totiente de Euler (`φ(n)`)**: Calculado com base na chave gerada pelo produto dos dois números informados. Ele determina a quantidade de inteiros positivos menores que `n` que são coprimos com `n`.

- **Cifragem**: Cada caractere da mensagem é convertido com base na fórmula `(ord(char) * φ(chave)) % 255`.

- **Decifragem**: Utiliza o inverso modular de `φ(chave)` módulo 255 para recuperar a mensagem original.

- **Hash MD5**: Garante que a mensagem original e a decifrada sejam idênticas.

---

## 📁 Estrutura do Código

O código está modularizado com as seguintes funções:

| Função                  | Descrição |
|-------------------------|-----------|
| `totient(n)`            | Calcula o totiente de Euler para o número `n`. |
| `cifrar(mensagem, chave)`   | Cifra a mensagem com base na chave fornecida. |
| `decifrar(mensagem_cifrada, chave)` | Decifra a mensagem usando a chave. |
| `calcular_hash(mensagem)` | Gera o hash MD5 da mensagem. |
| `gerar_chave(num1, num2)` | Gera a chave multiplicando os dois números fornecidos. |
| `executar_programa()`     | Função principal que roda toda a lógica do programa. |

---

## ▶️ Como Executar

### Pré-requisitos
- Python 3 instalado

### Executando o script

```bash
python criptografia_totiente.py
```

Você será guiado pelo terminal com as seguintes etapas:
1. Inserir dois números para gerar a chave.
2. Inserir a mensagem que deseja cifrar.
3. Visualizar o resultado cifrado e decifrado.
4. Verificar se os hashes coincidem.

---

## ✅ Exemplo de Execução

```
Digite o primeiro número: 5
Digite o segundo número: 7
Chave gerada: 35

Digite a mensagem a ser cifrada: ola

Mensagem cifrada: ýìý
Mensagem decifrada: ola

Hash original: 8f14e45fceea167a5a36dedd4bea2543
Hash decifrado: 8f14e45fceea167a5a36dedd4bea2543

Verificação: SUCESSO! Os hashes são idênticos.
```

---

## 📌 Observações

- Esta implementação **não é adequada para criptografia real**, pois não possui mecanismos robustos de segurança. É um exemplo **educacional** para mostrar conceitos matemáticos e programação funcional.
- A função de inverso modular usada aqui é simplificada e só funciona corretamente para números pequenos.

---

## 📄 Licença

Este projeto é de uso livre para fins educacionais. ✌️

---