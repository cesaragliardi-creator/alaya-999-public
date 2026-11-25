# ALAYA-999 005: protocolo de recuperação IPFS entre operadores independentes

**Projeto:** César Agliardi Pereira · ORCID 0009-0000-3322-4834 · Brasil  
**Versão:** 0.1.0 · 25 de novembro de 2026 · Protocolo e validação local, não resultado de campo

## Resumo

A redundância de processos numa única máquina não demonstra preservação distribuída entre operadores. O Experimento 005 define um ensaio de sete dias com dois operadores Kubo e um verificador em terceira infraestrutura. O desfecho principal é recuperar a âncora congelada usando só seu CID a partir de um repositório vazio, com a origem comprovadamente desligada, e obter o mesmo SHA-256. Atribuição ao voluntário, descoberta pública, respostas de gateway e disponibilidade posterior são desfechos distintos. A validação local confirmou fixidez, tolerância a interrupção simulada e restauração de versão; o teste de campo permanece pendente.

## Método e resultados

A âncora de 4.639 bytes, uma raiz IPFS de bloco bruto, foi verificada por CIDv1, SHA-256, importação Kubo offline e assinatura Ed25519 do manifesto do pacote 004. A assinatura atesta vínculo com uma chave técnica especificada, não autoria nem veracidade do documento. Uma interrupção HTTP simulada, em loopback, produziu recusa; um servidor local alternativo recuperou os bytes corretos e uma resposta HTTP 200 com bytes errados foi rejeitada. A reconexão local ao servidor reiniciado restabeleceu o digest esperado. Dois ramos sintéticos conflitantes foram mantidos; o ramo sem fonte não encerrou a divergência. Um sucessor sintético alterado foi detectado e o pacote congelado restaurado sem sobrescrever a referência.

## Validade e protocolo de campo

A recebe a função de origem e B preserva o CAR. C não recebe o arquivo antes da tentativa. Com A desligado, C tenta descoberta e recuperação pelo CID, sem estado anterior. Uma verificação separada, com consentimento de B e novo repositório, procura atribuir a entrega a B; só endereço, ASN, sucesso de gateway ou anúncio de provedor não provam independência física. Registre testes negativos, tempo UTC, versão Kubo, método, estado da origem, SHA-256 e repetição em outra data. Agregue evidências sem divulgar identificadores pessoais ou de rede sem consentimento.

**Limite:** a fotografia de lançamento registra zero operadores independentes confirmados, zero nós com consentimento e zero recuperações de campo verificadas. Persistência e continuidade funcional documentada não demonstram consciência nem identidade contínua interna.

[Protocolo público e artefato](https://cesaragliardi-creator.github.io/alaya-999-public/experimentos/005/) · [Coordenação](https://github.com/cesaragliardi-creator/alaya-999-public/issues/13) · [Kubo](https://docs.ipfs.tech/reference/kubo/cli/)
