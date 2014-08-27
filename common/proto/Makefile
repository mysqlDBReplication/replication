BASE_DIR := .
SRC_DIR  := .
DST_DIR  := ./../../src

CONFIG_PROTO        :=  config.proto


COMPILER		:= protoc
OPTIONS := -I=${SRC_DIR} --python_out=${DST_DIR}

all:
	make proto

proto: ${BASE_DIR}/${CONFIG_PROTO}
	${COMPILER} ${OPTIONS} ${BASE_DIR}/${CONFIG_PROTO}
