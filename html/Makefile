all: _generic.item.html userlist.html person.item.html person.index.html \
     customer.index.html customer.item.html device.item.html \
     sensor.item.html sensor.index.html measurement.index.html \
     device_group.item.html ext_tracker_state.ext_attr.html \
     userlist.js

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

sensor.item.html: device.index.html
	ln -s device.index.html sensor.item.html

sensor.index.html: device.index.html
	ln -s device.index.html sensor.index.html

measurement.index.html: device.index.html
	ln -s device.index.html measurement.index.html

device_group.item.html: device_group.index.html
	ln -s device_group.index.html device_group.item.html

ext_tracker_state.ext_attr.html: issue.ext_attr.html
	ln -s issue.ext_attr.html ext_tracker_state.ext_attr.html
