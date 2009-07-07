all: _generic.item.html userlist.html

_generic.item.html: _generic.index.html
	ln -s _generic.index.html _generic.item.html

userlist.html:
	cd .. && utils/userlist.py
