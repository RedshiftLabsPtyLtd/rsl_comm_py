TARGET_EGG_INFO=rsl_comm_py.egg-info
DIST=dist
BUILD=build

all:
	python3.7 setup.py sdist bdist_wheel

clean:
	rm  -rf ${TARGET_EGG_INFO} ${DIST} ${BUILD}
