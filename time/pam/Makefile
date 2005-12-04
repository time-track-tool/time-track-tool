all: pwch_notify.so

%.so: %.c
	cc -shared $< -o $@ -lpam
