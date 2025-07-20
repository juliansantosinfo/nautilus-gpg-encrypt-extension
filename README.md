# GPG Encrypt Extension for Nautilus

A simple extension for the Nautilus file manager that allows you to encrypt and decrypt files using GPG directly from the context menu.

![Screenshot](https://i.imgur.com/your-screenshot.png)

## Features

* Encrypt files with a GPG key or a password (symmetric encryption).
* Decrypt `.gpg` files.
* Direct integration with Nautilus context menu.

---

## Installation (PPA - Recommended)

The recommended way to install this extension on Ubuntu and derivatives is via PPA:

```bash
sudo add-apt-repository ppa:juliansantosinfo/nautilus-gpg-encrypt-extension
sudo apt update
sudo apt install nautilus-gpg-encrypt-extension
nautilus -q
