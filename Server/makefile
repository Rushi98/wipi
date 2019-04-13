package_name := wipi
LIB_DEST_DIR := /usr/lib/$(package_name)
EXEC_DIR := /usr/bin
SYSTEMD_UNIT_DIR := /usr/lib/systemd/systemd

.PHONY: install
install: main.py dataviewhandler.py executor.sh parse.py register.html wipi rpi.db wipi.service
	mkdir -p $(LIB_DEST_DIR)
	install -m755 main.py $(LIB_DEST_DIR)
	install -m755 dataviewhandler.py $(LIB_DEST_DIR)
	install -m755 executor.sh $(LIB_DEST_DIR)
	install -m755 parse.py $(LIB_DEST_DIR)
	install -m755 register.html $(LIB_DEST_DIR)
	install -m755 wipi $(EXEC_DIR)
	install -m644 wipi.service $(SYSTEMD_UNIT_DIR)
	systemctl enable wipi.service

.PHONY: uninstall
uninstall:
	rm $(EXEC_DIR)/wipi
	rm $(LIB_DEST_DIR)/main.py
	rm $(LIB_DEST_DIR)/dataviewhandler.py
	rm $(LIB_DEST_DIR)/executor.sh
	rm $(LIB_DEST_DIR)/parse.py
	rm $(LIB_DEST_DIR)/rpi.db
	rm $(LIB_DEST_DIR)/register.html
	rmdir $(LIB_DEST_DIR)
	systemctl disable wipi.service
	rm $(SYSTEMD_UNIT_DIR)/wipi.service
