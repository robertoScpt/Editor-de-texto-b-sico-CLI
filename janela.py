import tkinter as tk
from tkinter import messagebox
import argparse
import os
import json

#Caminho para o arquivo de configuração da janela, chamado config.json
cfg = os.path.join('config.json')

# Configurando o parser
parser = argparse.ArgumentParser(description="Um exemplo de captura de parâmetros.")
parser.add_argument("caminho", type=str, nargs='*', help="Caminho do arquivo")

# Parse dos argumentos
args = parser.parse_args()
c = ' '.join(args.caminho)


def foconat(event):
    text_area.focus_set()
def foconoi(event):
    inp.focus_set()

root = tk.Tk()
root.geometry('600x500')

# Criação da Textarea
text_area = tk.Text(root, wrap=tk.WORD)
text_area.pack(fill=tk.BOTH, expand=True)
text_area.focus_set()

#obter apenas o nome do arquivo
nome = os.path.basename(c)

#criacao da leitura do arquivo
def leitura(caminho):
    arquivo = open(c, 'r', encoding='utf-8')
    # Limpa o conteúdo atual da Text
    text_area.delete(1.0, tk.END)
    if os.path.isfile(caminho):
        # Lê o conteúdo do arquivo e insere na textarea
        conteudo = arquivo.read()
        root.title(nome)
        text_area.insert(tk.END, conteudo)
    else:
        messagebox.showinfo("Erro", f'{nome} não é um arquivo')

# Criação do Input
inp = tk.Entry(root)
inp.pack(fill=tk.BOTH)

#obitendo a configuração
arqA = open(cfg, 'r')
jsonabA = json.load(arqA)
arqA.close()
#obtendo todo o estilo
text_area['font'] = jsonabA['EstiloDaFonte'], jsonabA['TamanhoDFonte']
text_area['background'] = jsonabA['CorDeFundo']
text_area['foreground'] = jsonabA['CorDeTexto']
inp['background'] = jsonabA['CorDeFundo']
inp['foreground'] = jsonabA['CorDeTexto']
inp['insertbackground'] = jsonabA['CorDeTexto']
text_area['insertbackground'] = jsonabA['CorDeTexto']

#Comandos do input
def enter(event):
    valor = inp.get()
    match valor:
        case 'i':
            foconat(event)
        case 'w':
            salva()
        case 'wq':
            salva()
            root.after(500, fechar)
        case 'q':
            fechar()
        case _:
            messagebox.showinfo("Erro", f'Comando [{valor}] inválido')
    inp.delete(0, tk.END)
inp.bind('<Escape>', foconat)
text_area.bind('<Escape>', foconoi)
inp.bind('<Return>', enter)
#Funções de cada comando
#salvar
def salva():
    conteudo = text_area.get(1.0, tk.END)
    arquiv = open(c, 'w')
    arquiv.write(conteudo)
    arquiv.close()
    messagebox.showinfo("Salvo!", f'As alterações feitas no {nome}, foram salvas!')
def fechar():
    root.quit()

if c == '':
    root.title('Editor CLI')
else:
    if os.access(c, os.F_OK):
        leitura(c)
        root.title(os.path.basename(c))
        # Iniciar a aplicação
        root.mainloop()
    else:
        messagebox.showinfo("Erro", f'[{c}] não existe')
