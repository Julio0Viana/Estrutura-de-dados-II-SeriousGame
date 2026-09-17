# Visualizador de Árvore Binária de Busca (BST)

Projeto de modernização, refatoração e expansão funcional de um visualizador interativo de Árvore Binária de Busca (BST) desenvolvido em Python. 

---

## Créditos e Origem do Código

Este projeto foi desenvolvido como uma evolução aprimorada a partir do código aberto original:
* **Repositório Base:** [binary-search-tree-visualizer](https://github.com/samarpancoder2002/binary-search-tree-visualizer) por **samarpancoder2002**.

A versão original foi totalmente reformulada para corrigir limitações estruturais rígidas, eliminar sobreposições de renderização e introduzir recursos avançados de análise de dados.

---

## Fundamentação Teórica e Inovações

A **Árvore Binária de Busca (BST)** é uma estrutura de dados hierárquica que mantém a propriedade de ordenação: para qualquer nó $N$, todos os elementos na subárvore esquerda possuem valores estritamente menores ($V_{esq} < V_N$) e todos os elementos na subárvore direita possuem valores estritamente maiores ($V_{dir} > V_N$).

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
| **Idiomas e Localização** | Inglês com nomenclaturas mistas. | **Português (pt-BR)** padronizado. |

---

## Análise de LimitaçõesDidáticas e Técnicas

### 1. Limitações do Código Original (Superadas)
* **Limitação Didática:** Impedia o estudante de visualizar o comportamento da estrutura de dados ao atingir profundidades maiores que 4 níveis ou em casos de degeneração.
* **Limitação Técnica:** Forte acoplamento entre a lógica de negócio e a interface gráfica (manipulação direta de elementos do `Canvas` misturada com estruturas de dados em listas de listas).

### 2. Limitações da Versão Atual (Trabalhos Futuros)
* **Limitação Didática:** Por ser uma BST pura, ela não realiza rotações automáticas para balanceamento (como árvores AVL ou Red-Black). Árvores puras muito profundas exigem uso frequente do Zoom/Pan.
* **Limitação Técnica:** A biblioteca `Tkinter/CustomTkinter` utiliza renderização baseada em CPU sem aceleração por hardware, o que pode impactar a taxa de quadros nas animações de percurso em árvores com centenas de nós simultâneos.

---

### Execução Direta
```bash
python visualizador_arvore.py
