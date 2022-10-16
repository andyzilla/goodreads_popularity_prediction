# especificamos a partir de qué imagen vamos a partir
FROM python:3.10

# a partir de acá, vamos a incluir algunas instrucciones más

# home directory
WORKDIR /code

# copiamos los requirements en este nuevo entorno
COPY requirements.txt requirements.txt

# instala las dependencias que estan en requirements
RUN pip install -r requirements.txt

# copia todo el proyecto en la nueva ubicación de docker
COPY . .