package_name := wipi
LIB_DEST_DIR := /usr/lib/$(package_name)
EXEC_DIR := /usr/bin
private_scripts = 	\
					main.py	\
					dataviewhandler.py	\
					executor.sh	\
					parse.py	\
					register.html	\
					wipi

.PHONY: install
install: main.py dataviewhandler.py executor.sh parse.py register.html
	mkdir -p ${LIB_DEST_DIR}
	install -m755 main.py $(LIB_DEST_DIR)
	install -m755 dataviewhandler.py $(LIB_DEST_DIR)
	install -m755 executor.sh $(LIB_DEST_DIR)
	install -m755 parse.py $(LIB_DEST_DIR)
	install -m755 register.html $(LIB_DEST_DIR)
	install -m755 wipi $(EXEC_DIR)

.PHONY: uninstall
uninstall:
	rm -f $(LIB_DEST_DIR)/main.py
	rm -f $(LIB_DEST_DIR)/dataviewhandler.py
	rm -f $(LIB_DEST_DIR)/executor.sh
	rm -f $(LIB_DEST_DIR)/parse.py
	rm -f $(LIB_DEST_DIR)/register.html
	rmdir ${LIB_DEST_DIR}
