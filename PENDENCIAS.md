# Anne Models: pendências

Protótipo com 16 páginas, gerado por `python gerar.py`. Textos, contatos e links ficam em `gerar.py` (CONFIG no topo) e em `assets/servicos.json`. Onde falta informação, o botão leva ao WhatsApp da agência com uma mensagem específica, sem link falso.

## Confirmar com a Anne
- **Nomes:** "Anne Mac Pherson" (site e artes) ou "Anny Mac" / "Anne McPherson"? O site usa "Método Anne Mac Pherson". A transcrição traz "Anny Mact First", que parece erro de transcrição.
- **Revista:** as artes dizem "Krystal" e o catálogo diz "Comunidade Cristal". O site usa os dois assim.
- **33 anos de experiência:** o site também diz que a agência foi fundada em 1995 (31 anos).
- **Preços do catálogo:** vêm das artes do catálogo do WhatsApp. O briefing recomenda tirá-los até ela confirmar que estão valendo.
- **Concursos:** o site mostra Top Model of the Year, Sósias do Brasil, ABC do Amanhã e Mulher Total (artes do WhatsApp). Saíram Top Fashion Star e Luxo no Lixo como concurso; Luxo no Lixo agora aparece como desfile do Fashion Trade.
- **Método:** o cartaz fala em 17 módulos, mas as artes mostram 11. O site lista os 11.

- **Tempo de carreira:** o site diz "33 anos" (4 vezes) e "1995" (4 vezes); o cartaz de Milão diz "há 30 anos".
- **WhatsApp principal:** o site usa (31) 97302-3077 como número da agência. No contrato de filiação, esse é o "Life Style" e o da Anne Models é (31) 99658-9729.
- **E-mail oficial:** há três (CEO, cursos e assessoria). Falta dizer qual vai no rodapé.
- **Portal:** "Life Style with Anne Mc", "Life Style com Anne Mc" e "Portal Lifestyle" aparecem para a mesma coisa.
- **Parceiro:** "Vadú Braga" (pedido do Erick) ou "Vadu Braga" (sites antigos); revista "Fashion Modus" ou "Fashion Models".
- **Revisão jurídica:** textos sobre idade mínima, RPMT, CCT, autorização de responsável, contratos e comissão não foram alterados e precisam de revisão de um advogado.
- **noindex:** todas as páginas estão fora dos buscadores. Tirar só quando ela aprovar o site.

## Apostila do Método (12/11/2026)
- Texto dos 11 módulos vem do PDF de 2018 (`3 Anny Prado - Curso de Modelo.pdf`), com erros de digitação óbvios corrigidos e sem o site/contato antigo. Quando ela mandar o Word atualizado, trocar `dados/apostila.json` e regerar o PDF (comando no `gerar.py`).
- Módulo 11 (Certificado) não tem texto no original: usei um parágrafo com o que já está na ficha.
- As capas dos módulos têm a marca d'água "Dola AI" no canto: pedir as artes sem marca ou refazer.
- Conteúdo sensível herdado do original (medidas "perfeitas", dietas, DRT/SIMREV, natação) precisa da revisão dela antes de vender o curso.

## Ela precisa enviar
- WhatsApp e e-mail da Jane Ribeiro (`wa_jane`).
- Contrato de agenciamento (`contrato_agenciamento`) e link da Comunidade Cristal para não agenciados (`comunidade_cristal`).
- Links do Google Forms de cada curso e links de pagamento.
- Carga horária, datas, formato e valores dos três cursos; programa do curso de Recepcionistas.
- Regulamento e calendário dos concursos e do Garota Fashion Models.
- Data, local e cotas do próximo Fashion Trade.
- Links dos fornecedores da Trade Sales e se há comissão de afiliado.
- Foto profissional dela, autorizada, e logo em SVG ou PNG transparente.
- Textos de privacidade e termos.

## Depende de sistema (não é site estático)
- Área do aluno com login, aulas, PDFs, tarefas e certificados: hoje é uma página explicando que o acesso está sendo preparado.
- Comentários no Portal Lifestyle: sem posts nem comentários até haver conteúdo e moderação.

## Fora do site
- Organização do notebook e dos e-mails pessoais (pedido nos áudios).
