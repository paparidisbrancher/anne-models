(() => {
  const WA = 'https://wa.me/' + document.body.dataset.wa + '?text=';
  const $ = id => document.getElementById(id);

  // Cabeçalho sólido depois da abertura (páginas sem foto já começam sólidas)
  const bar = $('topo');
  const hero = document.querySelector('.hero');
  const onScroll = () => bar.classList.toggle('solid', !hero || scrollY > innerHeight * 0.75);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // Menu do celular
  const mb = $('menuBtn'), nav = $('menuNav');
  if (mb) {
    const set = open => { mb.setAttribute('aria-expanded', open); nav.classList.toggle('open', open); document.body.classList.toggle('menu-open', open); };
    mb.addEventListener('click', () => set(mb.getAttribute('aria-expanded') !== 'true'));
    nav.addEventListener('click', e => { if (e.target.closest('a')) set(false); });
    addEventListener('keydown', e => { if (e.key === 'Escape') set(false); });
  }

  // Entrada suave
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('on'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -10% 0px' });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));

  // Cadastro em 3 passos, enviado pelo WhatsApp
  const form = $('formInsc');
  if (form) {
    const steps = [...form.querySelectorAll('.step')];
    const marks = [...form.querySelectorAll('.steps-nav [data-s]')];
    const bV = $('btnVoltar'), bS = $('btnSeguir'), bE = $('btnEnviar');
    let cur = 0;
    const show = i => {
      i = Math.max(0, Math.min(steps.length - 1, i)); cur = i;
      steps.forEach((s, k) => s.classList.toggle('on', k === i));
      marks.forEach((m, k) => m.classList.toggle('on', k <= i));
      bV.hidden = i === 0; bS.hidden = i === steps.length - 1; bE.hidden = i !== steps.length - 1;
    };
    const ok = i => { for (const el of steps[i].querySelectorAll('input,select')) { if (!el.checkValidity()) { el.reportValidity(); return false; } } return true; };
    const toForm = () => scrollTo({ top: form.getBoundingClientRect().top + scrollY - 96, behavior: 'smooth' });
    bS.addEventListener('click', () => { if (ok(cur)) { show(cur + 1); toForm(); } });
    bV.addEventListener('click', () => { show(cur - 1); toForm(); });
    const idade = form.elements.idade, resp = $('campoResp');
    idade.addEventListener('input', () => { const menor = idade.value !== '' && +idade.value < 16; resp.hidden = !menor; form.elements.responsavel.required = menor; });
    const q = new URLSearchParams(location.search);
    if (q.has('tv') || /tv/i.test(q.get('utm_source') || '')) { const r = form.querySelector('[name=origem][value="Entrevista na TV"]'); if (r) r.checked = true; }
    const pre = q.get('curso'); if (pre && form.elements.curso) form.elements.curso.value = pre;
    form.addEventListener('submit', e => {
      e.preventDefault();
      for (let i = 0; i < steps.length; i++) { show(i); if (!ok(i)) return; }
      const f = form.elements;
      const quero = [...form.querySelectorAll('[name=interesse]:checked')].map(x => x.value).join(', ') || 'não informado';
      const l = ['Olá! Quero fazer meu cadastro gratuito na Anne Models.', 'Nome: ' + f.nome.value, 'Idade: ' + f.idade.value, 'Cidade: ' + f.cidade.value];
      if (f.responsavel.value) l.push('Responsável: ' + f.responsavel.value);
      l.push('Quero ser: ' + quero, 'Curso de interesse: ' + f.curso.value, 'Concurso: ' + f.concurso.value);
      if (f.altura.value) l.push('Altura: ' + f.altura.value + ' cm');
      if (f.redes.value) l.push('Redes: ' + f.redes.value);
      l.push('Como conheci: ' + (form.querySelector('[name=origem]:checked') || {}).value, 'Vou enviar minhas 4 fotos nesta conversa.');
      window.open(WA + encodeURIComponent(l.join('\n')), '_blank', 'noopener');
    });
    show(0);
  }

  // Seleção de talentos para contratantes
  const sb = $('selbar');
  if (sb) {
    const sel = new Set(), cnt = $('selCount'), list = $('selList'), send = $('selSend'), cta = $('ctaTalentos');
    const upd = () => {
      const a = [...sel];
      const href = WA + encodeURIComponent('Olá! Gostaria de solicitar talentos da Anne Models.' + (a.length ? '\nSeleção: ' + a.join(', ') + '.' : ''));
      send.href = href; cta.href = href;
      cta.textContent = a.length ? 'Solicitar talentos (' + a.length + ')' : 'Solicitar talentos';
      cnt.textContent = a.length; list.textContent = a.join(', '); sb.hidden = !a.length;
    };
    document.querySelectorAll('.pick').forEach(b => b.addEventListener('click', () => {
      const v = b.dataset.pick, on = !sel.has(v);
      on ? sel.add(v) : sel.delete(v);
      b.setAttribute('aria-pressed', on); b.textContent = on ? '✓ Selecionado' : '+ Selecionar';
      upd();
    }));
  }

  // Catálogo de serviços: filtros e detalhes
  const dataEl = $('catData');
  if (dataEl) {
    const catData = JSON.parse(dataEl.textContent);
    const fbtns = document.querySelectorAll('.cat-filtros button'), ccards = document.querySelectorAll('.cat-card');
    fbtns.forEach(b => b.addEventListener('click', () => {
      fbtns.forEach(x => x.setAttribute('aria-pressed', x === b));
      ccards.forEach(c => { c.hidden = !(b.dataset.f === 'todos' || c.dataset.cat === b.dataset.f); });
    }));
    const dlg = $('catDlg'), big = $('catBig');
    if (dlg) {
      const open = key => {
        const it = catData[key]; if (!it) return;
        const cover = document.querySelector('[data-open="' + key + '"].cv');
        big.className = 'cv cat-big ' + (cover.classList.contains('cv-light') ? 'cv-light' : 'cv-dark');
        big.innerHTML = cover.innerHTML;
        $('catDlgTag').textContent = it.tag;
        $('catDlgTitle').textContent = it.t;
        $('catDlgPrice').textContent = it.p;
        $('catDlgList').replaceChildren(...it.d.map(x => Object.assign(document.createElement('li'), { textContent: x })));
        $('catDlgCta').href = 'https://wa.me/' + (dataEl.dataset.wa || document.body.dataset.wa) + '?text=' + encodeURIComponent('Olá! Tenho interesse no serviço "' + it.t + '" da Anne Models.');
        $('catDlgArt').href = dataEl.dataset.base + it.img[0];
        dlg.showModal ? dlg.showModal() : dlg.setAttribute('open', '');
        history.replaceState(null, '', '#' + key);
      };
      document.querySelectorAll('[data-open]').forEach(b => b.addEventListener('click', () => open(b.dataset.open)));
      dlg.querySelector('.cat-close').addEventListener('click', () => dlg.close());
      dlg.addEventListener('click', e => { if (e.target === dlg) dlg.close(); });
      dlg.addEventListener('close', () => history.replaceState(null, '', location.pathname + location.search));
      if (location.hash.slice(1) in catData) open(location.hash.slice(1));
    }
  }
})();
