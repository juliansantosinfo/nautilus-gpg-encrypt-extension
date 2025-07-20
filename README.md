# GPG Encrypt Extension for Nautilus

A simple extension for the Nautilus file manager that allows you to encrypt and decrypt files using GPG directly from the context menu.

![Screenshot](https://i.imgur.com/your-screenshot.png)

## Features

* Encrypt files with a GPG key or a password (symmetric encryption).
* Decrypt `.gpg` files.
* Direct integration with Nautilus context menu.

---

## Installation (via PPA - Recommended)

The recommended way to install this extension on Ubuntu and derivatives is via PPA:

```bash
sudo add-apt-repository ppa:juliansantosinfo/nautilus-gpg-encrypt-extension
sudo apt update
sudo apt install nautilus-gpg-encrypt-extension
nautilus -q
````

---

## How to Use

* **Encrypt:** Right-click on a file and select **GPG Encryption**.
* **Decrypt:** Right-click on a `.gpg` file and select **GPG Decryption**.
