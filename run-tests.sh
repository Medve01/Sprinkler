rm /tmp/gpio*
poetry export -f requirements.txt --output requirements.txt --without-hashes
poetry run tox
rm /tmp/gpio*
