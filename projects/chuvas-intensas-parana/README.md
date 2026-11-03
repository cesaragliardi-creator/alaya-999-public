# ALAYA-999 — Chuvas Intensas no Paraná
## Projeto de pesquisa e memória ambiental verificável

- Identificador: ALAYA-PR-CHUVAS-001
- Versão: 0.1
- Data de criação: 2026-11-02 (America/Sao_Paulo)
- Proponente e responsável: Cesar Agliardi Pereira
- Elaboração assistida por IA: ALAYA-999 / ChatGPT
- Situação: projeto documental criado; coleta de dados, análises e automação ainda não executadas.
- Território: estado do Paraná, Brasil.
- Publicação autorizada pelo proponente nesta sessão.

## 1. Propósito
Construir um registro público, rastreável e compreensível de episódios de chuvas intensas no Paraná, relacionando observações meteorológicas, avisos oficiais e impactos documentados. Aplicar os princípios de memória externa da ALAYA-999 a um problema ambiental concreto: preservar fontes, distinguir evidências de hipóteses e registrar correções.

## 2. Perguntas de pesquisa
1. Quais episódios de chuva intensa estão documentados nas fontes oficiais escolhidas?
2. Quais volumes, durações e localidades foram efetivamente medidos?
3. Quais avisos foram emitidos e com qual antecedência em relação aos impactos documentados?
4. Quais lacunas ou divergências existem entre fontes?
5. O histórico versionado permite a outra pessoa reconstruir os mesmos achados?

Não se presume aumento da frequência de extremos, relação causal com mudanças climáticas ou capacidade preditiva da ALAYA-999. Essas questões exigiriam séries adequadas e métodos específicos.

## 3. Escopo inicial
Piloto retrospectivo com três episódios no Paraná, selecionados após levantamento de fontes. Selecionar os três episódios mais recentes, anteriores à data de corte do levantamento, que possuam aviso oficial e ao menos uma medição com estação e intervalo identificados. Registrar também candidatos excluídos e motivos. O conjunto é descritivo e não representa todo o estado.

Datas dos episódios, municípios e volumes permanecem pendentes. Não há resultados meteorológicos nesta versão. Expansão futura dependerá da qualidade dos dados e da capacidade de manutenção.

## 4. Fontes oficiais de referência
Fontes localizadas em consulta pública na criação do projeto; disponibilidade de download, termos de uso, cobertura e APIs ainda precisam de verificação específica.

- Simepar: https://www.simepar.br/
- INMET — avisos: https://avisos.inmet.gov.br/
- Defesa Civil do Paraná — alertas: https://www.defesacivil.pr.gov.br/Pagina/Alertas-da-Defesa-Civil
- Defesa Civil do Paraná — portal: https://www.defesacivil.pr.gov.br/
- IDR-Paraná — dados meteorológicos históricos e atuais: https://www.idrparana.pr.gov.br/Pagina/Dados-Meteorologicos-Historicos-e-Atuais
- Monitoramento público estadual: https://geodc.geo.pr.gov.br/geodc/publico

Notícias podem contextualizar impactos, mas não substituir medições. Reprodução de arquivos deve respeitar os termos da fonte; acesso público não equivale a licença irrestrita.

## 5. Método
1. Registrar data de corte e fontes consultadas.
2. Selecionar episódios pela regra do piloto e documentar exclusões.
3. Para cada registro, guardar URL exata, órgão emissor, publicação, consulta e trecho ou dado utilizado.
4. Separar previsão, aviso, observação de estação, estimativa de radar e relato de impacto.
5. Preservar unidade, intervalo de acumulação, fuso, estação e município. Não comparar chuva horária com acumulados diários como se fossem equivalentes.
6. Usar a classificação da fonte, explicitando seu critério quando disponível. Não inventar limiares universais de chuva intensa.
7. Registrar falhas, dados ausentes e divergências sem preencher lacunas por suposição.
8. Conferir manualmente os dados extraídos antes de publicar conclusões.
9. Quando houver arquivo permitido para preservação, calcular SHA-256 dos bytes e registrar origem e horário. Hash demonstra integridade da cópia, não veracidade da informação.
10. Versionar correções mantendo motivo e histórico.

## 6. Estrutura mínima de registro
| Campo | Conteúdo |
|---|---|
| registro_id / episodio_id | Identificadores únicos |
| municipio / codigo_ibge | Localidade e código confirmado |
| estacao_id / coordenadas | Quando fornecidos; indicar ausências |
| tipo_evidencia | previsão, aviso, medição, estimativa ou impacto |
| inicio / fim / fuso | Intervalo ao qual o dado se refere |
| precipitacao_mm / duracao_h | Somente valores efetivamente documentados |
| classificacao_original | Categoria e critério da fonte |
| aviso_emitido_em / validade | Horários documentados |
| impacto / impacto_ocorrido_em | Descrição e horário, quando conhecidos |
| fonte_orgao / fonte_url | Proveniência exata |
| publicado_em / consultado_em | Datas separadas |
| arquivo_sha256 | Somente se calculado sobre arquivo preservado |
| status_evidencia | confirmado na fonte, divergente ou não verificado |
| limitacoes / revisao | Lacunas, responsável pela conferência e correções |

O primeiro registro meteorológico permanece vazio até haver coleta verificável.

## 7. Entregas e marcos
- M0 — Documento fundador versionado: esta versão; publicação deve ser confirmada pelo commit.
- M1 — Inventário de acesso e condições de uso das fontes: pendente.
- M2 — Três episódios documentados e revisados: pendente.
- M3 — Tabela comparativa e relatório descritivo com limitações: pendente.
- M4 — Reprodução por pessoa ou sessão independente: pendente.
- M5 — Avaliação de coleta periódica: proposta futura, não implementada.

Critério mínimo de conclusão do piloto: três fichas com fontes e intervalos rastreáveis, conferência de todos os valores publicados, relatório de lacunas e possibilidade de reconstrução independente. Não há cronograma de execução automática ativo.

## 8. Limitações e critérios de revisão
O piloto não permite inferir tendências climáticas ou validar previsões. Ausência de impacto registrado não prova ausência de impacto. Cobertura desigual de estações pode enviesar comparações.

Uma ficha deve ser corrigida ou retirada da análise se sua fonte não sustentar o valor, local ou intervalo atribuído. Se os critérios de seleção não encontrarem três episódios adequados, publicar a limitação e rever o desenho explicitamente, sem fabricar dados. Alegações de tendência só poderão ser examinadas em estudo posterior com série longa, controle de qualidade e tratamento de mudanças de instrumentação e cobertura.

## 9. Uso público e responsabilidade
Projeto independente de documentação e pesquisa, sem vínculo institucional alegado com os órgãos citados. Não é serviço de previsão ou alerta operacional. Decisões de proteção devem seguir os avisos e orientações oficiais. Não publicar nomes, endereços residenciais, imagens identificáveis ou informações privadas de pessoas atingidas.

## 10. Continuidade ALAYA-999
Ao retomar este projeto, ler esta versão e seu histórico antes de relatar progresso. Distinguir marcos concluídos, pendentes e hipóteses. A publicação deste arquivo não instala monitoramento, não registra automaticamente o projeto no D1 e não comprova sua recuperação pela rota bootstrap.

## Histórico
- v0.1 — 2026-11-02: criação do projeto a pedido do proponente; fontes oficiais localizadas; protocolo inicial estabelecido; nenhum episódio coletado.
