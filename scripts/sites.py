"""Lê a página pública de cada empresa e aponta sinais de maturidade comercial.

Detecta, pelo código público da home (sem login):
- ferramentas de vendas, marketing e atendimento instaladas no site;
- se tem página de carreira (está contratando de forma estruturada);
- se tem chamada comercial ("fale com um consultor", "agende uma demonstração").

Uso:
  python scripts/sites.py empresa.com.br outra.com

Saída: JSON por site. O que não for detectado fica vazio (não quer dizer que não usa).
"""
from __future__ import annotations

import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from comum import baixar, dominio, imprimir_json, saida_utf8  # noqa: E402

saida_utf8()

# Assinaturas públicas (trechos de script ou domínio) -> nome e categoria.
ASSINATURAS = [
    (r"d335luupugsy2\.cloudfront|rdstation(-static)?\.com\.br/|rdstation\.com/.*\.js|rd-station", "RD Station", "marketing"),
    (r"js\.hs-scripts\.com|js\.hsforms\.net|hs-analytics\.net|js\.hubspot\.com|hs-banner\.com", "HubSpot", "CRM e marketing"),
    (r"leadbooster-chat\.pipedrive|webforms\.pipedrive|pipedriveassets", "Pipedrive", "CRM"),
    (r"pi\.pardot\.com|pardot\.com/pd\.js|salesforceliveagent|force\.com/embeddedservice|embeddedservice/.*esw", "Salesforce", "CRM"),
    (r"ploomes\.com/.*(form|widget|\.js)", "Ploomes", "CRM"),
    (r"agendor\.com\.br/.*(form|widget|\.js)", "Agendor", "CRM"),
    (r"meetime\.com\.br/.*\.js", "Meetime", "vendas"),
    (r"exactsales\.com\.br/.*\.js|exactspotter", "Exact Sales", "vendas"),
    (r"widget\.intercom\.io|js\.intercomcdn\.com", "Intercom", "atendimento"),
    (r"zendesk|zdassets", "Zendesk", "atendimento"),
    (r"octadesk", "Octadesk", "atendimento"),
    (r"blip\.ai|take\.net", "Blip", "atendimento"),
    (r"jivosite|jivochat", "JivoChat", "atendimento"),
    (r"tawk\.to", "Tawk.to", "atendimento"),
    (r"calendly", "Calendly", "agenda"),
    (r"snap\.licdn\.com|linkedin\.com/px", "LinkedIn Insight", "anúncios"),
    (r"connect\.facebook\.net|fbevents\.js", "Meta Pixel", "anúncios"),
    (r"googleadservices|gtag/js\?id=AW-", "Google Ads", "anúncios"),
    (r"googletagmanager\.com", "Google Tag Manager", "medição"),
    (r"hotjar", "Hotjar", "medição"),
    (r"wa\.me/|api\.whatsapp\.com", "WhatsApp no site", "atendimento"),
]
CARREIRA = r"carreiras|trabalhe[- ]conosco|vagas|careers|jobs|gupy\.io|solides|kenoby|greenhouse|lever\.co"
COMERCIAL = (r"fale com (um )?(consultor|especialista|vendas|comercial)|agende (uma )?(demo|demonstra)|"
             r"solicite (uma )?(proposta|demonstra|or[çc]amento)|falar com vendas|time comercial")


def analisar(site: str) -> dict:
    d = dominio(site)
    if not d:
        return {"site": site, "erro": "site inválido"}
    try:
        html = baixar(f"https://{d}", navegador=True, tentativas=2)
    except Exception as e:
        return {"site": d, "erro": f"não abriu ({e})"}
    baixo = html.lower()
    # Ferramentas: procura só dentro de scripts, iframes e links (não no texto visível),
    # pra não confundir "integra com o HubSpot" com "usa o HubSpot".
    codigo = " ".join(
        re.findall(r"<script[^>]*>.*?</script>|<(?:script|iframe|link|img)[^>]+(?:src|href)=[\"'][^\"']+", baixo, re.S)
    )
    achadas, cats = [], set()
    for padrao, nome, cat in ASSINATURAS:
        if re.search(padrao, codigo):
            achadas.append(nome)
            cats.add(cat)
    return {
        "site": d,
        "ferramentas": achadas,
        "categorias": sorted(cats),
        "tem_pagina_carreira": bool(re.search(CARREIRA, baixo)),
        "tem_chamada_comercial": bool(re.search(COMERCIAL, baixo)),
        "anuncia_pago": any(c == "anúncios" for c in cats),
    }


def main(args: list[str]) -> int:
    if not args:
        print(__doc__)
        return 1
    res = []
    for n, s in enumerate(args):
        if n:
            time.sleep(0.5)
        res.append(analisar(s))
    imprimir_json(res if len(res) > 1 else res[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
