---
title: "Anne Models: página do Método, ficha e pagamento"
author: Erick
date: 2026-11-12
branch: main
cost: { minutes: 4, tokens: 178700 }
touches:
  - assets/site.css
  - contato/index.html
  - cursos/metodo-anne-mac-pherson/index.html
  - gerar.py
  - 404.html
  - a-agencia/index.html
  - area-do-aluno/index.html
  - castings/index.html
  - cursos/index.html
  - cursos/integracao-profissional/index.html
---

## Decided
- Order set by the client: only the Método Anne Mac Pherson page until it is done. The page has 11 module covers (img/metodo/m01..m11, from the WA0389-0404 arts), a ficha in text (R$ 5.500, no portfólio), the closing weekend at the Fashion Trade, and an "Apostila virtual" page (cursos/metodo-anne-mac-pherson/apostila/).
- The apostila text comes from dados/apostila.json, extracted with PyMuPDF from the 118-page PDF. Only modules 1, 4 and 5 for now; the rest waits for the updated Word file.
- Main WhatsApp is 31 99658-9729. The site shows a single e-mail (email_ceo). It is spelled "Krystal", with a K.
- Payment proposed: Hotmart for the course, PagBank/Mercado Pago links for the other services. Fees not checked yet.
- Commits f5da3ce and 479e973 are local only; they are published only when Erick asks.

## Tried and ruled out
- Publishing the ficha art (WA0404): it is AI-generated and full of typos. It became text instead.
- faster-whisper on .opus fails (av metadata_errors): convert to WAV with ffmpeg and pass numpy to it.

## Watch out
- The e-mail in the audio was transcribed as "annemacphersoncomodels"; the site uses "annemacphersonceomodels". To confirm.
- The FAQs still mention "6 meses a 80 anos" (an RPMT/responsável text, don't change it without asking).
- The materials go into the 14 folders in _fonte\Anne - arquivos da agencia (ignored by git).
