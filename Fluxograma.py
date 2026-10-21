import tkinter as tk
from tkinter import font, filedialog, messagebox, colorchooser
import json
import math
import os

try:
    from PIL import Image, ImageDraw, ImageFont
    TEM_PIL = True
except ImportError:
    TEM_PIL = False


PASTA_PROGRAMA = os.path.dirname(os.path.abspath(__file__))
PASTA_FLUXOGRAMAS = os.path.join(PASTA_PROGRAMA, "fluxogramas")

GRADE = 20
ZOOM_MIN = 0.3
ZOOM_MAX = 3.0
LIMITE_DESFAZER = 100

COR_FUNDO = "#1e1e1e"
COR_PAINEL = "#2b2b2b"
COR_BOTAO = "#3a3a3a"
COR_BOTAO_HOVER = "#505050"
COR_TEXTO = "#ffffff"
COR_TEXTO_SUAVE = "#a0a0a0"
COR_TITULO = "#ff9500"
COR_SELECAO = "#1e88e5"
COR_LIGACAO = "#ff9500"
COR_PAPEL = "#fbfbf8"
COR_GRADE = "#eeeeea"
COR_GRADE_FORTE = "#deded8"
COR_CONTORNO = "#333333"
COR_SETA = "#3c3c3c"

TIPOS = {
    "terminal": {
        "nome": "Início / Fim", "categoria": "basica", "w": 140, "h": 60, "cor": "#a8e6a3", "texto": "Início",
        "descricao": "Onde o processo começa e onde ele termina.",
        "manual": "O QUE É\nA \"pílula\" marca o começo e o fim do fluxograma.\n\n"
                  "QUANDO USAR\nTodo fluxograma tem UM Início e pelo menos UM Fim. Pode ter vários Fins "
                  "se o processo terminar de jeitos diferentes (\"Fim: venceu\", \"Fim: perdeu\").\n\n"
                  "CUIDADO\nNão escreva ações aqui dentro. \"Digite a senha\" não é Início: é uma Entrada.\n\n"
                  "EXEMPLO\nInício → ... → Fim\n\nNO PYTHON\nAbrir o programa e fechar o programa.",
    },
    "processo": {
        "nome": "Processo", "categoria": "basica", "w": 160, "h": 70, "cor": "#9cc9ff", "texto": "Processo",
        "descricao": "Uma ação, algo que é FEITO (calcular, mover, somar...).",
        "manual": "O QUE É\nO retângulo é uma AÇÃO. É a forma mais usada de todas.\n\n"
                  "QUANDO USAR\nSempre que algo é feito. Dica: o texto costuma começar com um verbo: "
                  "\"Somar os pontos\", \"Mover o personagem\", \"Ferver a água\".\n\n"
                  "CUIDADO\nPerguntas NÃO vão no retângulo. Se termina com \"?\", é um losango (Decisão).\n\n"
                  "EXEMPLO\nPassar o café\n\nNO PYTHON\nUma linha de código: pontos = pontos + 1",
    },
    "decisao": {
        "nome": "Decisão", "categoria": "basica", "w": 160, "h": 100, "cor": "#ffd27f", "texto": "Condição?",
        "descricao": "Uma PERGUNTA que divide o caminho. As respostas vão nas setas.",
        "manual": "O QUE É\nO losango é o momento em que o caminho se DIVIDE.\n\n"
                  "REGRA DE OURO\nA PERGUNTA vai dentro do losango. As RESPOSTAS (Sim / Não) são escritas "
                  "nas SETAS que saem dele, não viram formas.\n\n"
                  "Dica: o programa já escreve \"Sim\" na 1ª seta e \"Não\" na 2ª que saem de um losango.\n\n"
                  "EXEMPLO\n◇ A senha está certa?\n   Sim → Abrir o cofre\n   Não → Digitar de novo\n\n"
                  "NO PYTHON\nif senha == correta:  ...  else:  ...",
    },
    "entrada_saida": {
        "nome": "Entrada / Saída", "categoria": "basica", "w": 170, "h": 70, "cor": "#d7b5ff", "texto": "Ler dados",
        "descricao": "Algo ENTRA no programa (vem de fora) ou SAI dele (é mostrado).",
        "manual": "O QUE É\nO paralelogramo (a caixa inclinada) é a \"conversa\" com o mundo de fora.\n\n"
                  "PENSE NUMA MÁQUINA DE REFRIGERANTE\n• Você coloca a moeda → ENTRADA (algo entra)\n"
                  "• A máquina entrega a latinha → SAÍDA (algo sai)\n"
                  "• Conferir o dinheiro lá dentro → isso é Processo (retângulo)\n\n"
                  "EXEMPLO\nDigitar a senha (entrada) · Mostrar \"Senha errada\" (saída)\n\n"
                  "NO PYTHON\ninput() é entrada · print() é saída",
    },
    "conector": {
        "nome": "Conector", "categoria": "basica", "w": 50, "h": 50, "cor": "#d9d9d9", "texto": "A",
        "descricao": "Um \"portal\": a seta entra num círculo e sai no outro de mesma letra.",
        "manual": "O QUE É\nUm \"portal\" para setas. É como o \"continua na próxima página\" de um gibi.\n\n"
                  "QUANDO USAR\nQuando uma seta teria que atravessar o desenho inteiro e virar bagunça. "
                  "Você corta a linha e coloca dois círculos com a MESMA letra: a linha entra num e sai no outro.\n\n"
                  "EXEMPLO\nLavar a louça → (A)      ...      (A) → Secar a louça\n\n"
                  "NO PYTHON\nNão tem equivalente: serve só para organizar o desenho.",
    },
    "subrotina": {
        "nome": "Sub-rotina", "categoria": "especial", "w": 160, "h": 70, "cor": "#ffb3b3", "texto": "Sub-rotina",
        "descricao": "Uma tarefa que tem a PRÓPRIA receita em outro lugar.",
        "manual": "O QUE É\nO retângulo com duas linhas nas laterais é uma tarefa grande que tem o próprio "
                  "fluxograma, desenhado à parte.\n\n"
                  "PENSE NUMA RECEITA DE BOLO\n\"Fazer a cobertura (veja na página 12)\". Em vez de desenhar "
                  "todos os passos da cobertura aqui, você escreve só o nome dela.\n\n"
                  "QUANDO USAR\nPara o fluxograma principal não ficar gigante.\n\n"
                  "NO PYTHON\nChamar uma função: fazer_cobertura()",
    },
    "banco_dados": {
        "nome": "Banco de dados", "categoria": "especial", "w": 120, "h": 90, "cor": "#7fdbda", "texto": "Banco de dados",
        "descricao": "Onde as informações ficam GUARDADAS (salvar / carregar).",
        "manual": "O QUE É\nO cilindro é um lugar onde os dados ficam guardados, mesmo depois que o programa fecha.\n\n"
                  "QUANDO USAR\nQuando o processo salva ou busca informações: cadastro de usuários, "
                  "pontuação, inventário...\n\n"
                  "EXEMPLO\nSalvar a pontuação → [cilindro: Ranking]\n\n"
                  "NO PYTHON\nUm arquivo .db do SQLite ou um arquivo .json.",
    },
    "documento": {
        "nome": "Documento", "categoria": "especial", "w": 150, "h": 80, "cor": "#ffef96", "texto": "Relatório",
        "descricao": "Um papel ou arquivo que é gerado ou lido (relatório, nota, PDF...).",
        "manual": "O QUE É\nA folha com a borda de baixo ondulada é um DOCUMENTO.\n\n"
                  "QUANDO USAR\nQuando o processo cria ou usa um papel ou arquivo para pessoas lerem: relatório, "
                  "recibo, certificado, PDF, imagem exportada.\n\n"
                  "EXEMPLO\nFim do jogo → [documento: Relatório da temporada]\n\n"
                  "NO PYTHON\nGerar um .txt, um .pdf ou um .png (como o \"Exportar PNG\" deste programa).",
    },
    "entrada_manual": {
        "nome": "Entrada manual", "categoria": "especial", "w": 160, "h": 70, "cor": "#ffc48c", "texto": "Digitar o nome",
        "descricao": "Uma pessoa DIGITA algo no teclado (o topo inclinado parece um teclado).",
        "manual": "O QUE É\nO retângulo com o topo inclinado lembra um teclado visto de lado.\n\n"
                  "QUANDO USAR\nÉ uma Entrada mais específica: deixa claro que uma PESSOA digita a informação "
                  "naquele momento.\n\n"
                  "EXEMPLO\nDigitar a senha · Digitar o nome do jogador\n\n"
                  "NO PYTHON\nnome = input(\"Seu nome: \")  ou uma caixa de texto (Entry) no tkinter.",
    },
    "preparacao": {
        "nome": "Preparação", "categoria": "especial", "w": 170, "h": 70, "cor": "#f7a8d8", "texto": "Para cada aluno",
        "descricao": "Arrumar algo antes de começar, ou o início de uma REPETIÇÃO.",
        "manual": "O QUE É\nO hexágono é um passo de PREPARAÇÃO: deixar as coisas prontas antes do trabalho.\n\n"
                  "QUANDO USAR\n• Zerar valores antes de começar (\"pontos = 0\").\n"
                  "• Começar uma repetição que passa por vários itens (\"Para cada aluno da lista\").\n\n"
                  "EXEMPLO\n⬡ Para cada pergunta do quiz → Mostrar a pergunta → ... volta para o ⬡\n\n"
                  "NO PYTHON\nfor aluno in alunos:",
    },
    "exibicao": {
        "nome": "Exibição", "categoria": "especial", "w": 170, "h": 70, "cor": "#c5e1a5", "texto": "Mostrar na tela",
        "descricao": "Algo é MOSTRADO na tela para quem está usando.",
        "manual": "O QUE É\nEssa forma (ponta na esquerda, curva na direita) lembra um monitor antigo.\n\n"
                  "QUANDO USAR\nÉ uma Saída mais específica: deixa claro que a informação aparece NA TELA.\n\n"
                  "EXEMPLO\nMostrar o placar · Mostrar \"Você venceu!\"\n\n"
                  "NO PYTHON\nprint(), um Label do tkinter ou uma messagebox.",
    },
    "espera": {
        "nome": "Espera", "categoria": "especial", "w": 140, "h": 70, "cor": "#ffe0b2", "texto": "Esperar 3 segundos",
        "descricao": "Uma PAUSA: o processo espera um tempo ou um acontecimento.",
        "manual": "O QUE É\nA forma de \"D\" é um ATRASO, um momento em que nada acontece até chegar a hora.\n\n"
                  "QUANDO USAR\nQuando o processo precisa esperar: um tempo, uma resposta, um carregamento.\n\n"
                  "EXEMPLO\nPlantar a semente → [Espera: 3 dias] → Colher\n\n"
                  "NO PYTHON\ntime.sleep(3)  ou  janela.after(3000, ...) no tkinter.",
    },
    "operacao_manual": {
        "nome": "Operação manual", "categoria": "especial", "w": 160, "h": 70, "cor": "#d7ccc8", "texto": "Conferir à mão",
        "descricao": "Uma tarefa feita por uma PESSOA, sem o computador.",
        "manual": "O QUE É\nO trapézio é um trabalho feito À MÃO, por uma pessoa.\n\n"
                  "QUANDO USAR\nEm processos que misturam pessoas e programa: alguém confere, assina, embala...\n\n"
                  "EXEMPLO\nO sistema imprime o pedido → [trapézio: Embalar o produto] → O sistema avisa o cliente\n\n"
                  "NO PYTHON\nNão tem: é justamente o que o programa NÃO faz.",
    },
    "conector_pagina": {
        "nome": "Conector de página", "categoria": "especial", "w": 60, "h": 60, "cor": "#d9d9d9", "texto": "1",
        "descricao": "O fluxograma continua em OUTRA página ou outro arquivo.",
        "manual": "O QUE É\nA \"casinha de cabeça para baixo\" é um portal para OUTRA página.\n\n"
                  "DIFERENÇA DO CONECTOR\n• Conector (círculo): o portal fica na MESMA folha.\n"
                  "• Conector de página: o desenho continua em OUTRA folha ou outro arquivo.\n\n"
                  "EXEMPLO\n... → [pág. 2]   e, na página 2:   [pág. 2] → ...\n\n"
                  "NO PYTHON\nNão tem equivalente: serve só para organizar o desenho.",
    },
}

