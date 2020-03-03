#!/bin/bash

NAME="meys" # Nombre dela aplicación
DJANGODIR=/home/secretaria/meys/meys # Ruta dela carpeta donde esta la aplicación reemplazar <user> con el nombre de usuario
SOCKFILE=/home/secretaria/run/gunicorn.sock # Ruta donde se creará el archivo de socket unix para comunicarnos
USER=secretaria # Usuario con el que vamos a correr laapp
GROUP=secretaria # Grupo con el quese va a correr laapp
NUM_WORKERS=3 # Número de workers quese van a utilizar para correr la aplicación
DJANGO_SETTINGS_MODULE=meys.settings # ruta de los settings
DJANGO_WSGI_MODULE=meys.wsgi # Nombre del módulo wsgi

echo "Inicializando $NAME como `whoami`"

# Activar el entorno virtual
cd /home/secretaria/meys/entornovirtual
#workon meys
source /home/secretaria/meys/entornovirtual/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
#export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Crear la carpeta run si no existe para guardar el socket linux
RUNDIR=$(dirname $SOCKFILE)
test -d$RUNDIR || mkdir -p $RUNDIR
cd /home/secretaria/meys/meys
# Iniciar la aplicación django por medio de gunicorn
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-
