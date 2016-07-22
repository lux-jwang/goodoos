# Makefile for SEAL examples
BIN_DIR=.
INCLUDE_DIR=../
SEAL_DIR=../SEAL
CXXFLAGS=-Wall -Wno-unused-function -std=c++11 -O3 -I$(INCLUDE_DIR) -I$(SEAL_DIR)
UPPER_SRC = nbmutils.cpp spp.cpp topn.cpp
SRCS= main.cpp cnut.cpp $(addprefix $(INCLUDE_DIR),$(UPPER_SRC))
OBJS=$(SRCS:.cpp=.o)
SEALRUN=$(BIN_DIR)/test.exe

.PHONY: all clean

all: $(SEALRUN)

$(SEALRUN): $(OBJS)
	$(CXX) $(CXXFLAGS) $(OBJS) -lcppunit -L$(INCLUDE_DIR) -lseal -o $(SEALRUN)

clean:
	-rm -f $(OBJS) $(SEALRUN)