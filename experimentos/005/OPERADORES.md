# ALAYA-999 005 | Guia de operação / operator guide · v0.1.0

**Português:** Este ensaio gratuito pede dois operadores independentes que já usem Kubo e uma terceira pessoa em máquina/rede separada. Mantenha a âncora pública de 4.639 bytes por sete dias a partir da data combinada. Participe ou retire-se pelo [tópico de coordenação](https://github.com/cesaragliardi-creator/alaya-999-public/issues/13). Só entram no registro público nós autorizados expressamente. Não exponha credenciais, IP, logs pessoais ou dados privados.

**English:** This no-cost trial seeks two independent existing Kubo operators and a third verifier on a separate machine/network. Hold the 4,639-byte public anchor for seven days from the coordinated start. Join or withdraw via the [coordination issue](https://github.com/cesaragliardi-creator/alaya-999-public/issues/13). Public node registration is opt-in. Never post credentials, IP addresses, personally identifying logs or private memory.

## Operators A and B only / Apenas operadores A e B

Use an existing, updated [official Kubo installation](https://docs.ipfs.tech/install/command-line/). Do not change firewall rules, expose the administrative API or grant anyone access to your device. Importing public content into an online IPFS node can advertise that your node can serve it. If that is not acceptable, offer method review instead.

1. Download the [public CAR transport](https://cesaragliardi-creator.github.io/alaya-999-public/experimentos/004/ALAYA-anchor-v1.car.b64) and decode Base64 into `ALAYA-anchor-v1.car` (for example, `base64 -d ALAYA-anchor-v1.car.b64 > ALAYA-anchor-v1.car` on GNU systems).
2. Check the decoded CAR SHA-256: `de3baff015c429dc676d24ff9ef279b719bab28438e6cc370201e1ee86b7d3ef`. Stop on mismatch.
3. Run `ipfs dag import ALAYA-anchor-v1.car` and verify the root is pinned with `ipfs pin ls bafkreica6jcydxtxyejv5ofdbqdiexadqhdazzwbfmn7wkxn4ya36st4by`.
4. Report readiness and confirm the coordinated test window. Do not disclose any network identifier publicly without opt-in. A reported pin is not independent retrieval evidence.
5. At withdrawal, tell coordinators so results are not misattributed. Removing a pin is optional and is your decision; removing it cannot remove copies held by others.

## Verifier C only / Apenas verificador C

1. Receive only the CID from the coordinator, never the CAR or anchor bytes before retrieval. Start a new empty Kubo repository and make sure it cannot load a previous local copy. Do not create new public shares or expose services.
2. The coordinator records A's confirmed shutdown time. Attempt a CID-only retrieval with a declared time budget: `ipfs block get bafkreica6jcydxtxyejv5ofdbqdiexadqhdazzwbfmn7wkxn4ya36st4by > recovered.json`. Use a fresh repository for each additional mode. `ipfs routing findprovs <CID>` is a discovery diagnostic, not proof of recovery.
3. Only after the retrieval attempt, check size and SHA-256: 4,639 bytes; `40f24581de77c1135eb8a30c06825c0381c60ce6c12b1bfb2aede601bf4a7c0e`. The root is a single raw block, so the raw block bytes should be the anchor bytes. Save negative observations as well.
4. In a separate fresh run, if B has explicitly agreed, verify attribution with a direct, provider-specific test. Report gateway-based results separately; a gateway could serve cached content. If B's role is unproved, report independent retrieval from an unknown provider rather than B's failover.
5. Repeat after B disconnects/reconnects if agreed, and again at a measured interval within the seven days. A pass proves only the measured time and circumstances.

### Report template / Modelo de relato

```yaml
role: operator | verifier | method-review
utc: YYYY-MM-DDTHH:MM:SSZ
kubo_version: unknown
mode: cid-only | consented-peer | gateway | local-fixture
origin_offline_confirmed: unknown
clean_store_confirmed: unknown
separate_machine_and_operator: unknown
result: matched | mismatch | timeout | unavailable | method-review
bytes: null
sha256: null
public_registry_opt_in: false
notes: ""
```

A label or timestamp does not prove authority or provenance. Keep older manifests, never overwrite the frozen anchor, and keep two conflicting records until evidence plus authorized human review warrants a recorded decision. See [004](https://cesaragliardi-creator.github.io/alaya-999-public/experimentos/004/) and [Kubo command reference](https://docs.ipfs.tech/reference/kubo/cli/).
