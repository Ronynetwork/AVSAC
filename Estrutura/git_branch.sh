#!/bin/bash

# Conferindo se a branch main existe, se não, cria
git reset --hard
git pull
git checkout -b main || git checkout main

# Restaurar todos os arquivos modificados para o estado do último commit
git restore --staged .
git restore .

# Limpar arquivos não rastreados
git clean -fd

# Configurar usuário e e-mail do Git
# (certifique-se de que essas configurações já estão feitas globalmente ou localmente)

# Adicionar apenas o arquivo desejado
git add ./teste_scripts/teste.py

# Fazer o commit com uma mensagem
git commit -m "Correction commit"

# Enviar as mudanças para o repositório remoto
git push origin main
