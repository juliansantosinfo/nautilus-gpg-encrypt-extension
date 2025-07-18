#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Nautilus extension to encrypt and decrypt files using GPG.

This extension adds "Encrypt with GPG" and "Decrypt with GPG" items
to the right-click context menu in Nautilus.
"""

import locale
import logging
import re
from typing import List

import gi
import gnupg
from gi.repository import Gio, GLib, GObject, Gtk, Nautilus

gi.require_version("Nautilus", "4.0")
gi.require_version("Gtk", "4.0")


APP_NAME = "GPGEncryptExtension"
APP_DESCRIPTION = "Nautilus extension to encrypt and decrypt files using GPG."
ENCRYPT_DESCRIPTION = (
    "Encrypts the selected file using the recipient's public GPG key or " "passphrase"
)
DECRYPT_DESCRIPTION = (
    "Decrypts the selected file using the recipient's private GPG key or " "passphrase"
)

UBUNTU_KEY_IDENTIFIER = "Created on UBUNTU"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(APP_NAME)


# Tradução simples via dicionário
LANG = locale.getdefaultlocale()[0] or "en"
TRANSLATIONS = {
    "pt_BR": {
        "Encrypt with GPG": "Criptografar com GPG",
        "Decrypt with GPG": "Descriptografar com GPG",
        "Enter password": "Digite a senha",
        "Encrypt": "Criptografar",
        "With Password": "Com Frase Secreta",
        "GPG Encryption": "Criptografia GPG",
        "GPG Decryption": "Descriptografia GPG",
        ENCRYPT_DESCRIPTION: "Criptografa o arquivo selecionado usando a chave GPG do destinatário ou senha",
        DECRYPT_DESCRIPTION: "Descriptografa o arquivo selecionado usando a chave GPG do destinatário ou senha",
    },
    "default": {},
}


def _(text):
    return TRANSLATIONS.get(LANG, TRANSLATIONS["default"]).get(text, text)


class EncryptPasswordWindow(Gtk.Window):
    """
    Window to prompt the user for a password for symmetric encryption.

    It contains a Gtk.Entry for password input and a button to confirm.
    When the button is clicked, the entered password is returned and the
    window closes.
    """

    def __init__(self):
        """Init the EncryptPasswordWindow."""
        super().__init__(title=_("Enter password"))
        self.set_default_size(300, 100)
        self.set_resizable(False)
        self.set_modal(True)

        vbox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12,
            margin_top=12,
            margin_bottom=12,
            margin_start=12,
            margin_end=12,
        )
        self.set_child(vbox)

        self.entry = Gtk.Entry()
        self.entry.set_visibility(False)
        self.entry.set_placeholder_text(_("Enter password"))
        vbox.append(self.entry)

        button = Gtk.Button(label=_("Encrypt"))
        button.connect("clicked", self.on_button_clicked)
        vbox.append(button)

        self.loop = GLib.MainLoop()
        self.loop_running = False

    def run(self):
        """
        Run the main loop to keep the window open until user input.

        Returns:
            str: The entered password when the button is clicked.
        """
        nautilus_app = Gtk.Application.get_default()
        nautilus_window = nautilus_app.get_active_window()
        self.set_transient_for(nautilus_window)

        self.present()
        self.loop_running = True
        self.loop.run()

        return self.entry.get_text()

    def on_button_clicked(self, button):
        """
        Handle the button click event.

        Args:
            button (Gtk.Button): The button that was clicked.
        """
        if self.loop_running:
            self.loop.quit()
            self.loop_running = False
        self.destroy()


class GPGEncryptExtension(GObject.GObject, Nautilus.MenuProvider):
    """
    Nautilus extension to encrypt and decrypt files using GPG.

    This extension adds "Encrypt with GPG" and "Decrypt with GPG" items
    to the right-click context menu in Nautilus.
    """

    def __init__(self):
        """Initialize the GPGEncryptExtension."""
        super().__init__()
        self.gpg = None
        self.gpg_keys = []
        self._initialize_gpg_and_keys()

    def _initialize_gpg_and_keys(self):
        """Initialize the GPG library and load available public keys."""
        logger.info("Loading GPG keys...")

        try:
            self.gpg = gnupg.GPG()
            public_keys = self.gpg.list_keys()

            if not public_keys:
                logger.warning(
                    "No GPG public keys found. Please create one using 'gpg --full-generate-key'."
                )
                return

            for key in public_keys:
                if UBUNTU_KEY_IDENTIFIER in key["uids"][0]:
                    continue

                if key["uids"]:
                    matches = re.finditer(r"<(.*?)>", key["uids"][0], re.MULTILINE)
                    for match in matches:
                        self.gpg_keys.append((match.group(1), key["fingerprint"]))

            logger.info(f"Keys found: {self.gpg_keys}")

        except Exception as e:
            logger.error(f"Error loading keys: {e}")

    def encrypt_file_callback(
        self, menu_item, file_info, gpg_recipient_uid, symmetric, **kwargs
    ):
        """
        Encrypt the selected file using the recipient's public GPG key.

        Args:
            menu_item (Nautilus.MenuItem): The menu item that was clicked.
            file_info (Nautilus.FileInfo): Info about the selected file.
            gpg_recipient_uid (str): The recipient's GPG key UID.
            symmetric (bool): Whether to use symmetric encryption.
            **kwargs: Additional keyword arguments.
        """
        passphrase = ""
        if symmetric:
            window_for_password = EncryptPasswordWindow()
            passphrase = window_for_password.run()

        if gpg_recipient_uid:
            logger.info(f"Encrypting {file_info.get_name()} for {gpg_recipient_uid}")
        elif symmetric:
            logger.info(f"Encrypting {file_info.get_name()} with symmetric method.")
        else:
            logger.warning("Not informing recipient UID or password for encryption.")
            return

        file_uri = file_info.get_uri()
        input_path = Gio.File.new_for_uri(file_uri).get_path()
        output_path = input_path + ".gpg"

        try:
            if symmetric:
                encrypted_data = self.gpg.encrypt_file(
                    input_path,
                    recipients=[],
                    symmetric=symmetric,
                    passphrase=passphrase,
                    output=output_path,
                )
            else:
                encrypted_data = self.gpg.encrypt_file(
                    input_path, recipients=[gpg_recipient_uid], output=output_path
                )

            if encrypted_data.ok:
                logger.info(
                    f"File encrypted successfully. Status: {encrypted_data.status}"
                )
                logger.info(
                    f"'{file_info.get_name()}' successfully encrypted for '{gpg_recipient_uid}' at '{output_path}'"
                )
            else:
                error_msg = encrypted_data.stderr or encrypted_data.status
                logger.error(f"Encryption failed: {error_msg}")

        except FileNotFoundError:
            logger.error("Input file not found.")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

    def decrypt_file_callback(self, menu_item, file_info, **kwargs):
        """
        Decrypt the selected file using the recipient's private GPG key.

        Args:
            menu_item (Nautilus.MenuItem): The menu item that was clicked.
            file_info (Nautilus.FileInfo): Info about the selected file.
            **kwargs: Additional keyword arguments.
        """
        logger.info(f"Decrypting {file_info.get_name()}")

        file_uri = file_info.get_uri()
        input_path = Gio.File.new_for_uri(file_uri).get_path()
        output_path = input_path.replace(".gpg", "")

        try:
            with open(input_path, "rb") as f:
                decrypted_data = self.gpg.decrypt(f.read(), output=output_path)

            if decrypted_data.ok:
                logger.info(
                    f"File decrypted successfully. Status: {decrypted_data.status}"
                )
                logger.info(
                    f"'{file_info.get_name()}' successfully decrypted at '{output_path}'"
                )
            else:
                error_msg = decrypted_data.stderr or decrypted_data.status
                logger.error(f"Decryption failed: {error_msg}")

        except FileNotFoundError:
            logger.error("Input file not found.")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

    def get_file_items(self, files: List[Nautilus.FileInfo]) -> List[Nautilus.MenuItem]:
        """
        Return menu items for selected files in Nautilus.

        Args:
            files (List[Nautilus.FileInfo]): A list of selected files.

        Returns:
            List[Nautilus.MenuItem]: A list of menu items.
        """
        if not self.gpg_keys:
            return []

        # Checks if exactly one file is selected and it is a regular file.
        if len(files) != 1 or files[0].is_directory() or files[0].is_gone():
            return []

        file = files[0]

        def create_base_menu_item(name, label, tip):
            return Nautilus.MenuItem(
                name=f"{APP_NAME}::{name}",
                label=label,
                tip=tip,
            )

        def get_encrypt_menu():
            """Create the encryption menu item."""
            encrypt_menu = create_base_menu_item(
                name="Encrypt",
                label=_("GPG Encryption"),
                tip=_(ENCRYPT_DESCRIPTION),
            )
            encrypt_submenu = Nautilus.Menu()
            encrypt_menu.set_submenu(encrypt_submenu)

            encrypt_with_password_menu = Nautilus.MenuItem(
                name="GPGEncryptExtension::Recipient::WithPassword",
                label=_("With Password"),
                tip=_("Encrypt with password"),
            )
            encrypt_with_password_menu.connect(
                "activate", self.encrypt_file_callback, file, None, True
            )
            encrypt_submenu.append_item(encrypt_with_password_menu)

            for key_uid, fingerprint in self.gpg_keys:
                item_name = f"GPGEncryptExtension::Recipient::{key_uid.replace(' ', '_').replace('@', '_')}"
                menu_item = Nautilus.MenuItem(
                    name=item_name,
                    label=f"{key_uid}",
                    tip=f"Encrypt for {key_uid}",
                )
                menu_item.connect(
                    "activate", self.encrypt_file_callback, file, fingerprint, False
                )
                encrypt_submenu.append_item(menu_item)

            return encrypt_menu

        def get_decrypt_menu():
            """Create the decryption menu item."""
            decrypt_menu = create_base_menu_item(
                name="Decrypt",
                label=_("GPG Decryption"),
                tip=_(DECRYPT_DESCRIPTION),
            )
            decrypt_menu.connect("activate", self.decrypt_file_callback, file)
            return decrypt_menu

        return [get_encrypt_menu(), get_decrypt_menu()]

    def get_background_items(
        self,
        current_folder: Nautilus.FileInfo,
    ) -> List[Nautilus.MenuItem]:
        """
        Return menu items for the background context menu in Nautilus.

        Args:
            current_folder: The current folder.

        Returns:
            An empty list, as this extension does not provide background items.
        """
        return []
