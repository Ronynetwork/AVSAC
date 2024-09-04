#!/bin/bash

# conferindo se branch main existe, se nao, cria
git pull --rebase origin main
git checkout -b main || git checkout main
# Configurar usuário e e-mail do Git
git pull --rebase origin main
git add ./teste_scripts/teste.py
git commit -m "Correction commit"
git push origin main

mv /tmp/package-lock.json /tmp/package.json .