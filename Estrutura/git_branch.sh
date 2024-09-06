#!/bin/bash

# Conferindo se a branch main existe, se não, cria
git reset --hard
git checkout -b main || git checkout main
git pull

# Adicionar apenas o arquivo desejado
git add ./teste_scripts/teste.py

# Fazer o commit com uma mensagem
git commit -m "Correction commit"

# Enviar as mudanças para o repositório remoto
git push origin main
