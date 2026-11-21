# Instalação em 3 passos

Você precisa de 3 coisas: um computador (Windows ou Mac), o app do Claude Code com um plano pago do Claude (Pro ou Max) e poucos minutos.

## 1. Instale o Claude Code

Baixe em https://claude.com/claude-code, abra e entre com a sua conta do Claude.

## 2. Cole o bloco abaixo numa conversa nova do Claude Code

Copie o bloco inteiro e cole. O Claude baixa o kit, prepara o seu computador e faz a sua primeira lista.

```text
Você vai instalar o "Radar de Contas" pra mim neste computador. Eu NÃO sou técnico: faça tudo sozinho, nunca me peça pra rodar comando nem editar arquivo, e explique cada passo em português simples. Mantenha uma lista de tarefas visível e vá marcando o que já fez.

1) BAIXAR O KIT
   git clone https://github.com/johnny01010101/radar-de-contas.git   (na minha pasta Documentos)
   Sem git? Baixe o ZIP do mesmo endereço (/archive/refs/heads/main.zip) e descompacte.
   Depois, trabalhe sempre de dentro da pasta "radar-de-contas".

2) PREPARAR O COMPUTADOR (só o que faltar, tudo grátis)
   Rode scripts/ambiente.py (python3 no Mac; python ou py no Windows).
   Sem Python 3.9+? Instale você mesmo (Windows: winget install -e --id Python.Python.3.12;
   Mac: instalador de python.org). Rode de novo até aparecer PRONTO.

3) CONHECER O MEU NEGÓCIO (uma pergunta por vez)
   Leia o CLAUDE.md e comece pelo /comecar: me pergunte só o site da minha empresa.

4) PRIMEIRA LISTA
   Siga /sinais, /calibrar, /lista e /planilha até a planilha ficar pronta.
   Me mostre onde ela foi salva.

Tenha paciência comigo, suponha que eu nunca usei um terminal e use só este kit.
```

Se ele pedir permissão pra instalar algo ou acessar um site, clique em **Permitir**.

## 3. Da próxima vez

Abra o Claude Code na pasta `radar-de-contas` (em Documentos) e escreva: **"quero as contas novas da semana"**. Ele roda o `/atualizar` e não repete as contas que você já recebeu.

## Deu problema?

- **"Python não encontrado" no Windows:** feche e abra o Claude Code depois da instalação do Python, pra ele enxergar o comando novo.
- **Algum site não abriu:** o kit segue pela busca na web do Claude. Só fica um pouco mais lento.
- **A lista veio fora do alvo:** peça "vamos refazer a calibração".
