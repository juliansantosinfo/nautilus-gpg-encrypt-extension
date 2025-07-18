# Extensão GPG Encrypt para Nautilus

Uma extensão simples para o gerenciador de arquivos Nautilus que permite criptografar e descriptografar arquivos usando GPG diretamente do menu de contexto.

![Screenshot](https://i.imgur.com/your-screenshot.png)

## Funcionalidades

* Criptografa arquivos com uma chave GPG ou com uma senha (criptografia simétrica).
* Descriptografa arquivos `.gpg`.
* Integração direta com o menu de contexto do Nautilus.

---

## Instalação (via PPA - Recomendado)

A forma recomendada de instalar esta extensão no Ubuntu e derivados é via PPA:

```bash
sudo add-apt-repository ppa:juliansantosinfo/nautilus-gpg-encrypt-extension
sudo apt update
sudo apt install nautilus-gpg-encrypt-extension
nautilus -q
```

---

## Como Usar

* **Criptografar:** clique com o direito em um arquivo e escolha **GPG Encryption**.
* **Descriptografar:** clique com o direito em um arquivo `.gpg` e escolha **GPG Decryption**.
