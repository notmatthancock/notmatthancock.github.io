all:
	gcc -c stack.h
	f2py region_growing.pyf -c stack.h region_growing.c -m region_growing # -DF2PY_REPORT_ON_ARRAY_COPY=1
