// Área de documentos com senha (/documentos/). O resto do site é servido direto dos assets.
// Senha: secret DOCS_SENHA (npx wrangler secret put DOCS_SENHA). Arquivos enviados: R2 (binding DOCS).
// Qualquer usuário serve no login; só a senha é conferida.

const MAX_BYTES = 20 * 1024 * 1024;
const TIPOS = { pdf: 'application/pdf', doc: 'application/msword', docx: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', jpg: 'image/jpeg', jpeg: 'image/jpeg', png: 'image/png' };
// Documentos oficiais (públicos, no repositório em arquivos/; também têm botão na página /staff/).
const FIXOS = [
  ['Credencial de filiação comercial e termo de autorizações', 'arquivos/credencial-filiacao.pdf'],
];

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (!url.pathname.startsWith('/documentos')) return env.ASSETS.fetch(req);
    if (!(await autorizado(req, env))) {
      return new Response('Senha necessária.', { status: 401, headers: { 'WWW-Authenticate': 'Basic realm="Documentos Anne Models", charset="UTF-8"', 'Cache-Control': 'no-store' } });
    }
    const p = url.pathname;
    if (p === '/documentos' || p === '/documentos/') return pagina(env, url.searchParams.get('ok'));
    if (p === '/documentos/enviar' && req.method === 'POST') return enviar(req, env);
    if (p.startsWith('/documentos/enviados/')) return baixar(env, decodeURIComponent(p.slice('/documentos/enviados/'.length)));
    return new Response('Não encontrado.', { status: 404 });
  },
};

async function autorizado(req, env) {
  const senha = env.DOCS_SENHA;
  if (!senha) return false; // sem senha configurada, fecha
  const h = req.headers.get('Authorization') || '';
  if (!h.startsWith('Basic ')) return false;
  let dado;
  try { dado = new TextDecoder().decode(Uint8Array.from(atob(h.slice(6)), c => c.charCodeAt(0))); } catch { return false; }
  const enviada = dado.slice(dado.indexOf(':') + 1);
  const [a, b] = await Promise.all([enviada, senha].map(s => crypto.subtle.digest('SHA-256', new TextEncoder().encode(s))));
  return crypto.subtle.timingSafeEqual(a, b);
}

