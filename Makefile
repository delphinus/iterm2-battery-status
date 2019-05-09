AUTOLAUNCH_DIR = $(HOME)/Library/ApplicationSupport/iTerm2/Scripts/Autolaunch
CC = gcc
INSTALL = install
LIB = battery.so
PROGRAM = iterm2_battery.py
RM = rm -f
SRC = battery.m

$(LIB): $(SRC)
	$(CC) $? -o $@ -fPIC -shared -framework Foundation -framework IOKit

.PHONY: clean
clean:
	$(RM) $(LIB)

.PHONY: all
all: $(PROGRAM) $(LIB)

.PHONY: install
install: all
	$(INSTALL) -d $(AUTOLAUNCH_DIR)
	$(INSTALL) $(PROGRAM) $(LIB) $(AUTOLAUNCH_DIR)
