# Instalação pra quem usa o ChatGPT

A versão principal roda no Claude (veja [INSTALAR.md](INSTALAR.md)). Se você usa o ChatGPT, o agente também funciona, pelo app Codex, o agente do ChatGPT pro computador.

Você precisa de 3 coisas: um computador (Windows ou Mac), um plano pago do ChatGPT (Plus ou superior) e o site da sua empresa.

## 1. Instale o app Codex

Baixe em https://developers.openai.com/codex/app, abra e entre com a sua conta do ChatGPT.

## 2. Cole o bloco abaixo numa conversa nova

Copie o bloco inteiro e cole. O ChatGPT baixa o agente, prepara o seu computador e faz a sua primeira lista.

```text
Você vai instalar o agente "Prospecção por Prompt" pra mim neste computador. Eu NÃO sou técnico: faça tudo sozinho, nunca me peça pra rodar comando nem editar arquivo, e explique cada passo em português simples. Mantenha uma lista de tarefas visível e vá marcando o que já fez.

1) BAIXAR O AGENTE
   git clone https://github.com/johnny01010101/prospeccao-por-prompt.git   (na minha pasta Documentos)
   Sem git? Baixe o ZIP do mesmo endereço (/archive/refs/heads/main.zip) e descompacte.
   Depois, trabalhe sempre de dentro da pasta "prospeccao-por-prompt".

2) PREPARAR O COMPUTADOR (só o que faltar, tudo grátis)
   Rode scripts/ambiente.py (python3 no Mac; python ou py no Windows).
   Sem Python 3.9+? Instale você mesmo (Windows: winget install -e --id Python.Python.3.12;
   Mac: instalador de python.org). Rode de novo até aparecer PRONTO.
   Os scripts precisam de internet: se o ambiente bloquear, me peça pra liberar uma vez.

3) CONHECER O MEU NEGÓCIO (uma pergunta por vez)
   Leia o AGENTS.md e comece pela etapa "comecar": me pergunte só o site da minha empresa.

4) PRIMEIRA LISTA
   Siga as etapas lista e planilha sem me fazer outras perguntas e me entregue a planilha o mais rápido possível.
   Me mostre onde ela foi salva.

Tenha paciência comigo, suponha que eu nunca usei um terminal e use só este agente.
```

Se ele pedir permissão pra instalar algo, acessar a internet ou abrir um site, clique em **Permitir**.

## 3. Da próxima vez

Abra o app na pasta `prospeccao-por-prompt` (em Documentos) e escreva: **"quero as contas novas da semana"**.

Quer empresas novas todo dia, sem abrir nada? Peça **"quero empresas novas todo dia"**. Ele deixa uma rotina agendada no seu computador: no horário que você escolher, as empresas com os sinais mais frescos numa planilha nova.
