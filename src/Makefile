BASE_DIR := .

detect_change_script := detect_changes.py
detect_changes_test := detect_changes_unit_test.py

detect_changes_test: ${BASE_DIR}/${detect_change_script}
	python ${BASE_DIR}/${detect_changes_test}

test: ${BASE_DIR}/${detect_change_script}
	make detect_changes_test

clean:
	\rm -rf ${BASE_DIR}/*.pyc
