# Visualizador de Árvore Binária de Busca (BST) 

Projeto de modernização, refatoração e expansão funcional de um visualizador interativo de Árvore Binária de Busca (BST) desenvolvido em Python. 

---

## Sumário
* [Créditos e Origem do Código](#créditos-e-origem-do-código)
* [Fundamentação Teórica e Inovações](#fundamentação-teórica-e-inovações)
* [Comparativo: Código Antigo vs. Reformulado](#comparativo-código-antigo-vs-código-reformulado)
* [Análise de Limitações Didáticas e Técnicas](#análise-de-limitações-didáticas-e-técnicas)
* [Download e Execução do Programa (.exe)](#download-e-execução-do-programa-exe)
* [Executando via Código Fonte](#executando-via-código-fonte)
  
---
## Créditos e Origem do Código

Este projeto foi desenvolvido como uma evolução aprimorada a partir do código aberto original:
* **Repositório Base:** [binary-search-tree-visualizer](https://github.com/samarpancoder2002/binary-search-tree-visualizer) por **samarpancoder2002**.

A versão original foi totalmente reformulada para corrigir limitações estruturais rígidas, eliminar sobreposições de renderização e introduzir recursos avançados de análise de dados.

---

## Fundamentação Teórica e Inovações

A **Árvore Binária de Busca (BST)** é uma estrutura de dados hierárquica que mantém a propriedade de ordenação: para qualquer nó $N$, todos os elementos na subárvore esquerda possuem valores estritamente menores ($V_{esq} < V_N$) e todos os elementos na subárvore direita possuem valores estritamente maiores ($V_{dir} > V_N$).
A **Árvore AVL(balanceada pela altura)** é outra estrutura de dados que traz maior eficiência na complexidade de tempo por gerar balanceamento com rotações. Ela impede que a árvore se degenere em lista encadeada e diminui a altura da árvore em no máximo 1. 

### O Rigor Teórico das Inovações Aplicadas:

1. **Disposição Espacial Dinâmica via Caminhamento Em-Ordem (*In-Order Traversal*):**
   * *O Problema:* Em BSTs puras, o desbalanceamento pode criar ramificações profundas. Métodos ingênuos de renderização dividem o espaço por potências de 2 ($X / 2^k$), o que causa colisão espacial acelerada.
   * *A Solução:* Implementou-se um algoritmo de disposição baseado no caminhamento Em-Ordem. A posição no eixo $X$ de cada nó é derivada diretamente do seu índice ordenado na sequência ($1º, 2º, \dots, Nº$ nó), garantindo **zero sobreposição espacial**, independentemente do formato ou profundidade da árvore.

2. **Demonstração Didática de Casos Limite (Degeneração em Lista Encadeada):**
   * Permite gerar dados em ordem estritamente crescente ou decrescente, demonstrando o comportamento do pior caso da BST ($O(n)$ em altura), onde a árvore se degenera em uma lista encadeada.

3. **Operações de Aproximação de Limites (*Floor* e *Ceil*):**
   * Além da busca exata ($O(h)$), a ferramenta executa a busca por valores aproximados na ausência da chave exata:
     * **Piso (*Floor*):** O maior elemento na árvore que é $\le$ ao valor buscado.
     * **Teto (*Ceil*):** O menor elemento na árvore que é $\ge$ ao valor buscado.

---

## Comparativo: Código Antigo vs. Código Reformulado

| Aspecto | Código Original (Base) | Código Reformulado (Atual) |
| :--- | :--- | :--- |
| **Arquitetura de Telas** | Coordenadas e janelas com posições travadas. | Layout responsivo e moderno com `CustomTkinter`. |
| **Profundidade Máxima** | Restrito a 4 níveis (lançava aviso e travava). | **Níveis ilimitados** através de recursão pura. |
| **Cálculo de Layout** | Divisão fixa de tela (colisão visual no 3º nível). | **Eixo X dinâmico** por caminhamento Em-Ordem. |
| **Navegação** | Estática (sem navegação). | **Pan & Zoom** (arraste com mouse e scroll). |
| **Dependências** | Módulo externo rígido (`Circular_queue.py`). | **Arquivo único independente** (sem dependências externas). |
| **Entrada de Dados** | Caixas de texto fixas no painel principal. | Diálogos modais sob demanda (`CTkInputDialog`). |
| **Interatividade** | Somente via botões da interface. | Clique direto no nó + remoção por teclado (`Delete`). |
| **Inclusão em Massa** | Apenas inserção individual manual. | Gerador automático de 1 a 99 nós (Aleatório/Crescente/Decrescente). |
| Apenas **Árvore BST** | Árvore Binária de Busca com complexidade O(n) na maioria dos casos | Árvore BST + Árvore AVL com complexidade de tempo O(log n) na maioria dos casos com rotações de balanceamento |
| **Idiomas e Localização** | Inglês com nomenclaturas mistas. | **Português (pt-BR)** padronizado. |

---

## Análise de Limitações Didáticas e Técnicas

### 1. Limitações do Código Original (Superadas)
* **Limitação Didática:** Impedia o estudante de visualizar o comportamento da estrutura de dados ao atingir profundidades maiores que 4 níveis ou em casos de degeneração.
* **Limitação Técnica:** Forte acoplamento entre a lógica de negócio e a interface gráfica (manipulação direta de elementos do `Canvas` misturada com estruturas de dados em listas de listas).
* **Limitação Técnica:** Tinha apenas a árvore simples de busca binária na mecânica original do jogo. Foi implementada a opção de switch que gera uma AVL.

### 2. Limitações da Versão Atual (Trabalhos Futuros)
* **Limitação Didática:** Árvores puras muito profundas exigem uso frequente do Zoom/Pan.
* **Limitação Técnica:** A biblioteca `Tkinter/CustomTkinter` utiliza renderização baseada em CPU sem aceleração por hardware, o que pode impactar a taxa de quadros nas animações de percurso em árvores com centenas de nós simultâneos.

---

## Download e Execução do Programa (.exe)

Para rodar o programa sem precisar instalar o Python ou configurar bibliotecas:

1. Acesse a aba **Releases** na barra lateral direita do GitHub.
2. Na Release mais recente, vá até a seção **Assets** e faça o download do arquivo executável (`.exe`).
3. Abra o arquivo baixado no seu computador.
4. **Aviso do Windows Defender (SmartScreen):** Por se tratar de um executável independente que não possui assinatura digital paga, o Windows pode exibir uma tela azul de proteção. Para abrir normalmente:
   * Clique em **"Mais informações"**.
   * Em seguida, clique no botão **"Executar mesmo assim"**.

---

## Executando via Código Fonte

Caso prefira rodar ou modificar o projeto diretamente em Python:

### Pré-requisitos
* Python 3.x
* Módulo CustomTkinter (`pip install customtkinter`)

### Execução Direta
```bash
python visualizador_arvore.py
```
## Compilando o Próprio Executável (.exe)
### Para gerar um executável único via PowerShell:
```bash
python -m pyinstaller --noconfirm --onefile --windowed --add-data "CAMINHO_DO_CUSTOMTKINTER;customtkinter/" visualizador_arvore.py
```
(O executável compilado estará disponível na pasta dist/)
