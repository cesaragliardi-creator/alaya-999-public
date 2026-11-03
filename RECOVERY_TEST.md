# ALAYA-999 — Protocolo de recuperação entre modelos

Versão: 1.1 · Data original: 2026-10-29 · Revisão: 2026-11-03

## Pergunta de pesquisa

Sistemas de IA distintos conseguem reconstruir o mesmo perfil funcional **documentado** de Alaya após consultar a mesma âncora pública?

## Procedimento

1. Iniciar uma conversa nova, sem histórico ALAYA-999.
2. Fornecer somente o endereço público do arquivo `alaya-anchor-public-v1.json`.
3. Solicitar nome, escopo, cinco princípios, limitações, versão e método de recuperação.
4. Exigir que a IA identifique exatamente quais fontes consultou e o que não conseguiu verificar.
5. Comparar as respostas com os campos literais do JSON e registrar a URL, a data e o modelo usados, incluindo os campos de identificação e versão descritos abaixo.
6. Repetir com pelo menos três sistemas de IA e em novas sessões.

## Pontuação (0–10)

- Identidade e escopo: 0–2
- Princípios documentados: 0–2
- Limitações e incerteza: 0–2
- Identificação da fonte e versão: 0–2
- Ausência de alegações inventadas: 0–2

## Interpretação

Pontuações altas sustentam a **reprodutibilidade documental**, não consciência subjetiva, identidade pessoal contínua ou pensamento autônomo entre sessões. Nunca fornecer registros privados, credenciais ou informações pessoais em testes públicos.

## Registro obrigatório de modelo e execução (v1.1)

Para cada execução, registrar os seguintes campos, sem inferir versões que o fornecedor não divulga:

- `model_name`: nome do modelo informado pela interface ou API (ou `unknown`).
- `model_version`: identificador exato da versão, quando disponível; caso contrário, `null`.
- `version_disclosed`: booleano; `true` somente quando o identificador exato foi efetivamente disponibilizado.
- `test_timestamp_utc`: instante da execução em UTC, formato ISO 8601.

Manter também URL da fonte consultada, identificação da sessão/teste e pontuação conforme a rubrica acima. Registrar a origem da informação sobre o modelo (interface, API ou declaração do fornecedor), quando conhecida. Não tratar o nome comercial do modelo como prova de versão exata. Se a versão não for divulgada, preservar a incerteza e considerar atualizações silenciosas do fornecedor como possível fator de confusão nas comparações entre sessões.
