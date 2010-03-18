all: _generic.item.html userlist.html person.item.html person.index.html

_generic.item.html: _generic.index.html
	ln -s _generic.index.html _generic.item.html

userlist.html:
	cd .. && utils/userlist.py

person.index.html: address.index.html
	ln -s address.index.html person.index.html

person.item.html: address.item.html
	ln -s address.item.html person.item.html
