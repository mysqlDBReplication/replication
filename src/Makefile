BASE_DIR := .
SRC_DIR  := ./../common/proto
DST_DIR  := .

CONFIG_PROTO             :=  config.proto
detect_change_script     := detect_changes.py
detect_changes_test      := detect_changes_unit_test.py
GENARL_UTILS             := general_utils.py
GENARL_UTILS_TEST        := general_utils_test.py

COMPILER := protoc
OPTIONS := -I=${SRC_DIR} --python_out=${DST_DIR}

all:
	make proto

proto: ${SRC_DIR}/${CONFIG_PROTO}
	${COMPILER} ${OPTIONS} ${SRC_DIR}/${CONFIG_PROTO}

detect_changes_test: ${BASE_DIR}/${detect_change_script}
	python ${BASE_DIR}/${detect_changes_test}

general_test: ${BASE_DIR}/${GENARL_UTILS} 
	python ${BASE_DIR}/${GENARL_UTILS_TEST}

test: ${BASE_DIR}/${detect_change_script}
	make detect_changes_test
	make general_test

clean:
	\rm -rf ${BASE_DIR}/*.pyc ${BASE_DIR}/*_pb2.py
