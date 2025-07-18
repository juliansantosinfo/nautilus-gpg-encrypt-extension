PACKAGE_NAME = nautilus-gpg-encrypt-extension
VERSION = 1.0.1
DISTRO = noble 

.PHONY: all build install uninstall deb deb-local clean

all:
	@echo "-----------------------------------------------------"
	@echo "Bem-vindo ao Makefile do $(PACKAGE_NAME)!"
	@echo "-----------------------------------------------------"
	@echo "Comandos disponíveis:"
	@echo "  make build      - Gera o tarball .orig.tar.gz (fonte original)."
	@echo "  make deb        - Prepara o changelog e constrói o pacote fonte Debian para PPA."
	@echo "                    (Requer que 'make build' tenha sido executado ou que o .orig.tar.gz exista)"
	@echo "  make deb-local  - Constrói o pacote .deb binário localmente para teste."
	@echo "  make install    - Instala a extensão Python para Nautilus localmente."
	@echo "  make uninstall  - Remove a extensão Python do Nautilus."
	@echo "  make clean      - Limpa arquivos de build e temporários."
	@echo "-----------------------------------------------------"

build:
	@echo "Criando ${PACKAGE_NAME}_${VERSION}.orig.tar.gz..."
	tar -czvf ../${PACKAGE_NAME}_${VERSION}.orig.tar.gz --exclude='.git' --exclude='debian' .
	@echo "Tarball de origem criado em ../${PACKAGE_NAME}_${VERSION}.orig.tar.gz"
	@echo "Nenhuma etapa de build de código necessária para este projeto Python."

install:
	@echo "Instalando a extensão Nautilus GPG..."
	install -D -m 755 encrypt_gpg.py /usr/share/nautilus-python/extensions/encrypt_gpg.py
	@echo "Extensão instalada em /usr/share/nautilus-python/extensions/"
	@echo "Pode ser necessário reiniciar o Nautilus (nautilus -q) ou sua sessão para que as mudanças surtam efeito."

uninstall:
	@echo "Removendo a extensão Nautilus GPG..."
	rm -f /usr/share/nautilus-python/extensions/encrypt_gpg.py
	@echo "Extensão removida."

deb: build # Garante que o .orig.tar.gz esteja atualizado
	@echo "Atualizando debian/changelog e construindo pacote fonte para PPA..."
	# Cria uma nova entrada no changelog. Adicionando '1' para a revisão Debian inicial.
	dch -v $(VERSION)-1 --distribution $(DISTRO) "Nova versão automática via Makefile."
	# -S para pacote fonte, -sa para incluir o .orig.tar.gz (mesmo que já exista).
	debuild -S -sa
	@echo "Pacote fonte gerado. Verifique os arquivos *.dsc, *.orig.tar.gz, *.debian.tar.xz no diretório pai."
	@echo "Você pode agora enviar para seu PPA usando 'dput PPA_NOME ../$(PACKAGE_NAME)_$(VERSION)-1_source.changes'"

deb-local: build # Garante que o .orig.tar.gz esteja atualizado
	@echo "Atualizando debian/changelog e construindo pacote .deb localmente..."
	# Cria uma nova entrada no changelog. Adicionando '1' para a revisão Debian inicial.
	dch -v $(VERSION)-1 --distribution $(DISTRO) "Nova versão automática via Makefile (build local)."
	# -b para pacote binário, -us e -uc para não assinar (bom para builds locais)
	debuild -b -us -uc
	@echo "Pacote .deb gerado. Verifique o arquivo *.deb no diretório pai."
	@echo "Você pode instalar localmente usando 'sudo dpkg -i ../$(PACKAGE_NAME)_$(VERSION)-1_*.deb'"

clean:
	@echo "Limpando arquivos temporários e de build..."
	rm -f ../$(PACKAGE_NAME)_*deb ../$(PACKAGE_NAME)_*changes ../$(PACKAGE_NAME)_*dsc ../$(PACKAGE_NAME)_*buildinfo ../$(PACKAGE_NAME)_*udeb
	find . -depth -name '*~' -exec rm -f {} \;
	find . -depth -name '*.pyc' -exec rm -f {} \;
	find . -depth -name '*.pyo' -exec rm -f {} \;
	find . -depth -name '__pycache__' -exec rm -rf {} \;
	@echo "Limpeza concluída."