function esc(s) {
  return String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

async function pagina(env, ok) {
  const lista = await env.DOCS.list({ include: ['customMetadata'] });
  const enviados = lista.objects
    .sort((a, b) => b.uploaded - a.uploaded)
    .map(o => {
      const m = o.customMetadata || {};
      const quando = new Date(o.uploaded).toLocaleString('pt-BR', { timeZone: 'America/Sao_Paulo' });
      return `<li><a href="/documentos/enviados/${encodeURIComponent(o.key)}">${esc(m.nome || o.key)}</a><span>${esc(quando)}${m.quem ? ' · ' + esc(m.quem) : ''}${m.obs ? ' · ' + esc(m.obs) : ''}</span></li>`;
    }).join('') || '<li><span>Nenhum arquivo enviado ainda.</span></li>';
  const fixos = FIXOS.map(([t, href]) => `<li><a href="/${href}" download>${esc(t)}</a><span>PDF para imprimir</span></li>`).join('');
  const aviso = ok ? '<p class="ok" role="status">Arquivo enviado. Ele já aparece na lista abaixo.</p>' : '';
  const html = `<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow"><title>Documentos · Anne Models Management</title><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<style>body{margin:0;background:#faf8f3;color:#2c2b28;font:17px/1.6 Jost,system-ui,sans-serif}main{width:min(880px,calc(100% - 40px));margin:0 auto;padding:56px 0 96px}h1{font:400 clamp(36px,5vw,56px)/1.05 'Bodoni Moda',Didot,serif;margin:0 0 8px}h2{font:400 28px/1.2 'Bodoni Moda',Didot,serif;margin:48px 0 12px}.sub{color:#4a4740;margin:0}.eyebrow{font:500 12px/1.4 Jost,sans-serif;letter-spacing:.22em;text-transform:uppercase;color:#80622a;margin:0 0 12px}ul{list-style:none;margin:0;padding:0;border-top:1px solid #3b3a37}li{display:flex;flex-wrap:wrap;justify-content:space-between;gap:4px 24px;padding:16px 0;border-bottom:1px solid #dcd8cf}li a{color:#2c2b28;font-weight:500}li span{color:#5e5a51;font-size:15px}form{display:grid;gap:14px;background:#fff;border:1px solid #e6decb;padding:24px}label{display:grid;gap:6px;font-size:15px;font-weight:500}input{font:inherit;padding:10px 12px;border:1px solid #c9bfa9;background:#fff}button{justify-self:start;min-height:48px;padding:12px 24px;border:0;background:#80622a;color:#fff;font:500 13px/1.2 Jost,sans-serif;letter-spacing:.14em;text-transform:uppercase;cursor:pointer}button:hover{background:#6a5022}.ok{background:#eef6ef;border-left:4px solid #1a7f45;padding:12px 16px}a:focus-visible,button:focus-visible,input:focus-visible{outline:2px solid #80622a;outline-offset:2px}</style></head>
<body><main><p class="eyebrow">Área restrita · equipe e assessoria jurídica</p><h1>Documentos da agência</h1><p class="sub">Baixe, revise e envie de volta a versão atualizada. Não compartilhe a senha.</p>${aviso}
<h2>Documentos oficiais</h2><ul>${fixos}</ul>
<h2>Arquivos enviados pela equipe</h2><ul>${enviados}</ul>
<h2>Enviar um arquivo</h2><form method="post" action="/documentos/enviar" enctype="multipart/form-data">
<label>Arquivo (PDF, Word, JPG ou PNG, até 20 MB)<input type="file" name="arquivo" required accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"></label>
<label>Seu nome<input type="text" name="quem" maxlength="80" required autocomplete="name"></label>
<label>Observação (opcional)<input type="text" name="obs" maxlength="200" placeholder="Ex.: contrato de filiado revisado para 2027"></label>
<button type="submit">Enviar arquivo</button></form></main></body></html>`;
  return new Response(html, { headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store', 'X-Robots-Tag': 'noindex' } });
}

async function enviar(req, env) {
  let form;
  try { form = await req.formData(); } catch { return erro('Não foi possível ler o envio.'); }
  const arq = form.get('arquivo');
  if (!arq || typeof arq === 'string' || !arq.size) return erro('Escolha um arquivo.');
  if (arq.size > MAX_BYTES) return erro('O arquivo passa de 20 MB.');
  const nome = String(arq.name || 'arquivo').replace(/[\\/\u0000-\u001f]/g, '_').slice(0, 120);
  const ext = (nome.split('.').pop() || '').toLowerCase();
  if (!TIPOS[ext]) return erro('Tipo de arquivo não aceito. Use PDF, Word, JPG ou PNG.');
  const quem = String(form.get('quem') || '').trim().slice(0, 80);
  if (!quem) return erro('Informe seu nome.');
  const obs = String(form.get('obs') || '').trim().slice(0, 200);
  const key = `${new Date().toISOString().replace(/[:.]/g, '-')}-${crypto.randomUUID().slice(0, 8)}.${ext}`;
  await env.DOCS.put(key, arq.stream(), { httpMetadata: { contentType: TIPOS[ext] }, customMetadata: { nome, quem, obs } });
  return Response.redirect(new URL('/documentos/?ok=1', req.url).toString(), 303);
}

async function baixar(env, key) {
  if (!/^[\w.-]+$/.test(key)) return new Response('Não encontrado.', { status: 404 });
  const o = await env.DOCS.get(key);
  if (!o) return new Response('Não encontrado.', { status: 404 });
  const nome = (o.customMetadata && o.customMetadata.nome) || key;
  return new Response(o.body, { headers: {
    'Content-Type': (o.httpMetadata && o.httpMetadata.contentType) || 'application/octet-stream',
    'Content-Disposition': `attachment; filename*=UTF-8''${encodeURIComponent(nome)}`,
    'Cache-Control': 'private, no-store', 'X-Content-Type-Options': 'nosniff',
  } });
}

function erro(msg) {
  return new Response(`<!DOCTYPE html><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><p style="font:17px/1.6 system-ui;margin:40px">${esc(msg)} <a href="/documentos/">Voltar</a></p>`, { status: 400, headers: { 'Content-Type': 'text/html; charset=utf-8' } });
}
