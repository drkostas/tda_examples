# Makefile for the tda_playground module

#ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
ROOT_DIR:=$(shell pwd)  # If this doesn't work try the command above
SHELL=/bin/bash
PYTHON_VERSION=3.7  # Change this to select python version

# You can use either venv (virtualenv) or conda env by specifying the correct argument (env=<conda, venv>)
ifeq ($(env),conda)
	# Use Conda
	BASE=~/anaconda3/envs/tda_playground
	BIN=$(BASE)/bin
	CLEAN_COMMAND="conda env remove -p $(BASE)"
	CREATE_COMMAND="conda create --prefix $(BASE) python=$(PYTHON_VERSION) -y"
#	SETUP_FLAG=
else ifeq ($(env),venv)
	# Use Venv
	BASE=venv
	BIN=$(BASE)/bin
	CLEAN_COMMAND="rm -rf $(BASE)"
	CREATE_COMMAND="python$(PYTHON_VERSION) -m venv $(BASE)"
#	SETUP_FLAG=
else
	# Use Conda
	BASE=~/anaconda3/envs/tda_playground
	BIN=$(BASE)/bin
	CLEAN_COMMAND="conda env remove -p $(BASE)"
	CREATE_COMMAND="conda create --prefix $(BASE) python=$(PYTHON_VERSION) --file gda-public/requirements.txt -y"
#	SETUP_FLAG='--local' # If you want to use this, you change it in setup.py too
endif

all:
	$(MAKE) help
help:
	@echo
	@echo "-----------------------------------------------------------------------------------------------------------"
	@echo "                                              DISPLAYING HELP                                              "
	@echo "-----------------------------------------------------------------------------------------------------------"
	@echo "Use make <make recipe> [env=<conda|venv>] to specify the env"
	@echo "Default env: conda"
	@echo
	@echo "make help"
	@echo "       Display this message"
	@echo "make install [env=<conda|venv>]"
	@echo "       Call clean delete_conda_env create_conda_env setup update_gda install_gda"
	@echo "make clean [env=<conda|venv>]"
	@echo "       Delete all './build ./dist ./*.pyc ./*.tgz ./*.egg-info' files"
	@echo "make delete_env [env=<conda|venv>]"
	@echo "       Delete the current conda env or virtualenv"
	@echo "make create_env [env=<conda|venv>]"
	@echo "       Create a new conda env or virtualenv for the specified python version"
	@echo "make setup [env=<conda|venv>]"
	@echo "       Call setup.py install"
	@echo "make update_gda [env=<conda|venv>]"
	@echo "       Update the gda-public repository"
	@echo "make install_gda [env=<conda|venv>]"
	@echo "       Install the gda-public library"
	@echo "-----------------------------------------------------------------------------------------------------------"
install:
	$(MAKE) clean
	$(MAKE) delete_env
	$(MAKE) create_env
	$(MAKE) setup
	$(MAKE) update_gda
	$(MAKE) install_gda
	@echo "Installation Successful!"
clean:
	$(PYTHON_BIN)python setup.py clean
delete_env:
	@echo "Deleting virtual environment.."
	eval $(DELETE_COMMAND)
create_env:
	@echo "Creating virtual environment.."
	eval $(CREATE_COMMAND)
setup:
	$(BIN)/pip install --upgrade pip
	$(BIN)/python setup.py install $(SETUP_FLAG)
update_gda:
	cd gda-public && git pull
install_gda:
	$(BIN)/pip install Cython
	$(BIN)/pip install "file://$(ROOT_DIR)/gda-public"


.PHONY: help install clean delete_env create_env setup install_gda update_gda