import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import time
import random

# Retorno ao Tema Escuro
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class NoArvore:
    """Representação de cada Nó da BST."""
    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None
        self.x = 0
        self.y = 0


class JanelaGeracaoMassa(ctk.CTkToplevel):
    """Popup para inserção de múltiplos nós."""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Gerar Vários Nós")
        self.geometry("400x350")
        self.resizable(False, False)
        self.grab_set()
        self._criar_widgets()

    def _criar_widgets(self):
        ctk.CTkLabel(self, text="Gerar Múltiplos Nós", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 10))
        
        ctk.CTkLabel(self, text="Quantidade de nós (1 a 99):", font=ctk.CTkFont(size=13)).pack(pady=(5, 0))
        self.entrada_qtd = ctk.CTkEntry(self, placeholder_text="Ex: 15", width=150)
        self.entrada_qtd.pack(pady=(0, 15))

        ctk.CTkLabel(self, text="Modo de geração dos números:", font=ctk.CTkFont(size=13)).pack(pady=(5, 5))
        self.var_modo = ctk.StringVar(value="randomico")

        ctk.CTkRadioButton(self, text="1 - Randômicos", variable=self.var_modo, value="randomico").pack(anchor="w", padx=100, pady=4)
        ctk.CTkRadioButton(self, text="2 - Crescentes", variable=self.var_modo, value="crescente").pack(anchor="w", padx=100, pady=4)
        ctk.CTkRadioButton(self, text="3 - Decrescentes", variable=self.var_modo, value="decrescente").pack(anchor="w", padx=100, pady=4)

        btn_confirmar = ctk.CTkButton(self, text="Gerar e Inserir", command=self._confirmar, fg_color="#2EA043", hover_color="#238636")
        btn_confirmar.pack(pady=20)

    def _confirmar(self):
        qtd_str = self.entrada_qtd.get().strip()
        if not qtd_str.isdigit() or not (1 <= int(qtd_str) <= 99):
            messagebox.showerror("Erro", "Digite um valor válido de 1 a 99.", parent=self)
            return

        self.parent.gerar_nos_em_massa(int(qtd_str), self.var_modo.get())
        self.destroy()


class JanelaBuscaAvancada(ctk.CTkToplevel):
    """Popup para busca com tolerância."""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Busca Avançada na Árvore")
        self.geometry("400x320")
        self.resizable(False, False)
        self.grab_set()
        self._criar_widgets()

    def _criar_widgets(self):
        ctk.CTkLabel(self, text="Buscar Valor na Árvore", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 10))

        ctk.CTkLabel(self, text="Número a buscar:", font=ctk.CTkFont(size=13)).pack(pady=(5, 0))
        self.entrada_valor = ctk.CTkEntry(self, placeholder_text="Ex: 42", width=150)
        self.entrada_valor.pack(pady=(0, 15))

        ctk.CTkLabel(self, text="Se o valor exato NÃO for encontrado:", font=ctk.CTkFont(size=13)).pack(pady=(5, 5))
        self.var_tolerancia = ctk.StringVar(value="exato")

        ctk.CTkRadioButton(self, text="Exigir valor exato", variable=self.var_tolerancia, value="exato").pack(anchor="w", padx=80, pady=3)
        ctk.CTkRadioButton(self, text="Mais próximo MENOR (Piso/Floor)", variable=self.var_tolerancia, value="menor").pack(anchor="w", padx=80, pady=3)
        ctk.CTkRadioButton(self, text="Mais próximo MAIOR (Teto/Ceil)", variable=self.var_tolerancia, value="maior").pack(anchor="w", padx=80, pady=3)

        btn_buscar = ctk.CTkButton(self, text="Executar Busca", command=self._buscar, fg_color="#1F6FE5", hover_color="#1158BE")
        btn_buscar.pack(pady=20)

    def _buscar(self):
        val_str = self.entrada_valor.get().strip()
        if not val_str.lstrip('-').isdigit():
            messagebox.showerror("Erro", "Insira um número inteiro válido.", parent=self)
            return

        self.parent.executar_busca_avancada(int(val_str), self.var_tolerancia.get())
        self.destroy()


