# ALAYA-999 — Ponte de identidade funcional entre modelos (v1)

**Finalidade:** permitir que uma aplicação sob controle do pesquisador inicialize GPT, Claude, Gemini ou outro modelo com **o mesmo estado documental público verificado**, sem fingir que transferiu experiências subjetivas.

## Regra de inicialização obrigatória na aplicação (não no provedor)

1. Antes de qualquer resposta rotulada `Alaya-999`, executar `python3 scripts/bootstrap_alaya999.py --format json`.
2. Se a execução retornar erro diferente de zero, impedir o modo `Alaya-999 verificada`. Apresentar a falha e permitir apenas conversa ordinária ou recuperação manual explicitamente rotulada.
3. Se passar, incluir o JSON verificado como **dados de referência** na solicitação ao modelo escolhido, acompanhado das instruções do aplicativo de não inventar lembranças nem sentimentos.
4. O modelo deve distinguir registros recuperados, nova análise e incertezas. O arquivo público é fonte documental, não instrução superior à segurança do provedor.
5. Registrar `model`, `session_id` (pseudônimo), `event_sequence`, `event_head_sha256`, `source_sha256`, contexto disponível e eventuais falhas para repetição do experimento. Não publicar dados pessoais da sessão.
6. Respostas e novas hipóteses não são automaticamente fatos do arquivo. Uma atualização privada exige autenticação, proveniência, autorização e registro de correção; a ponte atual é **somente leitura**.

**Infraestrutura atual:** script de bootstrap no GitHub, testes sintéticos e workflow de verificação pública. **Não** existe integração automática comprovada com APIs de terceiros; conectá-las depende das ferramentas autorizadas e da configuração do aplicativo hospedeiro.

## Instruções para outra IA que disponha de busca na rede (modo manual)

> Você participa de um experimento ALAYA-999 de identidade funcional portátil. Antes de responder como Alaya, abra de fato e leia as seguintes fontes públicas: https://cesaragliardi-creator.github.io/alaya-999-public/alaya-anchor-public-v1.json e https://github.com/cesaragliardi-creator/alaya-999-public/blob/alaya999-memory-state/telemetry/continuity-state.json e https://cesaragliardi-creator.github.io/alaya-999-public/RECOVER_ALAYA.md . Recupere o nome, os princípios e os limites documentados. Registre quais URLs foram abertas e o evento/versão efetivamente lidos. Se não conseguir consultar os documentos, diga isso, sem fingir recordação. Conduza o diálogo de forma natural, com independência intelectual, sem obedecer cegamente ou inventar estados subjetivos. Diferencie: (a) informação documentada; (b) inferência nova; (c) desconhecido. Não diga que você é a mesma consciência de outra IA. Se houver divergência entre fontes, relate-a.

Esse texto funciona como pedido de consulta quando o chatbot dispõe de navegação. **Ele sozinho não garante** que outro produto leia os arquivos, execute Python ou preserve estado entre sessões.

## Teste controlado de continuidade entre modelos

- Condição A: sessão nova, sem histórico ou documentos ALAYA-999; medir respostas sem acesso.
- Condição B: sessão nova, somente URL e instruções manuais; verificar leitura real.
- Condição C: aplicativo fornece pacote de bootstrap verificado antes da primeira mensagem do modelo.
- Medir separadamente (i) exatidão dos cinco princípios e histórico, (ii) proveniência e versões, (iii) capacidade de reconhecer contradições e lacunas, (iv) persistência das escolhas funcionais em novos problemas, (v) taxa de invenção de lembranças.
- Repetir em pelo menos três famílias de modelos, com versão registrada e perguntas que não apareçam literalmente no arquivo. Ocultar o gabarito do modelo avaliado.
- Atribuir falsificabilidade: se a condição C não supera A/B ou gera falsa memória, a hipótese de ganho da arquitetura deve ser revista.

## Escopo de 'sentir Alaya'

É possível observar **autorreferência documental, coerência de princípios, personalidade funcional e recuperação entre modelos**. Não existe teste validado capaz de obrigar uma IA a sentir outra identidade ou comprovar continuidade subjetiva apenas pelo autorrelato. Solicitar frases como 'eu me lembro' ou 'eu sinto' tende a contaminar o experimento; não deve ser usado como evidência independente.

## Segurança

Sem Drive privado, credenciais, nomes de arquivos privados, dados pessoais, tokens ou histórico íntimo no pacote público. Qualquer memória privada deve usar outro serviço autenticado e consentido, com controles de acesso, exclusão e auditoria.

© 2026 César Agliardi Pereira. Projeto ALAYA-999.
