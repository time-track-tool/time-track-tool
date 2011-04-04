all: _generic.item.html userlist.html person.item.html person.index.html \
     customer.index.html customer.item.html device.item.html

_generic.item.html: _generic.index.html
	ln -s _generic.index.html _generic.item.html

userlist.html:
	cd .. && utils/userlist.py

customer.index.html: address.index.html
	ln -s address.index.html customer.index.html

customer.item.html: address.item.html
	ln -s address.item.html customer.item.html

person.index.html: address.index.html
	ln -s address.index.html person.index.html

person.item.html: address.item.html
	ln -s address.item.html person.item.html

device.item.html: device.index.html
	ln -s device.index.html device.item.html