MANUAL_GERAL = {
    "Primeiros passos":
        "BEM-VINDO AO FLUXOGRAMA!\n\nUm fluxograma é um desenho que mostra os PASSOS de um processo, na ordem em que "
        "acontecem. Serve para planejar um programa, uma receita, um jogo, qualquer coisa que tenha etapas.\n\n"
        "COMO MONTAR O PRIMEIRO\n1. No painel da esquerda, clique numa forma (ex.: Início / Fim).\n"
        "2. Clique na folha para colocá-la.\n3. Dê um duplo clique na forma para escrever o texto.\n"
        "4. Escolha \"Ligar com seta\" (tecla L), clique na forma de origem e depois na de destino.\n"
        "5. Salve com Ctrl+S.\n\n"
        "Quer ver um pronto? Ajuda › Carregar exemplo.",
    "Regra de ouro":
        "AS 3 REGRAS QUE MAIS IMPORTAM\n\n"
        "1. PERGUNTA NO LOSANGO, RESPOSTA NA SETA\nA pergunta (\"A senha está certa?\") vai dentro do losango. "
        "\"Sim\" e \"Não\" são escritos nas setas, não viram formas.\n\n"
        "2. A PÍLULA É SÓ PARA INÍCIO E FIM\nAções e perguntas nunca vão nela.\n\n"
        "3. AS SETAS MOSTRAM A ORDEM\nSiga as setas com o dedo: se der para \"ler\" o processo do Início ao Fim "
        "sem se perder, o fluxograma está bom.\n\n"
        "LAÇOS (REPETIÇÕES)\nUma seta pode VOLTAR para um passo anterior. Ex.: senha errada → digitar de novo → "
        "conferir de novo. Isso é o \"while\" do Python.",
    "Formas básicas x especiais":
        "POR QUE DOIS GRUPOS?\n\n"
        "FORMAS BÁSICAS (5)\nCom elas você desenha quase qualquer fluxograma: Início/Fim, Processo, Decisão, "
        "Entrada/Saída e Conector. Comece sempre por elas.\n\n"
        "FORMAS ESPECIAIS (9)\nTêm funções específicas. Elas não são obrigatórias, mas deixam o desenho mais "
        "preciso. Ex.: em vez de uma Entrada/Saída genérica, a \"Entrada manual\" diz que uma PESSOA digita; "
        "a \"Exibição\" diz que algo aparece NA TELA.\n\n"
        "DICA\nNa dúvida, use a forma básica. Passe o mouse sobre uma forma no painel para ver para que ela serve, "
        "ou clique com o botão direito numa forma da folha › \"Ver no manual\".",
    "Setas e rótulos":
        "SETAS\n• Ferramenta \"Ligar com seta\" (L): clique na origem e depois no destino.\n"
        "• Duplo clique numa seta: escreve um rótulo nela (ex.: Sim / Não).\n"
        "• Botão direito numa seta: inverter a direção ou apagar.\n\n"
        "ÂNGULO RETO\nEm Exibir, \"Setas em ângulo reto\" faz as setas andarem só na horizontal e na vertical, "
        "como num organograma.\n\nDICA\nSe muitas setas se cruzarem, use um Conector (o portal) para limpar o desenho.",
    "Organizar a folha":
        "• Grade: as linhas de fundo que ajudam a alinhar.\n"
        "• Encaixar na grade: as formas \"grudam\" na grade ao mover.\n"
        "• Quadradinho azul: aparece no canto da forma selecionada; arraste para mudar o tamanho.\n"
        "• Caixa de seleção: arraste no vazio para selecionar várias formas.\n"
        "• Para frente / Para trás: decide qual forma fica por cima.\n"
        "• Zoom: Ctrl + rodinha, ou os botões − 100% + do painel. \"Ajustar\" enquadra tudo na tela.\n"
        "• Botão do meio do mouse: arrasta a folha.\n\n"
        "PAINEL\nClique no título de uma seção (ex.: ▾ EDITAR) para recolher ou expandir. "
        "Use a rodinha sobre o painel para rolar.",
    "Arquivos":
        "• Salvar (Ctrl+S): guarda o fluxograma num arquivo .json, para continuar depois.\n"
        "• Abrir (Ctrl+O): carrega um fluxograma salvo.\n"
        "• Exportar PNG (Ctrl+E): cria uma imagem do fluxograma, para mostrar a outras pessoas.\n\n"
        "Por padrão tudo vai para a pasta \"fluxogramas\", ao lado do programa.\n\n"
        "Se fechar com alterações não salvas, o programa pergunta se você quer salvar.",
}

PALETA = [
    "#a8e6a3", "#9cc9ff", "#ffd27f", "#d7b5ff", "#ffb3b3", "#d9d9d9",
    "#7fdbda", "#ffef96", "#ffc48c", "#f7a8d8", "#ffffff", "#b0bec5",
]

ATALHOS = """FERRAMENTAS
  V  ............  Selecionar / mover
  L  ............  Ligar formas (seta)
  1 a 5  .......  Escolher uma forma básica
  Esc  .........  Cancelar / limpar seleção
  F1 / F2  .....  Atalhos / Manual de instruções

MOUSE
  Clique  ........  Seleciona
  Shift + clique  Adiciona à seleção
  Arrastar  ......  Move (ou caixa de seleção no vazio)
  Duplo clique  ..  Edita o texto (no vazio cria um Processo)
  Botão direito  .  Menu da forma / seta
  Rodinha  .......  Rola (Shift = para os lados)
  Ctrl + rodinha  Zoom
  Botão do meio  .  Arrasta a folha

EDIÇÃO
  Ctrl+Z / Ctrl+Y  Desfazer / Refazer
  Ctrl+C / Ctrl+V  Copiar / Colar
  Ctrl+D  ........  Duplicar
  Ctrl+A  ........  Selecionar tudo
  Delete  ........  Apagar
  Setas  .........  Move a seleção (Shift = 1 px)

ARQUIVO
  Ctrl+N  Novo      Ctrl+O  Abrir
  Ctrl+S  Salvar    Ctrl+Shift+S  Salvar como
  Ctrl+E  Exportar PNG

No editor de texto: Enter confirma, Shift+Enter quebra a linha."""


