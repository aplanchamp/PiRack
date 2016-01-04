#
# slave Makefile
#

CC      = gcc
CFLAGS  = -g -I../src
LFLAGS  = -L.. -liniparser
AR	    = ar
ARFLAGS = rcv
RM      = rm -f


default: all

all: slave

slave: slave.c
	$(CC) $(CFLAGS) -o slave slave.c -I./src -L. -liniparser

clean veryclean:
	$(RM) slave
