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

  // Inscrição (modelo Ford), enviada pelo WhatsApp
  const form = $('formInsc');
  if (form) {
    const f = form.elements, resp = $('campoResp');
    const idade = () => { const d = new Date(f.nascimento.value); if (isNaN(d)) return null; const n = new Date(); let a = n.getFullYear() - d.getFullYear(); if (n < new Date(n.getFullYear(), d.getMonth(), d.getDate())) a--; return a; };
    f.nascimento.addEventListener('change', () => { const a = idade(), menor = a !== null && a < 16; resp.hidden = !menor; f.responsavel.required = menor; });
    const q = new URLSearchParams(location.search);
    if (q.has('tv') || /tv/i.test(q.get('utm_source') || '')) f.origem.value = 'Entrevista na TV';
    const pre = q.get('curso'); if (pre) f.curso.value = pre;
    const marcados = n => [...form.querySelectorAll('[name=' + n + ']:checked')].map(x => x.value).join(', ');
    form.addEventListener('submit', e => {
      e.preventDefault();
      const l = ['Olá! Quero fazer minha inscrição gratuita na Anne Models.'];
      const add = (r, v) => { if (v) l.push(r + ': ' + v); };
      add('Gênero', marcados('genero')); add('Nome', f.nome.value); add('E-mail', f.email.value);
      add('Nascimento', f.nascimento.value.split('-').reverse().join('/') + ' (' + idade() + ' anos)');
      add('Responsável', f.responsavel.value); add('Cidade', f.cidade.value + ' - ' + f.estado.value); add('Telefone', f.telefone.value);
      add('Instagram', f.instagram.value); add('TikTok', f.tiktok.value);
      add('Altura', f.altura.value && f.altura.value + ' cm'); add('Cintura', f.cintura.value && f.cintura.value + ' cm');
      add('Quadril', f.quadril.value && f.quadril.value + ' cm'); add('Busto/Tórax', f.busto.value && f.busto.value + ' cm');
      add('Sapato', f.sapato.value); add('Olhos', f.olhos.value); add('Cabelo', f.cabelo.value);
      add('Quero ser', marcados('interesse')); add('Formação de interesse', f.curso.value); add('Categoria', marcados('categoria'));
      add('Como conheci', f.origem.value);
      l.push('Vou enviar minhas 4 fotos nesta conversa: rosto, corpo inteiro, meio corpo e perfil.');
      window.open(WA + encodeURIComponent(l.join('\n')), '_blank', 'noopener');
    });
  }

  // Formulário "Envie sua mensagem", enviado pelo WhatsApp
  const fm = $('formMsg');
  if (fm) fm.addEventListener('submit', e => {
    e.preventDefault();
    const f = fm.elements;
    const l = ['Olá! Mensagem enviada pelo site da Anne Models.', 'Nome: ' + f.nome.value, 'Idade: ' + f.idade.value, 'Cidade: ' + f.cidade.value,
      'E-mail: ' + f.email.value, 'WhatsApp: ' + f.whats.value, 'O que mais gostei no site: ' + f.gostou.value, 'Interesse: ' + f.interesse.value];
    window.open(WA + encodeURIComponent(l.join('\n')), '_blank', 'noopener');
  });

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
      b.setAttribute('aria-pressed', on); b.textContent = on ? 'Selecionado' : 'Selecionar';
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
