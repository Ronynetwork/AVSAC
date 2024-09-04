#!/bin/bash

mv package-lock.json package.json /tmp/
# conferindo se branch main existe, se nao, cria
git pull --rebase origin main
git checkout -b main || git checkout main
# Configurar usuário e e-mail do Git
git pull --rebase origin main
git add ./test_scripts/teste.py
git commit -m "Correction commit"
git push origin main

mv /tmp/package-lock.json /tmp/package.json .