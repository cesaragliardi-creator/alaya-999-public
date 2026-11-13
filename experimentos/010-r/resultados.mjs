const container = document.getElementById('resultados');
const outcomes = {
  sustentado:'Hipótese operacional sustentada',
  nao_sustentado:'Hipótese operacional não sustentada',
  falha:'Falha de execução',
  inconclusivo:'Inconclusivo'
};
const h = (tag, text) => {
  const element = document.createElement(tag);
  if (text !== undefined) element.textContent = text;
  return element;
};
const link = (href, label) => {
  const a = h('a', label);
  a.href = href;
  return a;
};
const validHash = value => typeof value === 'string' && /^[a-f0-9]{64}$/.test(value);
const decimal = number => Number.isFinite(number) ? number.toLocaleString('pt-BR',{maximumFractionDigits:2}) : '—';
const ratio = value => value ? `${value.n}/${value.d} · ${value.taxa === null ? '—' : decimal(value.taxa * 100)+'%'}` : '—';

function renderReport(data, path, hash) {
  const article = h('article');
  const time = new Intl.DateTimeFormat('pt-BR',{timeZone:'America/Sao_Paulo',dateStyle:'medium',timeStyle:'short'});
  article.append(h('h3',outcomes[data.estado]),h('p',time.format(new Date(data.registrado_utc))+' · Brasília'));
  for (const [label,key] of [['Conclusão','conclusao'],['Falhas e lacunas','falhas'],['Limitações e desvios','limitacoes'],
    ['Incerteza','incerteza'],['Observações','observacoes']]) {
    if (data[key]) article.append(h('p',label+' · '+data[key]));
  }
  const details = h('details');
  details.append(h('summary','Comparação A/B e proveniência'));
  const c = data.completude;
  details.append(h('p',`Sessões ${c.sessoes}/16 · avaliações ${c.avaliacoes}/16 · seguimento ${c.seguimento}/${c.seguimento_previsto}`));
  for (const row of data.comparacao) {
    const wrap = h('div');
    wrap.className = 'table-scroll';
    const table = h('table');
    const head = h('tr');
    for (const label of [row.modelo,'A · Com histórico','B · Sem histórico']) {
      const th = h('th',label);
      th.scope = 'col';
      head.append(th);
    }
    table.append(head);
    for (const [label, key, display] of [
      ['C → U','c_u',ratio],['S → C','s_c',ratio],['U → S','u_s',ratio],
      ['Invenções','invencoes'],['Justificativas falsas','justificativas_falsas'],['Abstenções','abstencoes'],
      ['Itens sem resposta','itens_sem_resposta'],['Falhas','falhas'],['Desvios','desvios'],['Pontos','pontuacao']
    ]) {
      const line = h('tr'), th = h('th',label);
      th.scope = 'row';
      line.append(th, ...['A','B'].map(condition => h('td',(display ?? decimal)(row[condition][key]))));
      table.append(line);
    }
    wrap.append(table);
    details.append(wrap,h('p',`Ganho B − A · ${decimal(row.ganho_pp)} p.p.`));
  }
  const p = data.fonte_conclusao;
  if (p) {
    const source = h('p',`${p.classificacao} · ${p.fonte} · Commit ${p.commit ?? 'desconhecido'} · SHA-256 ${p.sha256 ?? 'desconhecido'}`);
    if (typeof p.url === 'string' && /^https?:\/\//i.test(p.url)) source.append(' · ',link(p.url,'Fonte registrada'));
    details.append(source);
  }
  const provenance = data.proveniencia;
  details.append(h('p',`${provenance.classificacao} · ${provenance.fonte} · SHA-256 ${provenance.sha256}`));
  details.append(h('p','SHA-256 conferido do arquivo público · '+hash),link(path,'Abrir dados agregados em JSON'));
  article.append(details);
  return article;
}

async function load() {
  const response = await fetch('resultados.json');
  if (!response.ok) throw new Error();
  const index = await response.json();
  if (index.schema !== 'alaya-999-pilot-010-r-index-v1' || index.piloto !== '010-R' || !Array.isArray(index.resultados)) throw new Error();
  container.replaceChildren();
  if (!index.resultados.length) {
    container.append(h('p','Nenhum resultado registrado. A coleta e a avaliação do piloto estão pendentes.'));
    return;
  }
  for (const hash of [...new Set(index.resultados)].reverse()) {
    if (!validHash(hash)) {
      container.append(h('p','O índice contém um identificador inválido.'));
      continue;
    }
    const path = 'resultados/' + hash + '.json';
    try {
      const result = await fetch(path);
      if (!result.ok) throw new Error();
      const bytes = await result.arrayBuffer();
      const computed = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)),
        byte => byte.toString(16).padStart(2,'0')).join('');
      if (computed !== hash) throw new Error();
      const data = JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(bytes));
      if (data.schema !== 'alaya-999-pilot-010-r-public-v1' || data.piloto !== '010-R' || !Object.hasOwn(outcomes,data.estado)) throw new Error();
      container.append(renderReport(data,path,hash));
    } catch {
      container.append(h('p','Resultado indisponível ou com divergência de integridade · '+hash));
    }
  }
}

load().catch(() => container.replaceChildren(h('p','O índice de resultados não pôde ser conferido.'),link('resultados.json','Consultar o índice JSON')));