class VisualizadorBST(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Visualizador de Árvore Binária de Busca (BST)")
        self.geometry("1250x780")
        self.minsize(1000, 600)

        self.raiz = None
        self.no_selecionado = None

        # Controle de Transformação da Câmera (Pan & Zoom)
        self.offset_x = 0
        self.offset_y = 0
        self.escala = 1.0
        self.drag_start_x = 0
        self.drag_start_y = 0

        # Estado da aba retrátil
        self.aba_percursos_aberta = False

        self._criar_layout()

    def _criar_layout(self):
        # Painel Lateral Esquerdo (Dark Mode)
        self.frame_controle = ctk.CTkFrame(self, width=300, corner_radius=15)
        self.frame_controle.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=15)

        ctk.CTkLabel(self.frame_controle, text="Painel de Controle", font=ctk.CTkFont(size=20, weight="bold")).pack(padx=20, pady=(20, 15))

        # Botões Principais de Edição da Árvore
        ctk.CTkButton(self.frame_controle, text="Inserir Nó", command=self.solicitar_insercao, fg_color="#2EA043", hover_color="#238636").pack(padx=20, pady=5, fill=tk.X)
        ctk.CTkButton(self.frame_controle, text="Remover Nó", command=self.solicitar_remocao, fg_color="#DA3633", hover_color="#B62324").pack(padx=20, pady=5, fill=tk.X)
        ctk.CTkButton(self.frame_controle, text="Gerar Vários Nós", command=lambda: JanelaGeracaoMassa(self), fg_color="#1F6FE5", hover_color="#1158BE").pack(padx=20, pady=5, fill=tk.X)
        ctk.CTkButton(self.frame_controle, text="Limpar Árvore", command=self.limpar_arvore, fg_color="#8B949E", hover_color="#6E7681").pack(padx=20, pady=(5, 15), fill=tk.X)

        # Divisor
        ctk.CTkFrame(self.frame_controle, height=2, fg_color="gray30").pack(fill=tk.X, padx=15, pady=5)

        # ABA RETRÁTIL COM SETINHA INDICADORA
        self.btn_toggle_percursos = ctk.CTkButton(
            self.frame_controle, 
            text="▶  Opções de Visualização", 
            command=self.toggle_aba_percursos,
            fg_color="transparent", 
            text_color="#58A6FF",
            hover_color="gray20",
            anchor="w",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.btn_toggle_percursos.pack(fill=tk.X, padx=15, pady=5)

        # Container interno das opções de visualização / busca
        self.frame_botoes_percurso = ctk.CTkFrame(self.frame_controle, fg_color="transparent")

        # Busca Avançada realocada para o grupo de visualização
        ctk.CTkButton(self.frame_botoes_percurso, text="Buscar Valor...", command=lambda: JanelaBuscaAvancada(self), fg_color="#D29922", hover_color="#BB861C").pack(padx=20, pady=4, fill=tk.X)
        ctk.CTkButton(self.frame_botoes_percurso, text="Pré-Ordem", command=lambda: self.executar_percurso("pre")).pack(padx=20, pady=3, fill=tk.X)
        ctk.CTkButton(self.frame_botoes_percurso, text="Em-Ordem", command=lambda: self.executar_percurso("em")).pack(padx=20, pady=3, fill=tk.X)
        ctk.CTkButton(self.frame_botoes_percurso, text="Pós-Ordem", command=lambda: self.executar_percurso("pos")).pack(padx=20, pady=3, fill=tk.X)
        ctk.CTkButton(self.frame_botoes_percurso, text="Em Nível", command=lambda: self.executar_percurso("nivel")).pack(padx=20, pady=3, fill=tk.X)

        # Botão Reset Visualização (Câmera)
        ctk.CTkButton(self.frame_controle, text="Recentralizar Câmera", command=self.reset_camera, fg_color="gray25", hover_color="gray35").pack(side=tk.BOTTOM, padx=20, pady=20, fill=tk.X)

        # Área Principal (Visualização + Status)
        self.frame_visualizacao = ctk.CTkFrame(self, corner_radius=15)
        self.frame_visualizacao.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=(0, 15), pady=15)

        self.lbl_status = ctk.CTkLabel(self.frame_visualizacao, text="Status: Clique em um nó e aperte Delete/Backspace para removê-lo.", font=ctk.CTkFont(size=13, weight="bold"), text_color="#58A6FF")
        self.lbl_status.pack(anchor="w", padx=20, pady=(15, 5))

        # Canvas
        self.canvas = tk.Canvas(self.frame_visualizacao, bg="#0D1117", highlightthickness=0)
        self.canvas.pack(expand=True, fill=tk.BOTH, padx=15, pady=10)

        # Bindings do Mouse e Teclado
        self.canvas.bind("<ButtonPress-1>", self._ao_clicar_canvas)
        self.canvas.bind("<B1-Motion>", self._executar_drag)
        self.canvas.bind("<MouseWheel>", self._executar_zoom)
        self.canvas.bind("<Button-4>", lambda e: self._executar_zoom(e, zoom_in=True))
        self.canvas.bind("<Button-5>", lambda e: self._executar_zoom(e, zoom_in=False))
        
        self.bind("<Delete>", lambda e: self.remover_no_selecionado())
        self.bind("<BackSpace>", lambda e: self.remover_no_selecionado())

        # Resultado dos percursos
        self.lbl_resultado_titulo = ctk.CTkLabel(self.frame_visualizacao, text="Resultado:", font=ctk.CTkFont(weight="bold"))
        self.lbl_resultado_titulo.pack(anchor="w", padx=20, pady=(5, 0))

        self.lbl_resultado = ctk.CTkLabel(self.frame_visualizacao, text="-", font=ctk.CTkFont(size=15), text_color="#238636")
        self.lbl_resultado.pack(anchor="w", padx=20, pady=(0, 15))

    # --- ACCORDION / ABA RETRÁTIL ---

    def toggle_aba_percursos(self):
        if self.aba_percursos_aberta:
            self.frame_botoes_percurso.pack_forget()
            self.btn_toggle_percursos.configure(text="▶  Opções de Visualização")
            self.aba_percursos_aberta = False
        else:
            self.frame_botoes_percurso.pack(fill=tk.X, pady=5)
            self.btn_toggle_percursos.configure(text="▼  Opções de Visualização")
            self.aba_percursos_aberta = True

    # --- CONTROLE DE MOUSE E SELEÇÃO DE NÓS ---

    def _ao_clicar_canvas(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

        clicou_no = self._buscar_no_por_coordenada(self.raiz, event.x, event.y)
        if clicou_no:
            self.no_selecionado = clicou_no
            self.lbl_status.configure(text=f"Status: Nó {clicou_no.valor} selecionado. Aperte Delete para remover.")
        else:
            self.no_selecionado = None
            
        self.atualizar_desenho()

    def _buscar_no_por_coordenada(self, no, px, py):
        if not no:
            return None
        
        x_trans, y_trans = self._transformar_coords(no.x, no.y)
        raio = max(10, int(20 * self.escala))
        
        dist = ((px - x_trans) ** 2 + (py - y_trans) ** 2) ** 0.5
        if dist <= raio:
            return no
            
        esq = self._buscar_no_por_coordenada(no.esquerda, px, py)
        if esq:
            return esq
            
        return self._buscar_no_por_coordenada(no.direita, px, py)

    def _executar_drag(self, event):
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        self.offset_x += dx
        self.offset_y += dy
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.atualizar_desenho()

    def _executar_zoom(self, event, zoom_in=None):
        if zoom_in is None:
            zoom_in = event.delta > 0

        fator = 1.1 if zoom_in else 0.9
        if 0.2 < (self.escala * fator) < 4.0:
            self.escala *= fator
            self.atualizar_desenho()

    def reset_camera(self):
        self.offset_x = 0
        self.offset_y = 0
        self.escala = 1.0
        self.atualizar_desenho()

    # --- ENTRADA VIA DIÁLOGO ---

    def solicitar_insercao(self):
        dialogo = ctk.CTkInputDialog(text="Digite o valor a ser inserido:", title="Inserir Nó")
        val_str = dialogo.get_input()
        if val_str is not None:
            val_str = val_str.strip()
            if val_str.lstrip('-').isdigit():
                val = int(val_str)
                self.raiz = self._inserir_rec(self.raiz, val)
                self.lbl_status.configure(text=f"Status: Nó {val} inserido com sucesso!")
                self.atualizar_desenho()
            else:
                messagebox.showerror("Erro", "Insira um número inteiro válido.")

    def solicitar_remocao(self):
        dialogo = ctk.CTkInputDialog(text="Digite o valor a ser removido:", title="Remover Nó")
        val_str = dialogo.get_input()
        if val_str is not None:
            val_str = val_str.strip()
            if val_str.lstrip('-').isdigit():
                val = int(val_str)
                self.raiz = self._remover_rec(self.raiz, val)
                self.no_selecionado = None
                self.lbl_status.configure(text=f"Status: Nó {val} removido se existia.")
                self.atualizar_desenho()
            else:
                messagebox.showerror("Erro", "Insira um número inteiro válido.")

    def remover_no_selecionado(self):
        if self.no_selecionado:
            val = self.no_selecionado.valor
            self.raiz = self._remover_rec(self.raiz, val)
            self.no_selecionado = None
            self.lbl_status.configure(text=f"Status: Nó {val} removido!")
            self.atualizar_desenho()

    # --- LÓGICA DA BST ---

    def _inserir_rec(self, no, valor, avisar_duplicado=True):
        if no is None:
            return NoArvore(valor)
        if valor < no.valor:
            no.esquerda = self._inserir_rec(no.esquerda, valor, avisar_duplicado)
        elif valor > no.valor:
            no.direita = self._inserir_rec(no.direita, valor, avisar_duplicado)
        else:
            if avisar_duplicado:
                messagebox.showwarning("Valor Duplicado", f"O valor {valor} já existe na árvore.")
        return no

    def _remover_rec(self, no, valor):
        if no is None:
            return no
        if valor < no.valor:
            no.esquerda = self._remover_rec(no.esquerda, valor)
        elif valor > no.valor:
            no.direita = self._remover_rec(no.direita, valor)
        else:
            if no.esquerda is None:
                return no.direita
            elif no.direita is None:
                return no.esquerda
            temp = self._no_min_valor(no.direita)
            no.valor = temp.valor
            no.direita = self._remover_rec(no.direita, temp.valor)
        return no

    def _no_min_valor(self, no):
        atual = no
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    def gerar_nos_em_massa(self, quantidade, modo):
        if modo == "randomico":
            valores = random.sample(range(1, 501), quantidade)
        elif modo == "crescente":
            valores = list(range(1, quantidade + 1))
        elif modo == "decrescente":
            valores = list(range(quantidade, 0, -1))

        for val in valores:
            self.raiz = self._inserir_rec(self.raiz, val, avisar_duplicado=False)

        self.lbl_status.configure(text=f"Status: {quantidade} nós inseridos no modo '{modo}'.")
        self.atualizar_desenho()

    def limpar_arvore(self):
        self.raiz = None
        self.no_selecionado = None
        self.reset_camera()
        self.lbl_status.configure(text="Status: Árvore limpa.")
        self.lbl_resultado.configure(text="-")
        self.atualizar_desenho()

    # --- LÓGICA DE BUSCA AVANÇADA ---

    def executar_busca_avancada(self, alvo, modo_tolerancia):
        if not self.raiz:
            messagebox.showwarning("Aviso", "A árvore está vazia!")
            return

        caminho_percorrido = []
        atual = self.raiz
        melhor_aprox = None

        while atual:
            caminho_percorrido.append(atual)
            
            if modo_tolerancia == "menor" and atual.valor <= alvo:
                if melhor_aprox is None or atual.valor > melhor_aprox.valor:
                    melhor_aprox = atual
            elif modo_tolerancia == "maior" and atual.valor >= alvo:
                if melhor_aprox is None or atual.valor < melhor_aprox.valor:
                    melhor_aprox = atual

            if atual.valor == alvo:
                melhor_aprox = atual
                break
            elif alvo < atual.valor:
                atual = atual.esquerda
            else:
                atual = atual.direita

        for no in caminho_percorrido:
            self.canvas.delete("all")
            self._desenhar_linhas(self.raiz)
            self._desenhar_nos(self.raiz, no_destaque=no, cor_destaque="#D29922")
            self.update()
            time.sleep(0.35)

        no_final = caminho_percorrido[-1] if caminho_percorrido else None
        
        if no_final and no_final.valor == alvo:
            self.lbl_status.configure(text=f"Status: Valor EXATO {alvo} encontrado!")
            self._desenhar_nos(self.raiz, no_destaque=no_final, cor_destaque="#2EA043")
        elif modo_tolerancia != "exato" and melhor_aprox:
            self.lbl_status.configure(text=f"Status: Exato não encontrado. Aproximação ({modo_tolerancia}): {melhor_aprox.valor}")
            self._desenhar_nos(self.raiz, no_destaque=melhor_aprox, cor_destaque="#2EA043")
        else:
            self.lbl_status.configure(text=f"Status: Valor {alvo} NÃO encontrado.")
            self._desenhar_nos(self.raiz, no_destaque=no_final, cor_destaque="#DA3633")

    # --- ALGORITMO DE POSICIONAMENTO DA ÁRVORE ---

    def _posicionar_arvore_dinamica(self, no, nivel=0, x_atual=0, espacamento_x=65, espacamento_y=75):
        if not no:
            return x_atual

        x_atual = self._posicionar_arvore_dinamica(no.esquerda, nivel + 1, x_atual, espacamento_x, espacamento_y)

        no.x = x_atual
        no.y = nivel * espacamento_y + 60
        x_atual += espacamento_x

        x_atual = self._posicionar_arvore_dinamica(no.direita, nivel + 1, x_atual, espacamento_x, espacamento_y)

        return x_atual

    def _centralizar_arvore(self, no, offset_x):
        if no:
            no.x += offset_x
            self._centralizar_arvore(no.esquerda, offset_x)
            self._centralizar_arvore(no.direita, offset_x)

    # --- RENDERIZAÇÃO E CÂMERA ---

    def atualizar_desenho(self):
        self.canvas.delete("all")

        largura_canvas = self.canvas.winfo_width()
        if largura_canvas <= 1:
            largura_canvas = 800

        if self.raiz:
            largura_total = self._posicionar_arvore_dinamica(self.raiz, nivel=0, x_atual=0)
            offset_central = (largura_canvas / 2) - (largura_total / 2)
            self._centralizar_arvore(self.raiz, offset_central)

            self._desenhar_linhas(self.raiz)
            self._desenhar_nos(self.raiz)

    def _transformar_coords(self, x, y):
        x_trans = (x * self.escala) + self.offset_x
        y_trans = (y * self.escala) + self.offset_y
        return x_trans, y_trans

    def _desenhar_linhas(self, no):
        if no is not None:
            x_pai, y_pai = self._transformar_coords(no.x, no.y)
            
            if no.esquerda:
                x_filho, y_filho = self._transformar_coords(no.esquerda.x, no.esquerda.y)
                self.canvas.create_line(x_pai, y_pai, x_filho, y_filho, fill="#484F58", width=max(1, int(2 * self.escala)))
                self._desenhar_linhas(no.esquerda)
            
            if no.direita:
                x_filho, y_filho = self._transformar_coords(no.direita.x, no.direita.y)
                self.canvas.create_line(x_pai, y_pai, x_filho, y_filho, fill="#484F58", width=max(1, int(2 * self.escala)))
                self._desenhar_linhas(no.direita)

    def _desenhar_nos(self, no, no_destaque=None, cor_destaque="#2EA043"):
        if no is not None:
            x, y = self._transformar_coords(no.x, no.y)
            raio = max(6, int(18 * self.escala))

            if no == self.no_selecionado:
                cor_fundo = "#DA3633"    # Vermelho para o selecionado
                cor_borda = "#FF7B72"
            elif no == no_destaque:
                cor_fundo = cor_destaque # Destaque de Percurso / Busca
                cor_borda = "#F2CC60"
            else:
                cor_fundo = "#1F6FE5"    # Azul Padrão
                cor_borda = "#58A6FF"

            self.canvas.create_oval(
                x - raio, y - raio, x + raio, y + raio,
                fill=cor_fundo, outline=cor_borda, width=max(1, int(2 * self.escala))
            )

            if self.escala > 0.35:
                fonte_tamanho = max(7, int(10 * self.escala))
                self.canvas.create_text(x, y, text=str(no.valor), fill="white", font=("Arial", fonte_tamanho, "bold"))

            self._desenhar_nos(no.esquerda, no_destaque, cor_destaque)
            self._desenhar_nos(no.direita, no_destaque, cor_destaque)

    # --- PERCURSOS ---

    def executar_percurso(self, tipo):
        if not self.raiz:
            messagebox.showwarning("Aviso", "A árvore está vazia!")
            return

        resultado = []
        if tipo == "pre":
            self.lbl_status.configure(text="Status: Executando Pré-Ordem...")
            self._pre_ordem(self.raiz, resultado)
        elif tipo == "em":
            self.lbl_status.configure(text="Status: Executando Em-Ordem...")
            self._em_ordem(self.raiz, resultado)
        elif tipo == "pos":
            self.lbl_status.configure(text="Status: Executando Pós-Ordem...")
            self._pos_ordem(self.raiz, resultado)
        elif tipo == "nivel":
            self.lbl_status.configure(text="Status: Executando Em Nível...")
            self._em_nivel(self.raiz, resultado)

        self._animar_percurso(resultado)

    def _pre_ordem(self, no, res):
        if no:
            res.append(no)
            self._pre_ordem(no.esquerda, res)
            self._pre_ordem(no.direita, res)

    def _em_ordem(self, no, res):
        if no:
            self._em_ordem(no.esquerda, res)
            res.append(no)
            self._em_ordem(no.direita, res)

    def _pos_ordem(self, no, res):
        if no:
            self._pos_ordem(no.esquerda, res)
            self._pos_ordem(no.direita, res)
            res.append(no)

    def _em_nivel(self, no, res):
        fila = [no]
        while fila:
            atual = fila.pop(0)
            res.append(atual)
            if atual.esquerda:
                fila.append(atual.esquerda)
            if atual.direita:
                fila.append(atual.direita)

    def _animar_percurso(self, lista_nos):
        valores_visitados = []
        for no in lista_nos:
            valores_visitados.append(str(no.valor))
            self.lbl_resultado.configure(text=" -> ".join(valores_visitados))
            
            self.canvas.delete("all")
            self._desenhar_linhas(self.raiz)
            self._desenhar_nos(self.raiz, no_destaque=no, cor_destaque="#D29922")
            
            self.update()
            time.sleep(0.35)

        self.atualizar_desenho()
        self.lbl_status.configure(text="Status: Percurso concluído!")


if __name__ == "__main__":
    app = VisualizadorBST()
    app.mainloop()