#!/bin/bash

SCRIPT_ROOT="$(cd "$(dirname "$0")"; pwd)"
SCRIPT_SHORT="$(basename "$0")"
SCRIPT_PATH="$SCRIPT_ROOT/$SCRIPT_SHORT"

VENV_NAME=venv
ENV_FILE=.env

unset SCRIPT_SHORT

cd "$SCRIPT_ROOT" && python3 -m virtualenv "$VENV_NAME"
[ "$?" != 0 ] && echo "ERROR: Failed to create venv $VENV_NAME. Aborting!" && exit 1
echo

echo "=========================================================================="
echo "Running virtualenv \"$VENV_NAME\" Under \"$SCRIPT_ROOT\""
echo "=========================================================================="
echo
source "$SCRIPT_ROOT/$VENV_NAME/bin/activate"
[ "$?" != 0 ] && echo "ERROR: Failed loading venv environment $VENV_NAME. Aborting!" && exit 1

if [ -r "$SCRIPT_ROOT/requirements.txt" ]
then
    pip3 install -r "$SCRIPT_ROOT/requirements.txt" --trusted-host pypi.org --trusted-host files.pythonhosted.org
    [ "$?" != 0 ] && echo "ERROR: Failed to install requirements. Aborting!" && exit 1
fi

echo "=========================================================================="
echo "Adding $SCRIPT_ROOT to PYTHONPATH for $VENV_NAME"
echo "=========================================================================="
echo
cd $(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
echo $SCRIPT_ROOT > proj_packages.pth
[ "$?" != 0 ] && echo "ERROR: Failed to add python project path to $VENV_NAME. Aborting!" && exit 1

cd "$SCRIPT_ROOT" && set -a && source $ENV_FILE
[ "$?" == 0 ] && echo "Environment configured!"

echo
echo "=========================================================================="
echo "Starting up docker container"
echo "=========================================================================="
echo
docker-compose build
docker-compose up