PACKAGE_NAME = nautilus-gpg-encrypt-extension
VERSION = 1.0.0
DISTRO = noble

.PHONY: all build clean install deb

all:
	@echo "Use 'make deb' para construir o pacote Debian."
	@echo "Use 'make install' para instalar localmente."
	@echo "Use 'make clean' para limpar arquivos temporários."

build:
	@echo "Nenhuma etapa de build necessária para este projeto Python."

install:
	sudo install -D -m 755 encrypt_gpg.py /usr/share/nautilus-python/extensions/encrypt_gpg.py
	@echo "Extensão instalada em /usr/share/nautilus-python/extensions/"

uninstall:
	sudo rm -f /usr/share/nautilus-python/extensions/encrypt_gpg.py
	@echo "Extensão removida."

deb:
	dch -v $(VERSION)-1 --distribution $(DISTRO) "Nova versão automática via Makefile."
	debuild -S -sa

clean:
	debuild clean || true
# 	rm -rf ../$(PACKAGE_NAME)_* ../*.build ../*.buildinfo ../*.changes
	@echo "Arquivos temporários e builds removidos."
