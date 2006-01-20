# Extract translatable strings from Roundup sources,
# update and compile all existing translations
#
# $Id$

# tool locations
XPOT ?= xpot
MSGFMT ?= msgfmt
MSGMERGE ?= msgmerge
XGETTEXT ?= xgettext
PYTHON ?= python2.4

TEMPLATE=roundup.pot

PACKAGES=$(shell find .. -name '*.py'|sed -e 's,/[^/]*$$,,'|sort|uniq)
SOURCES=$(PACKAGES:=/*.py)
PO_FILES=$(wildcard *.po)
MO_FILES=$(PO_FILES:.po=.mo)
HTML=$(filter-out ../html/calendar.html,$(shell echo ../html/*.html))

RUN_PYTHON=$(PYTHON) -O
TAL_GETTEXT=${RUN_PYTHON} \
    /usr/local/lib/python2.4/site-packages/roundup/cgi/TAL/talgettext.py

all: dist

help:
	@echo "$(MAKE)           - build MO files.  Run this before sdist"
	@echo "$(MAKE) template  - update message template from sources"
	@echo "$(MAKE) locale.po - update message file from template"
	@echo "$(MAKE) locale.mo - compile individual message file"
	@echo "$(MAKE) help      - this text"\

# This will rebuild all MO files without updating their corresponding PO
# files first.  Run before creating Roundup distribution (hence the name).
# PO files should be updated by their translators only, automatic update
# adds unwanted fuzzy labels.
dist:
	for file in $(PO_FILES); do \
	  ${MSGFMT} -o `basename $$file .po`.mo $$file; \
	done

template: attr.py
	${XPOT} -n -o $(TEMPLATE) $(SOURCES) attr.py
	${TAL_GETTEXT} -u $(TEMPLATE) $(HTML)
	${XGETTEXT} -j -w 80 -F \
	  --msgid-bugs-address=rsc@runtux.com \
	  --copyright-holder="Ralf Schlatterbeck" \
	  -o $(TEMPLATE) $(SOURCES)

%.po: $(TEMPLATE)
	${MSGMERGE} -U --suffix=.bak $@ $<

%.mo: %.po
	${MSGFMT} --statistics -o $@ $<

attr.py: attributes.py ../schema.py
	$(RUN_PYTHON) attributes.py > attr.py
