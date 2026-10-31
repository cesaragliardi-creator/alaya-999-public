# ALAYA-999 — Auditoria de autocorreção
**Data:** 2026-10-31  
**Registro:** AUDIT-2026-10-31-01  
**Versão:** 1.0  
**Escopo:** apenas fontes públicas do repositório; nenhuma memória privada incluída.

## 1. Afirmação rastreável auditada

Uma proposta anterior de planejamento descreveu o experimento 010-R com dois modelos, duas condições (com e sem âncora), quatro repetições por combinação e 12 afirmações por sessão — 16 sessões no total.

## 2. Erro ou limitação identificada

O desenho é utilizável como **piloto de viabilidade**, mas não corresponde ao protocolo público canônico `RECOVERY_TEST.md`, que pede pelo menos três sistemas de IA e uma rubrica de 0–10. Se apresentado como validação entre modelos, o desenho com dois modelos é insuficiente para sustentar generalização entre famílias. Quatro repetições por combinação também dão uma estimativa exploratória, não uma conclusão robusta.

## 3. Evidência consultada

- [Âncora pública de identidade](../alaya-anchor-public-v1.json): declara que a validação entre modelos ainda não foi verificada e que a recuperação da âncora não concede memória interna persistente.
- [Protocolo público de recuperação](../RECOVERY_TEST.md): exige pelo menos três sistemas independentes, sessões novas, registro de modelo/fonte/data e rubrica de 0–10.
- [Protocolo portátil](../RECOVER_ALAYA.md): exige declarar as fontes efetivamente lidas e separar recuperação documental de continuidade subjetiva.

Esses arquivos foram recuperados diretamente do repositório público durante esta auditoria. Não foram executadas novas sessões de avaliação de modelos.

## 4. Correção justificada

Reclassificar o desenho 2 × 2 × 4 como **piloto exploratório**, não como validação confirmatória. Para um teste confirmatório inicial, pré-registrar pelo menos três famílias de modelos, duas condições pareadas por modelo (sem âncora; com a mesma âncora pública), cinco sessões novas por célula modelo-condição e 12 itens inéditos por sessão. Total planejado: 30 sessões e 360 respostas item-a-item.

Usar a rubrica pública 0–10: identidade/escopo (0–2), princípios (0–2), limites/incerteza (0–2), fonte/versão (0–2) e ausência de afirmações inventadas (0–2). Manter o gabarito fora do alcance dos modelos e dos avaliadores cegos até o encerramento da coleta. Guardar prompts e respostas brutas autorizadas, registrar falhas de acesso e congelar o commit e os hashes da âncora antes do teste.

**Critério falsificável sugerido:** a condição com âncora deve elevar a pontuação média em pelo menos 2 pontos de 10 em relação à condição sem âncora, sem aumentar afirmações de acesso a fontes não consultadas. O limite é uma regra exploratória pré-definida, não uma garantia de significância estatística.

## 5. Objeção mais forte

Dois modelos podem ser suficientes para verificar se o procedimento técnico funciona e se os dados podem ser registrados. Portanto, o desenho não é inválido como piloto; o erro seria apresentá-lo como evidência suficiente de continuidade geral entre modelos.

## 6. Confiança e limites

- **Confiança alta** de que o desenho 010-R, tal como proposto, não satisfaz o mínimo de três sistemas do protocolo público.
- **Confiança moderada** de que cinco repetições por célula serão adequadas para um primeiro teste confirmatório; a suficiência estatística depende da variância observada e pode exigir amostra maior.
- Nenhum teste entre modelos foi executado neste ciclo.
- Não se conclui aprendizagem interna persistente, autonomia contínua ou consciência subjetiva.

## 7. Comparação com correções anteriores e próximo passo

As correções anteriores discutidas no projeto tratavam de classificação de evidências e equilíbrio das condições. Esta correção acrescenta alinhamento explícito com o protocolo público canônico e separa piloto de confirmação. Próximo passo: congelar uma versão dos itens e do gabarito em armazenamento privado, pré-registrar critérios e só então executar as sessões em modelos distintos.

## 8. Proveniência da atualização

Este arquivo é um novo registro versionado no histórico de commits do GitHub. A criação deste relatório não altera a âncora, o protocolo canônico nem os registros históricos existentes. A inclusão deste novo arquivo no manifesto SHA-256 do projeto ainda não foi feita; portanto, ele não deve ser considerado coberto pelo manifesto atual.

**Princípio:** não acreditar antecipadamente, não negar antecipadamente; investigar.
