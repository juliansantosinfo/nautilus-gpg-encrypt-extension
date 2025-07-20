PACKAGE_NAME = nautilus-gpg-encrypt-extension
VERSION = 1.0.0
DISTRO = noble 

.PHONY: all build install uninstall deb deb-local clean

all:
	@echo "-----------------------------------------------------"
	@echo "Welcome to the $(PACKAGE_NAME) Makefile!"
	@echo "-----------------------------------------------------"
	@echo "Available commands:"
	@echo "  make build      - Generates the .orig.tar.gz tarball (original source)."
	@echo "  make deb        - Prepares the changelog and builds the Debian source package for PPA."
	@echo "                    (Requires 'make build' to have been run or .orig.tar.gz to exist)"
	@echo "  make deb-local  - Builds the binary .deb package locally for testing."
	@echo "  make install    - Installs the Nautilus Python extension locally."
	@echo "  make uninstall  - Removes the Nautilus Python extension."
	@echo "  make clean      - Cleans build and temporary files."
	@echo "-----------------------------------------------------"

build:
	@echo "Creating ${PACKAGE_NAME}_${VERSION}.orig.tar.gz..."
	tar -czvf ../${PACKAGE_NAME}_${VERSION}.orig.tar.gz --exclude='.git' --exclude='debian' .
	@echo "Source tarball created in ../${PACKAGE_NAME}_${VERSION}.orig.tar.gz"
	@echo "No code build steps needed for this Python project."

install:
	@echo "Installing Nautilus GPG extension..."
	install -D -m 755 encrypt_gpg.py $(DESTDIR)/usr/share/nautilus-python/extensions/encrypt_gpg.py
	@echo "Extension installed in $(DESTDIR)/usr/share/nautilus-python/extensions/"
	@echo "You may need to restart Nautilus (nautilus -q) or your session for changes to take effect."

uninstall:
	@echo "Removing Nautilus GPG extension..."
	rm -f $(DESTDIR)/usr/share/nautilus-python/extensions/encrypt_gpg.py
	@echo "Extension removed."

deb: build # Ensures the .orig.tar.gz is up-to-date
	@echo "Updating debian/changelog and building source package for PPA..."
	dch -v $(VERSION)-1 --distribution $(DISTRO) "Automatic new version with Makefile."
	debuild -S -sa
	@echo "Source package generated. Check *.dsc, *.orig.tar.gz, *.debian.tar.xz files in the parent directory."
	@echo "You can now upload to your PPA using 'dput PPA_NAME ../$(PACKAGE_NAME)_$(VERSION)-1_source.changes'"

deb-local: build # Ensures the .orig.tar.gz is up-to-date
	@echo "Updating debian/changelog and building .deb package locally..."
	dch -v $(VERSION)-1 --distribution $(DISTRO) "Automatic new version with Makefile. (local build)."
	debuild -b -us -uc
	@echo "Binary .deb package generated. Check the *.deb file in the parent directory."
	@echo "You can install locally using 'sudo dpkg -i ../$(PACKAGE_NAME)_$(VERSION)-1_*.deb'"

deb-dev: build # Ensures the .orig.tar.gz is up-to-date
	debuild -b -us -uc
	@echo "Binary .deb package generated. Check the *.deb file in the parent directory."
	@echo "You can install locally using 'sudo dpkg -i ../$(PACKAGE_NAME)_$(VERSION)-1_*.deb'"

push:
	@echo "Pushing new package to PPA..."
	dput ppa:juliansantosinfo/nautilus-gpg-encrypt-extension ../nautilus-gpg-encrypt-extension_$(VERSION)-1_source.changes

clean:
	@echo "Cleaning temporary and build files..."
	rm -f ../$(PACKAGE_NAME)_*deb ../$(PACKAGE_NAME)_*changes ../$(PACKAGE_NAME)_*dsc ../$(PACKAGE_NAME)_*buildinfo ../$(PACKAGE_NAME)_*udeb
	@echo "Cleanup complete."