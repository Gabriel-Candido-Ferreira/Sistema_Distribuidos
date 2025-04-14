# 📘 Comparativo: Algoritmos de Exclusão Mútua Distribuída

## 🔄 Tabela Comparativa

| Critério                          | Ricart & Agrawala                          | Algoritmo do Anel                          | Ambos                                      |
|----------------------------------|--------------------------------------------|--------------------------------------------|--------------------------------------------|
| Tipo de algoritmo                | Baseado em mensagens diretas              | Baseado em passagem de um token            | Exclusão mútua distribuída                 |
| Modelo de comunicação            | Multicast para todos os processos         | Comunicação por token em anel lógico       | Comunicação entre processos                |
| Token                            | ❌ Não utiliza                             | ✅ Utiliza                                 | -                                          |
| Ordem lógica                     | Timestamps (Lamport)                      | Ordem do anel                             | Usam alguma forma de ordenação             |
| Mensagens por entrada na CS      | 2(N−1) mensagens                          | 1 mensagem (token)                         | Requer troca de mensagens                  |
| Tolerância a falhas              | Baixa (um processo travado afeta todos)  | Média (token pode ser regenerado)         | Sensível a falhas                          |
| Prioridade de acesso             | Por timestamps                            | Por posição no anel                       | Controle de acesso à CS                    |
| Sincronização                    | Requer sincronização de relógios lógicos | Estrutura fixa de anel                     | Exige algum tipo de coordenação            |
| Desempenho em redes grandes      | Baixo desempenho                          | Bom desempenho                             | Limitados por escala                      |
| Complexidade de implementação    | Alta                                      | Baixa a moderada                          | Requer conhecimento em sistemas distribuídos |

## 🔍 Características Exclusivas

### ✅ Somente Ricart & Agrawala

- Baseado em **timestamp de Lamport** para ordenação.
- Requere **confirmação de todos os processos** antes de entrar na CS.
- **Número elevado de mensagens**.
- Funciona em topologias **arbitrárias**.

### ✅ Somente Algoritmo do Anel

- Utiliza um **token exclusivo** que circula entre os processos.
- Apenas o processo que possui o **token** pode acessar a CS.
- **Baixo tráfego de mensagens**.
- Requer estrutura de **anel lógico**.



