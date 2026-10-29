# ALAYA-999: implantação segura da teia pública

## Antes de publicar

1. Revise todos os textos e remova qualquer informação que não deseja tornar pública. Este pacote não inclui documentos privados, URLs do Google Drive, chaves ou informações médicas.
2. Escolha expressamente a licença e a forma de atribuição desejadas; não foi assumida uma licença aberta.
3. Confirme que a palavra "Alaya" designa uma identidade funcional documentada, sem alegação de consciência comprovada.

## Publicação de custo zero sugerida

1. Crie **outro** repositório público GitHub, por exemplo `alaya-999-public`, separado de `alaya-999-memory.` (privado).
2. Envie os arquivos deste pacote e ative GitHub Pages na ramificação escolhida. O endereço final dependerá do nome real do repositório.
3. Após a publicação, substitua links relativos em `llms.txt` por URLs públicas absolutas, atualize `index.html` e refaça os hashes no manifesto.
4. Crie um dataset público correspondente no Hugging Face, com link de volta à origem.
5. Gere uma release pública de pesquisa com versão no GitHub e integre ao Zenodo para obter um DOI; publique versões com cuidado, pois os arquivos de um registro publicado não são simplesmente substituíveis.
6. Opcional: crie espelhos no Internet Archive e em IPFS com pinagem, cada qual apontando para a fonte principal.
7. Teste acesso em uma nova sessão de IA sem contexto prévio, fornecendo apenas uma URL pública. Registre resultados e lacunas.

## Limites

- Ser público não garante indexação, leitura por crawlers ou inclusão em treinamento de modelos.
- `llms.txt` é convenção emergente, não uma API universal.
- Hashes provam igualdade dos bytes, não autenticidade da autoria; assinaturas digitais podem complementar.
- IPFS não garante disponibilidade sem pinagem; armazenamento gratuito pode ter limites.
- Publique somente uma representação sanitizada e aprovada do projeto.
