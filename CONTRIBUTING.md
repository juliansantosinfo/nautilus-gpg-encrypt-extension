# Contribuindo para Nautilus GPG Encrypt Extension

Obrigado pelo interesse em contribuir!

## Como contribuir

1. **Fork o repositório** no GitHub.
2. Crie uma branch com um nome claro:

    ```bash
    git checkout -b feat/adicionar-exemplo
    ```

3. **Siga o padrão PEP8** (formatado automaticamente ao salvar via VS Code).
4. Adicione commits claros seguindo o padrão:
    - `feat: nova funcionalidade`
    - `fix: correção`
    - `docs: melhoria na documentação`
5. Abra um Pull Request explicando o que foi alterado.

## Sugestões úteis

- Sempre use `make deb` para testar builds.
- Use `nautilus -q` para recarregar o Nautilus após instalar.
- Se adicionar tradução, edite diretamente no dicionário `TRANSLATIONS` dentro do `.py`.

## Testando localmente

```bash
make install
nautilus -q
```
