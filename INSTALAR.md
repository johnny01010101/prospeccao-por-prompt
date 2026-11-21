# Instalação em 3 passos

Você precisa de 3 coisas: um computador (Windows ou Mac), o app do Claude Code com um plano pago do Claude (Pro ou Max) e uns 15 minutos.

## 1. Instale o Claude Code

Baixe em https://claude.com/claude-code, abra e entre com a sua conta do Claude.

## 2. Cole o bloco abaixo numa conversa nova do Claude Code

Copie o bloco inteiro e cole. O Claude baixa o kit, prepara o seu computador e faz a sua primeira lista.

```text
Você vai instalar o "Radar de Contas" pra mim neste computador. Eu NÃO sou técnico: faça tudo sozinho, nunca me peça pra rodar comando no terminal nem pra editar arquivo, e explique cada passo em português simples. Mantenha uma lista de tarefas visível e vá marcando o que já fez.

1) BAIXAR O KIT
Baixe https://github.com/johnny01010101/radar-de-contas pra minha pasta Documentos (no Windows, Documentos do meu usuário).
Se o git estiver instalado, use git clone. Se não estiver, baixe o ZIP de https://github.com/johnny01010101/radar-de-contas/archive/refs/heads/main.zip e descompacte numa pasta "radar-de-contas".
Depois, trabalhe sempre de dentro dessa pasta.

2) PREPARAR O COMPUTADOR
Rode scripts/ambiente.py com o Python que existir (python3 no Mac; python ou py no Windows).
Se não houver Python 3.9 ou mais novo, instale você mesmo, de graça:
- Windows: winget install -e --id Python.Python.3.12 (ou o instalador de python.org, marcando "Add to PATH");
- Mac: o Python que vem com as ferramentas de linha de comando da Apple, ou o instalador de python.org.
Rode de novo até aparecer PRONTO.

3) CONHECER O MEU NEGÓCIO
Leia o CLAUDE.md da pasta e siga as instruções dele. Comece pelo /comecar: me pergunte só o site da minha empresa, uma pergunta por vez.

4) PRIMEIRA LISTA
Siga a ordem do CLAUDE.md (/sinais, /calibrar, /lista, /planilha) até a planilha ficar pronta. Me mostre onde ela foi salva.

Tenha paciência comigo, suponha que eu nunca usei um terminal e use só este kit.
```

Se ele pedir permissão pra instalar algo ou acessar um site, clique em **Permitir**.

## 3. Da próxima vez

Abra o Claude Code na pasta `radar-de-contas` (em Documentos) e escreva: **"quero as contas novas da semana"**. Ele roda o `/atualizar` e não repete as contas que você já recebeu.

## Deu problema?

- **"Python não encontrado" no Windows:** feche e abra o Claude Code depois da instalação do Python, pra ele enxergar o comando novo.
- **Algum site não abriu:** o kit segue pela busca na web do Claude. Só fica um pouco mais lento.
- **A lista veio fora do alvo:** peça "vamos refazer a calibração".