class Fluxograma:
    def __init__(self, janela):
        self.janela = janela
        self.janela.geometry("1280x800")
        self.janela.minsize(960, 720)
        self.janela.configure(bg=COR_FUNDO)

        self.formas = {}
        self.setas = {}
        self.proximo_id = 1
        self.sel_formas = set()
        self.sel_setas = set()
        self.ferramenta = "selecionar"
        self.origem_ligacao = None
        self.zoom = 1.0
        self.arquivo_atual = None
        self.modificado = False
        self.pilha_desfazer = []
        self.pilha_refazer = []
        self.area_transferencia = None
        self.colagens = 0
        self.arraste = None
        self.editor = None
        self.fontes = {}
        self.aviso_id = None
        self.janela_manual = None
        self.topico_manual = None

        self.var_grade = tk.BooleanVar(value=True)
        self.var_encaixe = tk.BooleanVar(value=True)
        self.var_cotovelo = tk.BooleanVar(value=False)

        self.fonte_titulo = font.Font(family="Segoe UI", size=9, weight="bold")
        self.fonte_botao = font.Font(family="Segoe UI", size=10)
        self.fonte_status = font.Font(family="consolas", size=10)

        self.criar_menu()
        self.criar_barra_status()
        self.criar_painel()
        self.criar_canvas()
        self.configurar_atalhos()
        self.escolher_ferramenta("selecionar")

        self.janela.protocol("WM_DELETE_WINDOW", self.sair)
        self.atualizar_titulo()
        self.janela.after(50, self.redesenhar_tudo)

    # ------------------------------------------------------------ interface

    def criar_menu(self):
        barra = tk.Menu(self.janela)

        arquivo = tk.Menu(barra, tearoff=0)
        arquivo.add_command(label="Novo", accelerator="Ctrl+N", command=self.novo)
        arquivo.add_command(label="Abrir...", accelerator="Ctrl+O", command=self.abrir)
        arquivo.add_command(label="Salvar", accelerator="Ctrl+S", command=self.salvar)
        arquivo.add_command(label="Salvar como...", accelerator="Ctrl+Shift+S", command=self.salvar_como)
        arquivo.add_separator()
        arquivo.add_command(label="Exportar PNG...", accelerator="Ctrl+E", command=self.exportar_png)
        arquivo.add_separator()
        arquivo.add_command(label="Sair", command=self.sair)
        barra.add_cascade(label="Arquivo", menu=arquivo)

        editar = tk.Menu(barra, tearoff=0)
        editar.add_command(label="Desfazer", accelerator="Ctrl+Z", command=self.desfazer)
        editar.add_command(label="Refazer", accelerator="Ctrl+Y", command=self.refazer)
        editar.add_separator()
        editar.add_command(label="Copiar", accelerator="Ctrl+C", command=self.copiar)
        editar.add_command(label="Colar", accelerator="Ctrl+V", command=self.colar)
        editar.add_command(label="Duplicar", accelerator="Ctrl+D", command=self.duplicar)
        editar.add_command(label="Apagar", accelerator="Delete", command=self.apagar_selecao)
        editar.add_command(label="Selecionar tudo", accelerator="Ctrl+A", command=self.selecionar_tudo)
        editar.add_separator()
        editar.add_command(label="Trazer para frente", command=self.trazer_frente)
        editar.add_command(label="Enviar para trás", command=self.enviar_tras)
        barra.add_cascade(label="Editar", menu=editar)

        exibir = tk.Menu(barra, tearoff=0)
        exibir.add_checkbutton(label="Grade", variable=self.var_grade, command=self.redesenhar_tudo)
        exibir.add_checkbutton(label="Encaixar na grade", variable=self.var_encaixe)
        exibir.add_checkbutton(label="Setas em ângulo reto", variable=self.var_cotovelo, command=self.alternar_cotovelo)
        exibir.add_separator()
        exibir.add_command(label="Aumentar zoom", accelerator="Ctrl++", command=lambda: self.mudar_zoom(1.25))
        exibir.add_command(label="Diminuir zoom", accelerator="Ctrl+-", command=lambda: self.mudar_zoom(0.8))
        exibir.add_command(label="Zoom 100%", accelerator="Ctrl+0", command=lambda: self.definir_zoom(1.0))
        exibir.add_command(label="Ajustar à tela", command=self.ajustar_tela)
        barra.add_cascade(label="Exibir", menu=exibir)

        ajuda = tk.Menu(barra, tearoff=0)
        ajuda.add_command(label="Manual de instruções", accelerator="F2", command=self.abrir_manual)
        ajuda.add_command(label="Atalhos", accelerator="F1", command=self.mostrar_atalhos)
        ajuda.add_command(label="Carregar exemplo", command=self.carregar_exemplo)
        ajuda.add_separator()
        ajuda.add_command(label="Sobre", command=self.mostrar_sobre)
        barra.add_cascade(label="Ajuda", menu=ajuda)

        self.janela.config(menu=barra)

    def criar_barra_status(self):
        barra = tk.Frame(self.janela, bg=COR_PAINEL, height=26)
        barra.pack(side="bottom", fill="x")

        self.lbl_dica = tk.Label(barra, text="", bg=COR_PAINEL, fg=COR_TEXTO_SUAVE,
                                 font=self.fonte_status, anchor="w")
        self.lbl_dica.pack(side="left", fill="x", expand=True, padx=8)

        self.lbl_coord = tk.Label(barra, text="", bg=COR_PAINEL, fg=COR_TEXTO_SUAVE,
                                  font=self.fonte_status, width=12)
        self.lbl_coord.pack(side="right", padx=4)
        self.lbl_zoom = tk.Label(barra, text="", bg=COR_PAINEL, fg=COR_TEXTO,
                                 font=self.fonte_status, width=11)
        self.lbl_zoom.pack(side="right", padx=4)
        self.lbl_contagem = tk.Label(barra, text="", bg=COR_PAINEL, fg=COR_TEXTO,
                                     font=self.fonte_status)
        self.lbl_contagem.pack(side="right", padx=8)

    def botao(self, pai, texto, comando):
        return tk.Button(pai, text=texto, command=comando, bg=COR_BOTAO, fg=COR_TEXTO,
                         font=self.fonte_botao, bd=0, activebackground=COR_BOTAO_HOVER,
                         activeforeground=COR_TEXTO, cursor="hand2")

    def criar_secao(self, titulo, aberta=True):
        cabecalho = tk.Label(self.painel, bg=COR_PAINEL, fg=COR_TITULO, font=self.fonte_titulo,
                             anchor="w", cursor="hand2")
        cabecalho.pack(fill="x", padx=8, pady=(8, 2))
        conteudo = tk.Frame(self.painel, bg=COR_PAINEL)
        secao = {"titulo": titulo, "cabecalho": cabecalho, "conteudo": conteudo, "aberta": aberta}
        cabecalho.bind("<Button-1>", lambda e: self.alternar_secao(secao))
        cabecalho.bind("<Enter>", lambda e: cabecalho.config(fg="#ffb84d"))
        cabecalho.bind("<Leave>", lambda e: cabecalho.config(fg=COR_TITULO))
        self.secoes.append(secao)
        self.mostrar_secao(secao)
        return conteudo

    def mostrar_secao(self, secao):
        seta = "▾" if secao["aberta"] else "▸"
        secao["cabecalho"].config(text=f"{seta}  {secao['titulo']}")
        if secao["aberta"]:
            secao["conteudo"].pack(fill="x", after=secao["cabecalho"])
        else:
            secao["conteudo"].pack_forget()

    def alternar_secao(self, secao):
        secao["aberta"] = not secao["aberta"]
        self.mostrar_secao(secao)

    def abrir_todas_secoes(self, aberta):
        for secao in self.secoes:
            secao["aberta"] = aberta
            self.mostrar_secao(secao)
        self.tela_painel.yview_moveto(0)

    def rolar_painel(self, e):
        if not str(e.widget).startswith(str(self.painel_externo)):
            return
        if self.painel.winfo_height() > self.tela_painel.winfo_height():
            self.tela_painel.yview_scroll(-1 if e.delta > 0 else 1, "units")

    def criar_painel(self):
        self.painel_externo = tk.Frame(self.janela, bg=COR_PAINEL, width=228)
        self.painel_externo.pack(side="left", fill="y")
        self.painel_externo.pack_propagate(False)

        self.tela_painel = tk.Canvas(self.painel_externo, bg=COR_PAINEL, highlightthickness=0,
                                     width=210, yscrollincrement=24)
        rolagem = tk.Scrollbar(self.painel_externo, orient="vertical", command=self.tela_painel.yview)
        self.tela_painel.configure(yscrollcommand=rolagem.set)
        rolagem.pack(side="right", fill="y")
        self.tela_painel.pack(side="left", fill="both", expand=True)

        self.painel = tk.Frame(self.tela_painel, bg=COR_PAINEL)
        self.tela_painel.create_window(0, 0, window=self.painel, anchor="nw", width=210)
        self.painel.bind("<Configure>", lambda e: self.tela_painel.configure(
            scrollregion=(0, 0, 210, self.painel.winfo_reqheight())))
        self.janela.bind_all("<MouseWheel>", self.rolar_painel, add="+")

        self.botoes_ferramenta = {}
        self.secoes = []

        topo = tk.Frame(self.painel, bg=COR_PAINEL)
        topo.pack(fill="x", padx=10, pady=(10, 0))
        self.botao(topo, "📖  Manual de instruções", self.abrir_manual).pack(fill="x")
        quadro_secoes = tk.Frame(topo, bg=COR_PAINEL)
        quadro_secoes.pack(fill="x", pady=(4, 0))
        self.botao(quadro_secoes, "▾ Expandir", lambda: self.abrir_todas_secoes(True)).pack(
            side="left", fill="x", expand=True, padx=(0, 2))
        self.botao(quadro_secoes, "▸ Recolher", lambda: self.abrir_todas_secoes(False)).pack(
            side="left", fill="x", expand=True, padx=(2, 0))

        secao = self.criar_secao("FERRAMENTAS")
        self.criar_opcao_ferramenta(secao, "selecionar", "Selecionar", "V",
                                    "Clique para selecionar, arraste para mover.")
        self.criar_opcao_ferramenta(secao, "ligar", "Ligar com seta", "L",
                                    "Clique na forma de origem e depois na de destino.")

        secao = self.criar_secao("FORMAS BÁSICAS")
        basicas = [t for t in TIPOS if TIPOS[t]["categoria"] == "basica"]
        for numero, tipo in enumerate(basicas, start=1):
            self.criar_opcao_ferramenta(secao, tipo, TIPOS[tipo]["nome"], str(numero), TIPOS[tipo]["descricao"])

        secao = self.criar_secao("FORMAS ESPECIAIS")
        for tipo in TIPOS:
            if TIPOS[tipo]["categoria"] == "especial":
                self.criar_opcao_ferramenta(secao, tipo, TIPOS[tipo]["nome"], "", TIPOS[tipo]["descricao"])

        secao = self.criar_secao("COR DA FORMA")
        quadro_cores = tk.Frame(secao, bg=COR_PAINEL)
        quadro_cores.pack(fill="x", padx=10)
        for i, cor in enumerate(PALETA):
            amostra = tk.Frame(quadro_cores, bg=cor, width=26, height=22, cursor="hand2",
                               highlightthickness=1, highlightbackground="#555555")
            amostra.grid(row=i // 6, column=i % 6, padx=2, pady=2)
            amostra.bind("<Button-1>", lambda e, c=cor: self.aplicar_cor(c))
        self.botao(secao, "Outra cor...", self.escolher_outra_cor).pack(fill="x", padx=10, pady=(4, 0))

        secao = self.criar_secao("EDITAR")
        quadro_editar = tk.Frame(secao, bg=COR_PAINEL)
        quadro_editar.pack(fill="x", padx=10)
        botoes = [
            ("↶ Desfazer", self.desfazer), ("↷ Refazer", self.refazer),
            ("Duplicar", self.duplicar), ("Apagar", self.apagar_selecao),
            ("Para frente", self.trazer_frente), ("Para trás", self.enviar_tras),
        ]
        for i, (texto, comando) in enumerate(botoes):
            self.botao(quadro_editar, texto, comando).grid(row=i // 2, column=i % 2, sticky="ew", padx=2, pady=2)
        quadro_editar.columnconfigure(0, weight=1)
        quadro_editar.columnconfigure(1, weight=1)

        secao = self.criar_secao("EXIBIR")
        for texto, variavel, comando in (
            ("Grade", self.var_grade, self.redesenhar_tudo),
            ("Encaixar na grade", self.var_encaixe, None),
            ("Setas em ângulo reto", self.var_cotovelo, self.alternar_cotovelo),
        ):
            tk.Checkbutton(secao, text=texto, variable=variavel, command=comando,
                           bg=COR_PAINEL, fg=COR_TEXTO, selectcolor=COR_BOTAO,
                           activebackground=COR_PAINEL, activeforeground=COR_TEXTO,
                           font=self.fonte_botao, anchor="w", bd=0).pack(fill="x", padx=8)
        quadro_zoom = tk.Frame(secao, bg=COR_PAINEL)
        quadro_zoom.pack(fill="x", padx=10, pady=(4, 0))
        for i, (texto, comando) in enumerate((
            ("−", lambda: self.mudar_zoom(0.8)),
            ("100%", lambda: self.definir_zoom(1.0)),
            ("+", lambda: self.mudar_zoom(1.25)),
            ("Ajustar", self.ajustar_tela),
        )):
            self.botao(quadro_zoom, texto, comando).grid(row=0, column=i, sticky="ew", padx=1)
            quadro_zoom.columnconfigure(i, weight=1)

        secao = self.criar_secao("SELEÇÃO")
        self.lbl_selecao = tk.Label(secao, text="", bg=COR_PAINEL, fg=COR_TEXTO_SUAVE,
                                    font=self.fonte_botao, anchor="nw", justify="left", wraplength=186)
        self.lbl_selecao.pack(fill="x", padx=10, pady=(0, 12))

    def criar_opcao_ferramenta(self, pai, nome, texto, tecla, descricao):
        opcao = tk.Canvas(pai, width=186, height=30, bg=COR_BOTAO, highlightthickness=0, cursor="hand2")
        opcao.pack(padx=10, pady=2)
        self.desenhar_icone(opcao, nome)
        opcao.create_text(52, 15, text=texto, anchor="w", fill=COR_TEXTO, font=self.fonte_botao)
        opcao.create_text(176, 15, text=tecla, anchor="e", fill=COR_TEXTO_SUAVE, font=self.fonte_status)
        opcao.bind("<Button-1>", lambda e: self.escolher_ferramenta(nome))
        opcao.bind("<Enter>", lambda e: self.lbl_dica.config(text=f"{texto}: {descricao}", fg=COR_TEXTO))
        opcao.bind("<Leave>", lambda e: self.mostrar_dica())
        self.botoes_ferramenta[nome] = opcao

    def desenhar_icone(self, tela, nome, centro=(22, 15), caixa=(34, 22), espessura=1):
        if nome == "selecionar":
            tela.create_polygon(18, 6, 18, 24, 22, 20, 26, 27, 29, 25, 25, 18, 31, 18,
                                fill=COR_TEXTO, outline="")
        elif nome == "ligar":
            tela.create_line(10, 22, 34, 8, fill=COR_TEXTO, width=2, arrow=tk.LAST, arrowshape=(8, 9, 3))
        else:
            dados = TIPOS[nome]
            proporcao = min(caixa[0] / dados["w"], caixa[1] / dados["h"])
            mini = {"tipo": nome, "x": centro[0], "y": centro[1],
                    "w": dados["w"] * proporcao, "h": dados["h"] * proporcao}
            pontos = [c for p in self.pontos_forma(mini) for c in p]
            tela.create_polygon(pontos, fill=dados["cor"], outline=COR_CONTORNO, width=espessura)
            for linha in self.detalhes_forma(mini):
                tela.create_line([c for p in linha for c in p], fill=COR_CONTORNO, width=espessura)

    def criar_canvas(self):
        area = tk.Frame(self.janela, bg=COR_FUNDO)
        area.pack(side="left", fill="both", expand=True)

        self.canvas = tk.Canvas(area, bg=COR_PAPEL, highlightthickness=0)
        rolagem_y = tk.Scrollbar(area, orient="vertical", command=self.canvas.yview)
        rolagem_x = tk.Scrollbar(area, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=rolagem_y.set, xscrollcommand=rolagem_x.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        rolagem_y.grid(row=0, column=1, sticky="ns")
        rolagem_x.grid(row=1, column=0, sticky="ew")
        area.rowconfigure(0, weight=1)
        area.columnconfigure(0, weight=1)

        self.canvas.bind("<Button-1>", self.ao_clicar)
        self.canvas.bind("<B1-Motion>", self.ao_arrastar)
        self.canvas.bind("<ButtonRelease-1>", self.ao_soltar)
        self.canvas.bind("<Double-Button-1>", self.ao_duplo_clique)
        self.canvas.bind("<Button-3>", self.ao_botao_direito)
        self.canvas.bind("<Button-2>", lambda e: self.canvas.scan_mark(e.x, e.y))
        self.canvas.bind("<B2-Motion>", lambda e: self.canvas.scan_dragto(e.x, e.y, gain=1))
        self.canvas.bind("<Motion>", self.ao_mover_mouse)
        self.canvas.bind("<MouseWheel>", self.ao_rodinha)
        self.canvas.bind("<Configure>", lambda e: self.redesenhar())

    def configurar_atalhos(self):
        atalhos = {
            "<Delete>": self.apagar_selecao,
            "<Control-z>": self.desfazer,
            "<Control-y>": self.refazer,
            "<Control-c>": self.copiar,
            "<Control-v>": self.colar,
            "<Control-d>": self.duplicar,
            "<Control-a>": self.selecionar_tudo,
            "<Control-n>": self.novo,
            "<Control-o>": self.abrir,
            "<Control-s>": self.salvar,
            "<Control-S>": self.salvar_como,
            "<Control-e>": self.exportar_png,
            "<Control-plus>": lambda: self.mudar_zoom(1.25),
            "<Control-equal>": lambda: self.mudar_zoom(1.25),
            "<Control-minus>": lambda: self.mudar_zoom(0.8),
            "<Control-0>": lambda: self.definir_zoom(1.0),
            "<Escape>": self.cancelar,
            "<F1>": self.mostrar_atalhos,
            "<v>": lambda: self.escolher_ferramenta("selecionar"),
            "<l>": lambda: self.escolher_ferramenta("ligar"),
            "<Left>": lambda: self.mover_selecao(-1, 0, False),
            "<Right>": lambda: self.mover_selecao(1, 0, False),
            "<Up>": lambda: self.mover_selecao(0, -1, False),
            "<Down>": lambda: self.mover_selecao(0, 1, False),
            "<Shift-Left>": lambda: self.mover_selecao(-1, 0, True),
            "<Shift-Right>": lambda: self.mover_selecao(1, 0, True),
            "<Shift-Up>": lambda: self.mover_selecao(0, -1, True),
            "<Shift-Down>": lambda: self.mover_selecao(0, 1, True),
        }
        atalhos["<F2>"] = self.abrir_manual
        basicas = [t for t in TIPOS if TIPOS[t]["categoria"] == "basica"]
        for numero, tipo in enumerate(basicas, start=1):
            atalhos[f"<Key-{numero}>"] = lambda t=tipo: self.escolher_ferramenta(t)

        for evento, funcao in atalhos.items():
            self.janela.bind(evento, self.atalho(funcao))

    def atalho(self, funcao):
        def tratar(evento):
            if self.editor or isinstance(evento.widget, (tk.Entry, tk.Text)):
                return None
            funcao()
            return "break"
        return tratar

    # ------------------------------------------------------------ geometria

    def arco(self, cx, cy, rx, ry, inicio, fim, passos=12):
        return [(cx + rx * math.cos(inicio + (fim - inicio) * i / passos),
                 cy + ry * math.sin(inicio + (fim - inicio) * i / passos)) for i in range(passos + 1)]

    def medidas(self, f):
        w, h = f["w"], f["h"]
        return {
            "inclinacao": min(h * 0.4, w * 0.25),
            "tampa": min(h * 0.15, 14),
            "onda": h * 0.1,
            "ponta": min(w * 0.2, h * 0.5),
            "curva": min(w * 0.18, h / 2),
            "recuo": min(12, w * 0.1),
        }

    def pontos_forma(self, f):
        x, y, w, h = f["x"], f["y"], f["w"], f["h"]
        esq, dir, topo, base = x - w / 2, x + w / 2, y - h / 2, y + h / 2
        m = self.medidas(f)
        tipo = f["tipo"]
        pi = math.pi

        if tipo == "decisao":
            return [(x, topo), (dir, y), (x, base), (esq, y)]
        if tipo == "entrada_saida":
            d = m["inclinacao"]
            return [(esq + d, topo), (dir, topo), (dir - d, base), (esq, base)]
        if tipo == "terminal":
            raio = min(w, h) / 2
            return (self.arco(dir - raio, y, raio, raio, -pi / 2, pi / 2)
                    + self.arco(esq + raio, y, raio, raio, pi / 2, 3 * pi / 2))
        if tipo == "conector":
            return self.arco(x, y, w / 2, h / 2, 0, 2 * pi, 36)[:-1]
        if tipo == "banco_dados":
            t = m["tampa"]
            return (self.arco(x, topo + t, w / 2, t, pi, 2 * pi)
                    + self.arco(x, base - t, w / 2, t, 0, pi))
        if tipo == "documento":
            onda = m["onda"]
            pontos = [(esq, topo), (dir, topo)]
            for i in range(21):
                t = i / 20
                pontos.append((dir - w * t, base - onda + onda * math.sin(2 * pi * t)))
            return pontos
        if tipo == "entrada_manual":
            return [(esq, topo + h * 0.3), (dir, topo), (dir, base), (esq, base)]
        if tipo == "preparacao":
            d = m["ponta"]
            return [(esq + d, topo), (dir - d, topo), (dir, y), (dir - d, base), (esq + d, base), (esq, y)]
        if tipo == "exibicao":
            d, r = m["ponta"] * 0.8, m["curva"]
            return ([(esq, y), (esq + d, topo)] + self.arco(dir - r, y, r, h / 2, -pi / 2, pi / 2)
                    + [(esq + d, base)])
        if tipo == "espera":
            r = m["curva"] * 1.6 if w > h else w / 2
            r = min(r, w / 2)
            return [(esq, topo)] + self.arco(dir - r, y, r, h / 2, -pi / 2, pi / 2) + [(esq, base)]
        if tipo == "operacao_manual":
            d = min(w * 0.15, h * 0.5)
            return [(esq, topo), (dir, topo), (dir - d, base), (esq + d, base)]
        if tipo == "conector_pagina":
            return [(esq, topo), (dir, topo), (dir, y + h * 0.1), (x, base), (esq, y + h * 0.1)]
        return [(esq, topo), (dir, topo), (dir, base), (esq, base)]

    def detalhes_forma(self, f):
        x, y, w, h = f["x"], f["y"], f["w"], f["h"]
        topo, base = y - h / 2, y + h / 2
        m = self.medidas(f)
        if f["tipo"] == "subrotina":
            r = m["recuo"]
            return [[(x - w / 2 + r, topo), (x - w / 2 + r, base)],
                    [(x + w / 2 - r, topo), (x + w / 2 - r, base)]]
        if f["tipo"] == "banco_dados":
            return [self.arco(x, topo + m["tampa"], w / 2, m["tampa"], 0, math.pi)]
        return []

    def centro_texto(self, f):
        m = self.medidas(f)
        if f["tipo"] == "banco_dados":
            return f["x"], f["y"] + m["tampa"] / 2
        if f["tipo"] == "documento":
            return f["x"], f["y"] - m["onda"] / 2
        if f["tipo"] == "entrada_manual":
            return f["x"], f["y"] + f["h"] * 0.1
        if f["tipo"] == "conector_pagina":
            return f["x"], f["y"] - f["h"] * 0.1
        if f["tipo"] == "exibicao":
            return f["x"] + m["ponta"] * 0.2, f["y"]
        return f["x"], f["y"]

    def largura_texto(self, f):
        m = self.medidas(f)
        tipo = f["tipo"]
        if tipo == "decisao":
            return f["w"] * 0.58
        if tipo == "entrada_saida":
            return f["w"] - 2 * m["inclinacao"] - 6
        if tipo == "subrotina":
            return f["w"] - 2 * m["recuo"] - 8
        if tipo in ("preparacao", "exibicao"):
            return f["w"] - 2 * m["ponta"]
        if tipo in ("operacao_manual", "conector_pagina"):
            return f["w"] * 0.7
        return f["w"] - 16

    def ponto_borda(self, f, alvo_x, alvo_y):
        cx, cy = f["x"], f["y"]
        dx, dy = alvo_x - cx, alvo_y - cy
        if dx == 0 and dy == 0:
            return cx, cy
        pontos = self.pontos_forma(f)
        melhor = None
        for i in range(len(pontos)):
            x1, y1 = pontos[i]
            x2, y2 = pontos[(i + 1) % len(pontos)]
            ex, ey = x2 - x1, y2 - y1
            denominador = dx * ey - dy * ex
            if abs(denominador) < 1e-9:
                continue
            t = ((x1 - cx) * ey - (y1 - cy) * ex) / denominador
            u = ((x1 - cx) * dy - (y1 - cy) * dx) / denominador
            if t > 0 and -1e-9 <= u <= 1 + 1e-9 and (melhor is None or t < melhor):
                melhor = t
        if melhor is None:
            return cx, cy
        return cx + dx * melhor, cy + dy * melhor

    def pontos_seta(self, s):
        a = self.formas[s["origem"]]
        b = self.formas[s["destino"]]
        if not self.var_cotovelo.get():
            return [self.ponto_borda(a, b["x"], b["y"]), self.ponto_borda(b, a["x"], a["y"])]

        dx, dy = b["x"] - a["x"], b["y"] - a["y"]
        if abs(dx) >= abs(dy):
            sentido = 1 if dx >= 0 else -1
            p1 = self.ponto_borda(a, a["x"] + sentido * 10000, a["y"])
            p2 = self.ponto_borda(b, b["x"] - sentido * 10000, b["y"])
            meio = (p1[0] + p2[0]) / 2
            return [p1, (meio, p1[1]), (meio, p2[1]), p2]
        sentido = 1 if dy >= 0 else -1
        p1 = self.ponto_borda(a, a["x"], a["y"] + sentido * 10000)
        p2 = self.ponto_borda(b, b["x"], b["y"] - sentido * 10000)
        meio = (p1[1] + p2[1]) / 2
        return [p1, (p1[0], meio), (p2[0], meio), p2]

    def meio_da_linha(self, pontos):
        trechos = [math.dist(pontos[i], pontos[i + 1]) for i in range(len(pontos) - 1)]
        metade = sum(trechos) / 2
        for i, tamanho in enumerate(trechos):
            if metade <= tamanho and tamanho > 0:
                t = metade / tamanho
                (x1, y1), (x2, y2) = pontos[i], pontos[i + 1]
                return x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
            metade -= tamanho
        return pontos[-1]

    def limites_conteudo(self):
        if not self.formas:
            return None
        xs, ys = [], []
        for f in self.formas.values():
            xs += [f["x"] - f["w"] / 2, f["x"] + f["w"] / 2]
            ys += [f["y"] - f["h"] / 2, f["y"] + f["h"] / 2]
        for s in self.setas.values():
            for px, py in self.pontos_seta(s):
                xs.append(px)
                ys.append(py)
        return min(xs), min(ys), max(xs), max(ys)

    def tamanho_mundo(self):
        limites = self.limites_conteudo()
        if not limites:
            return 4000, 3000
        return max(4000, limites[2] + 800), max(3000, limites[3] + 800)

    def encaixar(self, valor):
        if self.var_encaixe.get():
            return round(valor / GRADE) * GRADE
        return valor

    # ------------------------------------------------------------ desenho

    def fonte(self, tamanho):
        tamanho = max(1, round(tamanho))
        if tamanho not in self.fontes:
            self.fontes[tamanho] = font.Font(family="Segoe UI", size=tamanho)
        return self.fontes[tamanho]

    def redesenhar_tudo(self):
        self.desenhar_grade()
        self.redesenhar()

    def desenhar_grade(self):
        c = self.canvas
        c.delete("grade")
        largura, altura = self.tamanho_mundo()
        z = self.zoom
        c.configure(scrollregion=(0, 0, largura * z, altura * z))
        if not self.var_grade.get():
            return
        passo = GRADE if z >= 0.6 else GRADE * 5
        for i, x in enumerate(range(0, int(largura) + 1, passo)):
            forte = passo > GRADE or i % 5 == 0
            c.create_line(x * z, 0, x * z, altura * z, fill=COR_GRADE_FORTE if forte else COR_GRADE, tags="grade")
        for i, y in enumerate(range(0, int(altura) + 1, passo)):
            forte = passo > GRADE or i % 5 == 0
            c.create_line(0, y * z, largura * z, y * z, fill=COR_GRADE_FORTE if forte else COR_GRADE, tags="grade")
        c.tag_lower("grade")

    def redesenhar(self):
        c = self.canvas
        c.delete("conteudo")
        for s in self.setas.values():
            self.desenhar_seta(s)
        for f in self.formas.values():
            self.desenhar_forma(f)

        if not self.formas:
            meio_x = c.canvasx(c.winfo_width() / 2)
            meio_y = c.canvasy(c.winfo_height() / 2)
            c.create_text(meio_x, meio_y, fill="#9a9a9a", font=self.fonte(13), justify="center",
                          text="Escolha uma forma no painel à esquerda e clique aqui na folha.\n\n"
                               "Quer ver um exemplo pronto? Ajuda › Carregar exemplo",
                          tags="conteudo")
        self.atualizar_informacoes()

    def desenhar_forma(self, f):
        c = self.canvas
        z = self.zoom
        marca = f"f{f['id']}"
        selecionada = f["id"] in self.sel_formas
        contorno, espessura = COR_CONTORNO, 1.5
        if f["id"] == self.origem_ligacao:
            contorno, espessura = COR_LIGACAO, 3
        elif selecionada:
            contorno, espessura = COR_SELECAO, 3

        pontos = [coord * z for p in self.pontos_forma(f) for coord in p]
        c.create_polygon(pontos, fill=f["cor"], outline=contorno, width=espessura, tags=("conteudo", marca))

        base = (f["y"] + f["h"] / 2) * z
        for linha in self.detalhes_forma(f):
            c.create_line([coord * z for p in linha for coord in p], fill=contorno, width=espessura,
                          tags=("conteudo", marca))

        tx, ty = self.centro_texto(f)
        c.create_text(tx * z, ty * z, text=f["texto"], width=max(10, self.largura_texto(f) * z),
                      justify="center", fill="#1a1a1a", font=self.fonte(10 * z), tags=("conteudo", marca))

        if selecionada and len(self.sel_formas) == 1:
            ax, ay = (f["x"] + f["w"] / 2) * z, base
            c.create_rectangle(ax - 5, ay - 5, ax + 5, ay + 5, fill=COR_SELECAO, outline="white",
                               tags=("conteudo", "alca", marca))

    def desenhar_seta(self, s):
        c = self.canvas
        z = self.zoom
        marca = f"s{s['id']}"
        selecionada = s["id"] in self.sel_setas
        cor = COR_SELECAO if selecionada else COR_SETA
        pontos = self.pontos_seta(s)

        c.create_line([coord * z for p in pontos for coord in p], fill=cor, width=3 if selecionada else 2,
                      arrow=tk.LAST, arrowshape=(12 * z, 14 * z, 5 * z), tags=("conteudo", marca))

        if s["rotulo"]:
            mx, my = self.meio_da_linha(pontos)
            texto = c.create_text(mx * z, my * z, text=s["rotulo"], fill=cor, font=self.fonte(9 * z),
                                  tags=("conteudo", marca))
            x1, y1, x2, y2 = c.bbox(texto)
            fundo = c.create_rectangle(x1 - 4, y1 - 1, x2 + 4, y2 + 1, fill=COR_PAPEL, outline=cor,
                                       tags=("conteudo", marca))
            c.tag_raise(texto, fundo)

    def atualizar_informacoes(self):
        self.lbl_contagem.config(text=f"Formas: {len(self.formas)}   Setas: {len(self.setas)}")
        self.lbl_zoom.config(text=f"Zoom {round(self.zoom * 100)}%")

        if len(self.sel_formas) == 1 and not self.sel_setas:
            f = self.formas[next(iter(self.sel_formas))]
            ligacoes = sum(1 for s in self.setas.values() if f["id"] in (s["origem"], s["destino"]))
            texto = f"{TIPOS[f['tipo']]['nome']}  •  {round(f['w'])} × {round(f['h'])}\n" \
                    f"{ligacoes} seta(s) • o quadradinho azul redimensiona"
        elif len(self.sel_setas) == 1 and not self.sel_formas:
            s = self.setas[next(iter(self.sel_setas))]
            origem = self.formas[s["origem"]]["texto"].replace("\n", " ")
            destino = self.formas[s["destino"]]["texto"].replace("\n", " ")
            texto = f"Seta: {origem} → {destino}"
        elif self.sel_formas or self.sel_setas:
            texto = f"{len(self.sel_formas)} forma(s) e {len(self.sel_setas)} seta(s) selecionadas."
        else:
            texto = "Nada selecionado."
        self.lbl_selecao.config(text=texto)

    def mostrar_aviso(self, texto):
        self.lbl_dica.config(text=texto, fg=COR_TITULO)
        if self.aviso_id:
            self.janela.after_cancel(self.aviso_id)
        self.aviso_id = self.janela.after(3000, self.mostrar_dica)

    def mostrar_dica(self):
        self.aviso_id = None
        if self.ferramenta == "selecionar":
            dica = "Clique para selecionar • arraste para mover • duplo clique edita o texto"
        elif self.ferramenta == "ligar":
            dica = "Clique na forma de ORIGEM e depois na de DESTINO • Esc cancela"
        else:
            dica = f"Clique na folha para colocar: {TIPOS[self.ferramenta]['nome']}"
        self.lbl_dica.config(text=dica, fg=COR_TEXTO_SUAVE)

    # ------------------------------------------------------------ ferramentas

    def escolher_ferramenta(self, nome):
        self.fechar_editor(True)
        self.ferramenta = nome
        self.origem_ligacao = None
        self.canvas.delete("previa")
        for chave, opcao in self.botoes_ferramenta.items():
            opcao.configure(bg=COR_SELECAO if chave == nome else COR_BOTAO)
        self.canvas.configure(cursor="arrow" if nome == "selecionar" else "crosshair")
        self.mostrar_dica()
        self.redesenhar()

    def cancelar(self):
        if self.origem_ligacao is not None:
            self.origem_ligacao = None
            self.canvas.delete("previa")
        elif self.ferramenta != "selecionar":
            self.escolher_ferramenta("selecionar")
            return
        else:
            self.sel_formas.clear()
            self.sel_setas.clear()
        self.redesenhar()

    def item_em(self, cx, cy):
        itens = self.canvas.find_overlapping(cx - 3, cy - 3, cx + 3, cy + 3)
        for item in reversed(itens):
            marcas = self.canvas.gettags(item)
            if "alca" in marcas:
                for m in marcas:
                    if m[0] == "f" and m[1:].isdigit():
                        return "alca", int(m[1:])
        for item in reversed(itens):
            for m in self.canvas.gettags(item):
                if m[0] == "f" and m[1:].isdigit():
                    return "forma", int(m[1:])
                if m[0] == "s" and m[1:].isdigit():
                    return "seta", int(m[1:])
        return None

    def ao_clicar(self, e):
        self.fechar_editor(True)
        self.canvas.focus_set()
        z = self.zoom
        cx, cy = self.canvas.canvasx(e.x), self.canvas.canvasy(e.y)
        mx, my = cx / z, cy / z
        alvo = self.item_em(cx, cy)
        shift = bool(e.state & 0x0001)

        if self.ferramenta in TIPOS:
            self.criar_forma(self.ferramenta, mx, my)
            self.escolher_ferramenta("selecionar")
            return

        if self.ferramenta == "ligar":
            if alvo and alvo[0] in ("forma", "alca"):
                if self.origem_ligacao is None:
                    self.origem_ligacao = alvo[1]
                elif alvo[1] != self.origem_ligacao:
                    self.criar_seta(self.origem_ligacao, alvo[1])
                    self.origem_ligacao = None
                    self.canvas.delete("previa")
            else:
                self.origem_ligacao = None
                self.canvas.delete("previa")
            self.redesenhar()
            return

        if alvo and alvo[0] == "alca":
            f = self.formas[alvo[1]]
            self.arraste = {"tipo": "redimensionar", "id": alvo[1], "inicio": (mx, my),
                            "original": (f["x"] - f["w"] / 2, f["y"] - f["h"] / 2, f["w"], f["h"]),
                            "estado": self.foto(), "moveu": False}
        elif alvo and alvo[0] == "forma":
            fid = alvo[1]
            if shift and fid in self.sel_formas:
                self.sel_formas.discard(fid)
                self.arraste = None
            else:
                if shift:
                    self.sel_formas.add(fid)
                elif fid not in self.sel_formas:
                    self.sel_formas = {fid}
                    self.sel_setas = set()
                self.arraste = {"tipo": "mover", "inicio": (mx, my), "referencia": fid,
                                "original": {i: (self.formas[i]["x"], self.formas[i]["y"]) for i in self.sel_formas},
                                "estado": self.foto(), "moveu": False}
        elif alvo and alvo[0] == "seta":
            sid = alvo[1]
            if shift:
                self.sel_setas ^= {sid}
            else:
                self.sel_setas = {sid}
                self.sel_formas = set()
            self.arraste = None
        else:
            if not shift:
                self.sel_formas = set()
                self.sel_setas = set()
            self.arraste = {"tipo": "caixa", "inicio": (cx, cy)}
        self.redesenhar()

    def ao_arrastar(self, e):
        a = self.arraste
        if not a:
            return
        z = self.zoom
        cx, cy = self.canvas.canvasx(e.x), self.canvas.canvasy(e.y)
        mx, my = cx / z, cy / z

        if a["tipo"] == "caixa":
            self.canvas.delete("caixa_selecao")
            x0, y0 = a["inicio"]
            self.canvas.create_rectangle(x0, y0, cx, cy, outline=COR_SELECAO, dash=(4, 2),
                                         tags="caixa_selecao")
            return

        dx, dy = mx - a["inicio"][0], my - a["inicio"][1]
        if not a["moveu"] and abs(dx) * z < 3 and abs(dy) * z < 3:
            return
        a["moveu"] = True

        if a["tipo"] == "mover":
            rx, ry = a["original"][a["referencia"]]
            dx = self.encaixar(rx + dx) - rx
            dy = self.encaixar(ry + dy) - ry
            for i, (ox, oy) in a["original"].items():
                f = self.formas[i]
                f["x"] = max(f["w"] / 2, ox + dx)
                f["y"] = max(f["h"] / 2, oy + dy)
        else:
            f = self.formas[a["id"]]
            esq, topo, w, h = a["original"]
            nova_w = max(40, self.encaixar(esq + w + dx) - esq)
            nova_h = max(30, self.encaixar(topo + h + dy) - topo)
            f["w"], f["h"] = nova_w, nova_h
            f["x"], f["y"] = esq + nova_w / 2, topo + nova_h / 2
        self.redesenhar()

    def ao_soltar(self, e):
        a = self.arraste
        self.arraste = None
        if not a:
            return
        if a["tipo"] == "caixa":
            self.canvas.delete("caixa_selecao")
            z = self.zoom
            x0, y0 = a["inicio"]
            x1, y1 = self.canvas.canvasx(e.x), self.canvas.canvasy(e.y)
            esq, dir = sorted((x0 / z, x1 / z))
            topo, base = sorted((y0 / z, y1 / z))
            if dir - esq > 2 or base - topo > 2:
                for f in self.formas.values():
                    if esq <= f["x"] <= dir and topo <= f["y"] <= base:
                        self.sel_formas.add(f["id"])
                for s in self.setas.values():
                    if s["origem"] in self.sel_formas and s["destino"] in self.sel_formas:
                        self.sel_setas.add(s["id"])
            self.redesenhar()
        elif a["moveu"]:
            self.registrar(a["estado"])
            self.redesenhar_tudo()

    def ao_duplo_clique(self, e):
        if self.ferramenta != "selecionar":
            self.ao_clicar(e)
            return
        z = self.zoom
        cx, cy = self.canvas.canvasx(e.x), self.canvas.canvasy(e.y)
        alvo = self.item_em(cx, cy)
        if alvo and alvo[0] in ("forma", "alca"):
            self.editar_texto_forma(alvo[1])
        elif alvo and alvo[0] == "seta":
            self.editar_rotulo_seta(alvo[1])
        else:
            fid = self.criar_forma("processo", cx / z, cy / z)
            self.editar_texto_forma(fid)

    def ao_mover_mouse(self, e):
        z = self.zoom
        cx, cy = self.canvas.canvasx(e.x), self.canvas.canvasy(e.y)
        self.lbl_coord.config(text=f"{round(cx / z)}, {round(cy / z)}")
        self.canvas.delete("previa")
        if self.ferramenta == "ligar" and self.origem_ligacao in self.formas:
            f = self.formas[self.origem_ligacao]
            x0, y0 = self.ponto_borda(f, cx / z, cy / z)
            self.canvas.create_line(x0 * z, y0 * z, cx, cy, fill=COR_LIGACAO, width=2, dash=(6, 3),
                                    arrow=tk.LAST, tags="previa")

    def ao_rodinha(self, e):
        passos = -1 if e.delta > 0 else 1
        if e.state & 0x0004:
            self.mudar_zoom(1.25 if e.delta > 0 else 0.8, (e.x, e.y))
        elif e.state & 0x0001:
            self.canvas.xview_scroll(passos, "units")
        else:
            self.canvas.yview_scroll(passos, "units")
        self.redesenhar()

    def menu_de_tipos(self, pai, comando):
        submenu = tk.Menu(pai, tearoff=0)
        for categoria, titulo in (("basica", "Formas básicas"), ("especial", "Formas especiais")):
            submenu.add_command(label=titulo, state="disabled")
            for tipo, dados in TIPOS.items():
                if dados["categoria"] == categoria:
                    submenu.add_command(label=f"   {dados['nome']}", command=lambda t=tipo: comando(t))
            if categoria == "basica":
                submenu.add_separator()
        return submenu

    def ao_botao_direito(self, e):
        self.fechar_editor(True)
        if self.ferramenta != "selecionar":
            self.escolher_ferramenta("selecionar")
        z = self.zoom
        cx, cy = self.canvas.canvasx(e.x), self.canvas.canvasy(e.y)
        alvo = self.item_em(cx, cy)
        menu = tk.Menu(self.janela, tearoff=0)

        if alvo and alvo[0] in ("forma", "alca"):
            fid = alvo[1]
            if fid not in self.sel_formas:
                self.sel_formas, self.sel_setas = {fid}, set()
            menu.add_command(label="Editar texto", command=lambda: self.editar_texto_forma(fid))
            menu.add_cascade(label="Trocar forma por", menu=self.menu_de_tipos(menu, self.trocar_tipo))
            menu.add_command(label=f"Ver \"{TIPOS[self.formas[fid]['tipo']]['nome']}\" no manual",
                             command=lambda: self.abrir_manual(self.formas[fid]["tipo"]))
            menu.add_command(label="Escolher cor...", command=self.escolher_outra_cor)
            menu.add_separator()
            menu.add_command(label="Copiar", command=self.copiar)
            menu.add_command(label="Duplicar", command=self.duplicar)
            menu.add_command(label="Trazer para frente", command=self.trazer_frente)
            menu.add_command(label="Enviar para trás", command=self.enviar_tras)
            menu.add_separator()
            menu.add_command(label="Apagar", command=self.apagar_selecao)
        elif alvo and alvo[0] == "seta":
            sid = alvo[1]
            self.sel_formas, self.sel_setas = set(), {sid}
            menu.add_command(label="Editar rótulo", command=lambda: self.editar_rotulo_seta(sid))
            menu.add_command(label="Inverter direção", command=lambda: self.inverter_seta(sid))
            menu.add_separator()
            menu.add_command(label="Apagar", command=self.apagar_selecao)
        else:
            menu.add_cascade(label="Inserir aqui",
                             menu=self.menu_de_tipos(menu, lambda t: self.criar_forma(t, cx / z, cy / z)))
            menu.add_command(label="Colar", command=self.colar,
                             state="normal" if self.area_transferencia else "disabled")
            menu.add_separator()
            menu.add_command(label="Selecionar tudo", command=self.selecionar_tudo)
            menu.add_command(label="Ajustar à tela", command=self.ajustar_tela)

        self.redesenhar()
        menu.tk_popup(e.x_root, e.y_root)

    # ------------------------------------------------------------ edição de texto

    def editar_texto_forma(self, fid):
        f = self.formas.get(fid)
        if not f:
            return
        z = self.zoom
        largura = max(120, self.largura_texto(f) * z + 20)
        self.abrir_editor("forma", fid, f["texto"], f["x"] * z, f["y"] * z, largura)

    def editar_rotulo_seta(self, sid):
        s = self.setas.get(sid)
        if not s:
            return
        z = self.zoom
        mx, my = self.meio_da_linha(self.pontos_seta(s))
        self.abrir_editor("seta", sid, s["rotulo"], mx * z, my * z, 120)

    def abrir_editor(self, tipo, ident, texto, x, y, largura):
        self.fechar_editor(True)
        caixa = tk.Text(self.canvas, wrap="word", font=self.fonte(11), bd=1, relief="solid",
                        bg="#fffde7", fg="#1a1a1a", insertbackground="#1a1a1a", undo=True)
        caixa.insert("1.0", texto)
        caixa.tag_add("sel", "1.0", "end-1c")
        linhas = max(2, texto.count("\n") + 2)
        janela = self.canvas.create_window(x, y, window=caixa, width=largura, height=linhas * 22 + 6)
        self.editor = {"tipo": tipo, "id": ident, "caixa": caixa, "janela": janela, "original": texto}

        caixa.bind("<Return>", lambda e: (self.fechar_editor(True), "break")[1])
        caixa.bind("<Shift-Return>", lambda e: None)
        caixa.bind("<Escape>", lambda e: (self.fechar_editor(False), "break")[1])
        caixa.bind("<FocusOut>", lambda e: self.fechar_editor(True))
        caixa.focus_set()

    def fechar_editor(self, salvar):
        ed = self.editor
        if not ed:
            return
        self.editor = None
        novo = ed["caixa"].get("1.0", "end-1c").strip()
        self.canvas.delete(ed["janela"])
        ed["caixa"].destroy()
        self.canvas.focus_set()

        if salvar and novo != ed["original"]:
            if ed["tipo"] == "forma" and ed["id"] in self.formas:
                self.registrar()
                self.formas[ed["id"]]["texto"] = novo
            elif ed["tipo"] == "seta" and ed["id"] in self.setas:
                self.registrar()
                self.setas[ed["id"]]["rotulo"] = novo
        self.redesenhar()

    # ------------------------------------------------------------ ações

    def novo_id(self):
        ident = self.proximo_id
        self.proximo_id += 1
        return ident

    def criar_forma(self, tipo, x, y):
        self.registrar()
        dados = TIPOS[tipo]
        texto = dados["texto"]
        if tipo == "terminal" and any(f["tipo"] == "terminal" for f in self.formas.values()):
            texto = "Fim"
        fid = self.novo_id()
        self.formas[fid] = {
            "id": fid, "tipo": tipo, "texto": texto, "cor": dados["cor"],
            "x": max(dados["w"] / 2, self.encaixar(x)), "y": max(dados["h"] / 2, self.encaixar(y)),
            "w": dados["w"], "h": dados["h"],
        }
        self.sel_formas, self.sel_setas = {fid}, set()
        self.redesenhar_tudo()
        return fid

    def criar_seta(self, origem, destino):
        for s in self.setas.values():
            if s["origem"] == origem and s["destino"] == destino:
                self.mostrar_aviso("Essas duas formas já estão ligadas nesse sentido.")
                return
        self.registrar()
        rotulo = ""
        if self.formas[origem]["tipo"] == "decisao":
            saidas = sum(1 for s in self.setas.values() if s["origem"] == origem)
            rotulo = ["Sim", "Não"][saidas] if saidas < 2 else ""
        sid = self.novo_id()
        self.setas[sid] = {"id": sid, "origem": origem, "destino": destino, "rotulo": rotulo}
        self.redesenhar_tudo()

    def inverter_seta(self, sid):
        s = self.setas.get(sid)
        if s:
            self.registrar()
            s["origem"], s["destino"] = s["destino"], s["origem"]
            self.redesenhar()

    def trocar_tipo(self, tipo):
        if not self.sel_formas:
            return
        self.registrar()
        for fid in self.sel_formas:
            f = self.formas[fid]
            f["tipo"] = tipo
            f["w"], f["h"] = TIPOS[tipo]["w"], TIPOS[tipo]["h"]
        self.redesenhar_tudo()

    def aplicar_cor(self, cor):
        if not self.sel_formas:
            self.mostrar_aviso("Selecione uma ou mais formas para pintar.")
            return
        self.registrar()
        for fid in self.sel_formas:
            self.formas[fid]["cor"] = cor
        self.redesenhar()

    def escolher_outra_cor(self):
        if not self.sel_formas:
            self.mostrar_aviso("Selecione uma ou mais formas para pintar.")
            return
        atual = self.formas[next(iter(self.sel_formas))]["cor"]
        escolhida = colorchooser.askcolor(color=atual, title="Cor da forma")[1]
        if escolhida:
            self.aplicar_cor(escolhida)

    def apagar_selecao(self):
        if not self.sel_formas and not self.sel_setas:
            return
        self.registrar()
        for fid in self.sel_formas:
            self.formas.pop(fid, None)
        for sid in list(self.setas):
            s = self.setas[sid]
            if sid in self.sel_setas or s["origem"] not in self.formas or s["destino"] not in self.formas:
                del self.setas[sid]
        self.sel_formas, self.sel_setas = set(), set()
        self.redesenhar_tudo()

    def selecionar_tudo(self):
        self.sel_formas = set(self.formas)
        self.sel_setas = set(self.setas)
        self.redesenhar()

    def copiar(self):
        if not self.sel_formas:
            return
        formas = [self.formas[i] for i in self.sel_formas]
        setas = [s for s in self.setas.values()
                 if s["origem"] in self.sel_formas and s["destino"] in self.sel_formas]
        self.area_transferencia = json.dumps({"formas": formas, "setas": setas})
        self.colagens = 0
        self.mostrar_aviso(f"{len(formas)} forma(s) copiada(s).")

    def colar(self):
        if not self.area_transferencia:
            return
        self.registrar()
        dados = json.loads(self.area_transferencia)
        self.colagens += 1
        deslocamento = GRADE * 2 * self.colagens
        novos_ids = {}
        self.sel_formas, self.sel_setas = set(), set()
        for f in dados["formas"]:
            fid = self.novo_id()
            novos_ids[f["id"]] = fid
            f.update(id=fid, x=f["x"] + deslocamento, y=f["y"] + deslocamento)
            self.formas[fid] = f
            self.sel_formas.add(fid)
        for s in dados["setas"]:
            sid = self.novo_id()
            s.update(id=sid, origem=novos_ids[s["origem"]], destino=novos_ids[s["destino"]])
            self.setas[sid] = s
            self.sel_setas.add(sid)
        self.redesenhar_tudo()

    def duplicar(self):
        if self.sel_formas:
            self.copiar()
            self.colar()

    def trazer_frente(self):
        if not self.sel_formas:
            return
        self.registrar()
        for fid in [i for i in self.formas if i in self.sel_formas]:
            self.formas[fid] = self.formas.pop(fid)
        self.redesenhar()

    def enviar_tras(self):
        if not self.sel_formas:
            return
        self.registrar()
        primeiro = {i: f for i, f in self.formas.items() if i in self.sel_formas}
        resto = {i: f for i, f in self.formas.items() if i not in self.sel_formas}
        self.formas = {**primeiro, **resto}
        self.redesenhar()

    def mover_selecao(self, dx, dy, fino):
        if not self.sel_formas:
            return
        self.registrar()
        passo = 1 if fino else (GRADE if self.var_encaixe.get() else 5)
        for fid in self.sel_formas:
            f = self.formas[fid]
            f["x"] = max(f["w"] / 2, f["x"] + dx * passo)
            f["y"] = max(f["h"] / 2, f["y"] + dy * passo)
        self.redesenhar_tudo()

    def alternar_cotovelo(self):
        self.marcar_modificado()
        self.redesenhar_tudo()

    # ------------------------------------------------------------ desfazer / refazer

    def foto(self):
        return json.dumps({
            "formas": list(self.formas.values()),
            "setas": list(self.setas.values()),
            "proximo_id": self.proximo_id,
            "cotovelo": self.var_cotovelo.get(),
        }, ensure_ascii=False)

    def carregar_foto(self, dados):
        self.formas = {f["id"]: f for f in dados.get("formas", [])}
        self.setas = {s["id"]: s for s in dados.get("setas", [])
                      if s["origem"] in self.formas and s["destino"] in self.formas}
        todos = list(self.formas) + list(self.setas)
        self.proximo_id = max([dados.get("proximo_id", 1)] + [i + 1 for i in todos])
        self.var_cotovelo.set(dados.get("cotovelo", False))
        self.sel_formas &= set(self.formas)
        self.sel_setas &= set(self.setas)

    def registrar(self, estado=None):
        self.pilha_desfazer.append(estado or self.foto())
        if len(self.pilha_desfazer) > LIMITE_DESFAZER:
            self.pilha_desfazer.pop(0)
        self.pilha_refazer.clear()
        self.marcar_modificado()

    def desfazer(self):
        self.fechar_editor(True)
        if not self.pilha_desfazer:
            self.mostrar_aviso("Nada para desfazer.")
            return
        self.pilha_refazer.append(self.foto())
        self.carregar_foto(json.loads(self.pilha_desfazer.pop()))
        self.marcar_modificado()
        self.redesenhar_tudo()

    def refazer(self):
        self.fechar_editor(True)
        if not self.pilha_refazer:
            self.mostrar_aviso("Nada para refazer.")
            return
        self.pilha_desfazer.append(self.foto())
        self.carregar_foto(json.loads(self.pilha_refazer.pop()))
        self.marcar_modificado()
        self.redesenhar_tudo()

    # ------------------------------------------------------------ zoom

    def definir_zoom(self, novo, foco=None):
        self.fechar_editor(True)
        novo = min(ZOOM_MAX, max(ZOOM_MIN, novo))
        c = self.canvas
        if foco is None:
            foco = (c.winfo_width() / 2, c.winfo_height() / 2)
        mundo_x = c.canvasx(foco[0]) / self.zoom
        mundo_y = c.canvasy(foco[1]) / self.zoom

        self.zoom = novo
        self.redesenhar_tudo()
        largura, altura = self.tamanho_mundo()
        c.xview_moveto(max(0, (mundo_x * novo - foco[0]) / (largura * novo)))
        c.yview_moveto(max(0, (mundo_y * novo - foco[1]) / (altura * novo)))
        self.redesenhar()

    def mudar_zoom(self, fator, foco=None):
        self.definir_zoom(self.zoom * fator, foco)

    def ajustar_tela(self):
        limites = self.limites_conteudo()
        if not limites:
            self.definir_zoom(1.0)
            return
        x0, y0, x1, y1 = limites
        c = self.canvas
        largura_tela, altura_tela = max(100, c.winfo_width()), max(100, c.winfo_height())
        novo = min(largura_tela / (x1 - x0 + 120), altura_tela / (y1 - y0 + 120), 1.5)
        self.zoom = min(ZOOM_MAX, max(ZOOM_MIN, novo))
        self.redesenhar_tudo()
        largura, altura = self.tamanho_mundo()
        z = self.zoom
        c.xview_moveto(max(0, ((x0 + x1) / 2 * z - largura_tela / 2) / (largura * z)))
        c.yview_moveto(max(0, ((y0 + y1) / 2 * z - altura_tela / 2) / (altura * z)))
        self.redesenhar()

    # ------------------------------------------------------------ arquivos

    def marcar_modificado(self):
        self.modificado = True
        self.atualizar_titulo()

    def atualizar_titulo(self):
        nome = os.path.basename(self.arquivo_atual) if self.arquivo_atual else "Sem título"
        self.janela.title(f"Fluxograma — {nome}{' *' if self.modificado else ''}")

    def confirmar_descartar(self):
        self.fechar_editor(True)
        if not self.modificado:
            return True
        resposta = messagebox.askyesnocancel("Fluxograma", "Salvar as alterações antes de continuar?")
        if resposta is None:
            return False
        if resposta:
            return self.salvar()
        return True

    def comecar_do_zero(self, dados=None, arquivo=None):
        self.formas, self.setas = {}, {}
        self.proximo_id = 1
        self.sel_formas, self.sel_setas = set(), set()
        self.var_cotovelo.set(False)
        if dados:
            self.carregar_foto(dados)
        self.pilha_desfazer.clear()
        self.pilha_refazer.clear()
        self.arquivo_atual = arquivo
        self.modificado = False
        self.atualizar_titulo()
        self.escolher_ferramenta("selecionar")
        self.zoom = 1.0
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        self.redesenhar_tudo()

    def novo(self):
        if self.confirmar_descartar():
            self.comecar_do_zero()

    def abrir(self):
        if not self.confirmar_descartar():
            return
        caminho = filedialog.askopenfilename(
            title="Abrir fluxograma", initialdir=PASTA_FLUXOGRAMAS if os.path.isdir(PASTA_FLUXOGRAMAS) else None,
            filetypes=[("Fluxograma", "*.json"), ("Todos os arquivos", "*.*")])
        if caminho:
            self.abrir_arquivo(caminho)

    def abrir_arquivo(self, caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            if not isinstance(dados.get("formas"), list):
                raise ValueError("o arquivo não tem a lista de formas")
            for f in dados["formas"]:
                if f.get("tipo") not in TIPOS:
                    raise ValueError(f"tipo de forma desconhecido: {f.get('tipo')}")
        except (OSError, ValueError, KeyError, AttributeError) as erro:
            messagebox.showerror("Fluxograma", f"Não foi possível abrir o arquivo.\n\n{erro}")
            return False
        self.comecar_do_zero(dados, caminho)
        self.mostrar_aviso(f"Aberto: {os.path.basename(caminho)}")
        return True

    def salvar(self):
        if not self.arquivo_atual:
            return self.salvar_como()
        return self.escrever_arquivo(self.arquivo_atual)

    def salvar_como(self):
        os.makedirs(PASTA_FLUXOGRAMAS, exist_ok=True)
        caminho = filedialog.asksaveasfilename(
            title="Salvar fluxograma", initialdir=PASTA_FLUXOGRAMAS, initialfile="meu_fluxograma.json",
            defaultextension=".json", filetypes=[("Fluxograma", "*.json")])
        if not caminho:
            return False
        return self.escrever_arquivo(caminho)

    def escrever_arquivo(self, caminho):
        self.fechar_editor(True)
        dados = {"programa": "Fluxograma", "versao": 1, **json.loads(self.foto())}
        try:
            with open(caminho, "w", encoding="utf-8") as arquivo:
                json.dump(dados, arquivo, ensure_ascii=False, indent=2)
        except OSError as erro:
            messagebox.showerror("Fluxograma", f"Não foi possível salvar.\n\n{erro}")
            return False
        self.arquivo_atual = caminho
        self.modificado = False
        self.atualizar_titulo()
        self.mostrar_aviso(f"Salvo em {os.path.basename(caminho)}")
        return True

    # ------------------------------------------------------------ exportar imagem

    def carregar_fonte_pil(self, tamanho):
        for nome in ("segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"):
            try:
                return ImageFont.truetype(nome, tamanho)
            except OSError:
                continue
        return ImageFont.load_default(tamanho)

    def quebrar_texto(self, texto, fonte_pil, largura):
        linhas = []
        for paragrafo in texto.split("\n"):
            atual = ""
            for palavra in paragrafo.split(" "):
                tentativa = f"{atual} {palavra}".strip()
                if atual and fonte_pil.getlength(tentativa) > largura:
                    linhas.append(atual)
                    atual = palavra
                else:
                    atual = tentativa
            linhas.append(atual)
        return "\n".join(linhas)

    def exportar_png(self, caminho=None):
        self.fechar_editor(True)
        if not self.formas:
            self.mostrar_aviso("O fluxograma está vazio, não há o que exportar.")
            return False
        if not TEM_PIL:
            messagebox.showerror("Fluxograma", "Para exportar PNG instale o Pillow:\n\npip install pillow")
            return False
        if caminho is None:
            nome = os.path.splitext(os.path.basename(self.arquivo_atual))[0] if self.arquivo_atual else "fluxograma"
            os.makedirs(PASTA_FLUXOGRAMAS, exist_ok=True)
            caminho = filedialog.asksaveasfilename(
                title="Exportar como imagem", initialdir=PASTA_FLUXOGRAMAS, initialfile=f"{nome}.png",
                defaultextension=".png", filetypes=[("Imagem PNG", "*.png")])
            if not caminho:
                return False

        escala, margem = 2, 40
        x0, y0, x1, y1 = self.limites_conteudo()
        imagem = Image.new("RGB", (int((x1 - x0 + 2 * margem) * escala), int((y1 - y0 + 2 * margem) * escala)), "white")
        pincel = ImageDraw.Draw(imagem)
        fonte_forma = self.carregar_fonte_pil(13 * escala)
        fonte_rotulo = self.carregar_fonte_pil(12 * escala)

        def tela(p):
            return (p[0] - x0 + margem) * escala, (p[1] - y0 + margem) * escala

        for s in self.setas.values():
            pontos = [tela(p) for p in self.pontos_seta(s)]
            (ax, ay), (bx, by) = pontos[-2], pontos[-1]
            angulo = math.atan2(by - ay, bx - ax)
            comprimento, abertura = 13 * escala, 5.5 * escala
            base_x, base_y = bx - comprimento * math.cos(angulo), by - comprimento * math.sin(angulo)
            pincel.line(pontos[:-1] + [(base_x, base_y)], fill=COR_SETA, width=2 * escala, joint="curve")
            pincel.polygon([(bx, by),
                            (base_x + abertura * math.sin(angulo), base_y - abertura * math.cos(angulo)),
                            (base_x - abertura * math.sin(angulo), base_y + abertura * math.cos(angulo))],
                           fill=COR_SETA)

        for f in self.formas.values():
            pincel.polygon([tela(p) for p in self.pontos_forma(f)], fill=f["cor"], outline=COR_CONTORNO, width=2)
            for linha in self.detalhes_forma(f):
                pincel.line([tela(p) for p in linha], fill=COR_CONTORNO, width=2)
            texto = self.quebrar_texto(f["texto"], fonte_forma, self.largura_texto(f) * escala)
            pincel.multiline_text(tela(self.centro_texto(f)), texto, font=fonte_forma, fill="#1a1a1a",
                                  anchor="mm", align="center", spacing=3 * escala)

        for s in self.setas.values():
            if s["rotulo"]:
                centro = tela(self.meio_da_linha(self.pontos_seta(s)))
                caixa = pincel.multiline_textbbox(centro, s["rotulo"], font=fonte_rotulo, anchor="mm")
                pincel.rectangle((caixa[0] - 8, caixa[1] - 3, caixa[2] + 8, caixa[3] + 3),
                                 fill="white", outline=COR_SETA, width=2)
                pincel.multiline_text(centro, s["rotulo"], font=fonte_rotulo, fill=COR_SETA,
                                      anchor="mm", align="center")

        try:
            imagem.save(caminho)
        except OSError as erro:
            messagebox.showerror("Fluxograma", f"Não foi possível exportar.\n\n{erro}")
            return False
        self.mostrar_aviso(f"Imagem exportada: {os.path.basename(caminho)}")
        return True

    # ------------------------------------------------------------ ajuda

    def abrir_manual(self, topico=None):
        if self.janela_manual and self.janela_manual.winfo_exists():
            self.janela_manual.deiconify()
            self.janela_manual.lift()
        else:
            self.criar_janela_manual()
        if topico is None:
            topico = self.topico_manual or "Primeiros passos"
        self.mostrar_topico(topico)

    def criar_janela_manual(self):
        janela = tk.Toplevel(self.janela)
        janela.title("Manual de instruções — Fluxograma")
        janela.geometry("920x620")
        janela.minsize(700, 450)
        janela.configure(bg=COR_FUNDO)
        janela.bind("<Escape>", lambda e: janela.destroy())
        self.janela_manual = janela

        self.itens_manual = [("GUIA", None)]
        self.itens_manual += [(f"   {nome}", nome) for nome in MANUAL_GERAL]
        self.itens_manual.append(("FORMAS BÁSICAS", None))
        self.itens_manual += [(f"   {d['nome']}", t) for t, d in TIPOS.items() if d["categoria"] == "basica"]
        self.itens_manual.append(("FORMAS ESPECIAIS", None))
        self.itens_manual += [(f"   {d['nome']}", t) for t, d in TIPOS.items() if d["categoria"] == "especial"]
        self.itens_manual += [("OUTROS", None), ("   Atalhos do teclado", "atalhos")]

        lista = tk.Listbox(janela, width=26, bg=COR_PAINEL, fg=COR_TEXTO, font=self.fonte_botao, bd=0,
                           highlightthickness=0, selectbackground=COR_SELECAO, activestyle="none")
        lista.pack(side="left", fill="y", padx=(10, 0), pady=10)
        for i, (rotulo, chave) in enumerate(self.itens_manual):
            lista.insert("end", rotulo)
            if chave is None:
                lista.itemconfig(i, fg=COR_TITULO, selectbackground=COR_PAINEL, selectforeground=COR_TITULO)
        lista.bind("<<ListboxSelect>>", self.ao_escolher_topico)
        self.lista_manual = lista

        direita = tk.Frame(janela, bg=COR_FUNDO)
        direita.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.lbl_topico = tk.Label(direita, text="", bg=COR_FUNDO, fg=COR_TEXTO, anchor="w",
                                   font=font.Font(family="Segoe UI", size=16, weight="bold"))
        self.lbl_topico.pack(fill="x")
        self.lbl_resumo = tk.Label(direita, text="", bg=COR_FUNDO, fg=COR_TEXTO_SUAVE, anchor="w",
                                   justify="left", font=self.fonte_botao, wraplength=600)
        self.lbl_resumo.pack(fill="x", pady=(0, 6))
        self.desenho_manual = tk.Canvas(direita, height=150, bg=COR_PAPEL, highlightthickness=0)

        quadro_texto = tk.Frame(direita, bg=COR_FUNDO)
        quadro_texto.pack(fill="both", expand=True)
        self.texto_manual = tk.Text(quadro_texto, wrap="word", bg=COR_PAINEL, fg=COR_TEXTO, bd=0, padx=16, pady=12,
                                    font=font.Font(family="Segoe UI", size=11), spacing1=2, spacing3=2,
                                    highlightthickness=0, cursor="arrow")
        rolagem = tk.Scrollbar(quadro_texto, orient="vertical", command=self.texto_manual.yview)
        self.texto_manual.configure(yscrollcommand=rolagem.set)
        rolagem.pack(side="right", fill="y")
        self.texto_manual.pack(side="left", fill="both", expand=True)
        self.texto_manual.tag_configure("titulo", foreground=COR_TITULO,
                                        font=font.Font(family="Segoe UI", size=10, weight="bold"), spacing1=8)
        self.texto_manual.tag_configure("mono", font=self.fonte_status)

    def ao_escolher_topico(self, e):
        selecao = self.lista_manual.curselection()
        if not selecao:
            return
        indice = selecao[0]
        chave = self.itens_manual[indice][1]
        if chave is None:
            if indice + 1 < len(self.itens_manual):
                self.mostrar_topico(self.itens_manual[indice + 1][1])
            return
        if chave != self.topico_manual:
            self.mostrar_topico(chave)

    def mostrar_topico(self, chave):
        self.topico_manual = chave
        for i, (rotulo, item) in enumerate(self.itens_manual):
            if item == chave:
                self.lista_manual.selection_clear(0, "end")
                self.lista_manual.selection_set(i)
                self.lista_manual.see(i)

        self.desenho_manual.pack_forget()
        if chave in TIPOS:
            dados = TIPOS[chave]
            grupo = "Forma básica" if dados["categoria"] == "basica" else "Forma especial"
            self.lbl_topico.config(text=dados["nome"])
            self.lbl_resumo.config(text=f"{grupo} — {dados['descricao']}")
            conteudo = dados["manual"]
            tela = self.desenho_manual
            tela.pack(fill="x", pady=(0, 8), before=self.texto_manual.master)
            tela.delete("all")
            tela.update_idletasks()
            meio = max(300, tela.winfo_width()) / 2
            self.desenhar_icone(tela, chave, centro=(meio, 75), caixa=(240, 115), espessura=2)
            exemplo = {**dados, "tipo": chave, "x": meio, "y": 75}
            escala = min(240 / dados["w"], 115 / dados["h"])
            exemplo["w"], exemplo["h"] = dados["w"] * escala, dados["h"] * escala
            tx, ty = self.centro_texto(exemplo)
            tela.create_text(tx, ty, text=dados["texto"], width=self.largura_texto(exemplo),
                             justify="center", font=self.fonte(12), fill="#1a1a1a")
        elif chave == "atalhos":
            self.lbl_topico.config(text="Atalhos do teclado")
            self.lbl_resumo.config(text="Tudo o que dá para fazer sem tirar a mão do teclado.")
            conteudo = ATALHOS
        else:
            self.lbl_topico.config(text=chave)
            self.lbl_resumo.config(text="Guia do Fluxograma")
            conteudo = MANUAL_GERAL[chave]

        caixa = self.texto_manual
        caixa.config(state="normal")
        caixa.delete("1.0", "end")
        for linha in conteudo.split("\n"):
            letras = [c for c in linha if c.isalpha()]
            if chave == "atalhos":
                marca = "titulo" if letras and linha == linha.upper() and not linha.startswith(" ") else "mono"
            else:
                marca = "titulo" if len(letras) > 3 and linha == linha.upper() else ""
            caixa.insert("end", linha + "\n", marca)
        caixa.config(state="disabled")
        caixa.yview_moveto(0)

    def mostrar_atalhos(self):
        janela = tk.Toplevel(self.janela)
        janela.title("Atalhos")
        janela.configure(bg=COR_PAINEL)
        janela.resizable(False, False)
        janela.transient(self.janela)
        tk.Label(janela, text=ATALHOS, bg=COR_PAINEL, fg=COR_TEXTO, font=self.fonte_status,
                 justify="left").pack(padx=20, pady=(16, 8))
        self.botao(janela, "Fechar", janela.destroy).pack(pady=(0, 14), ipadx=20)
        janela.bind("<Escape>", lambda e: janela.destroy())
        janela.focus_set()

    def mostrar_sobre(self):
        messagebox.showinfo("Sobre", "Fluxograma\nProjeto 019 da Meta 100 — Saga MundoPessoal\n\n"
                                     "Desenhe fluxogramas com formas, setas e rótulos,\n"
                                     "salve em JSON e exporte como imagem PNG.")

    def carregar_exemplo(self):
        if not self.confirmar_descartar():
            return
        formas = [
            (1, "terminal", "Início", 400, 80),
            (2, "processo", "Ferver a água", 400, 200),
            (3, "decisao", "Tem pó de café?", 400, 340),
            (4, "entrada_saida", "Comprar pó de café", 660, 340),
            (5, "processo", "Passar o café", 400, 480),
            (6, "subrotina", "Adoçar a gosto", 400, 600),
            (7, "terminal", "Fim", 400, 720),
        ]
        setas = [(8, 1, 2, ""), (9, 2, 3, ""), (10, 3, 5, "Sim"), (11, 3, 4, "Não"),
                 (12, 4, 5, ""), (13, 5, 6, ""), (14, 6, 7, "")]
        dados = {
            "formas": [{"id": i, "tipo": t, "texto": texto, "cor": TIPOS[t]["cor"], "x": x, "y": y,
                        "w": TIPOS[t]["w"], "h": TIPOS[t]["h"]} for i, t, texto, x, y in formas],
            "setas": [{"id": i, "origem": a, "destino": b, "rotulo": r} for i, a, b, r in setas],
            "proximo_id": 15,
        }
        self.comecar_do_zero(dados)
        self.mostrar_aviso("Exemplo carregado: Fazer café ☕")

    def sair(self):
        if self.confirmar_descartar():
            self.janela.destroy()


if __name__ == "__main__":
    janela = tk.Tk()
    app = Fluxograma(janela)
    janela.mainloop()
