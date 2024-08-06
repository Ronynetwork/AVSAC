#!/bin/bash

# Atualiza a lista de pacotes e instala dependências necessárias
sudo apt-get update
sudo apt-get install -y ca-certificates curl

# Cria o diretório para armazenar a chave GPG do Docker
sudo install -m 0755 -d /etc/apt/keyrings

# Baixa a chave GPG do Docker e altera as permissões
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Adiciona o repositório Docker às fontes do Apt
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo \"$VERSION_CODENAME\") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Atualiza a lista de pacotes
sudo apt-get update

# Define a versão do Docker a ser instalada
VERSION_STRING=5:27.1.0-1~ubuntu.24.04~noble

# Instala o Docker e plugins
sudo apt-get install -y docker-ce=$VERSION_STRING docker-ce-cli=$VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin

# Executa o Docker Compose
docker compose -f /caminho/para/seu/docker-compose.yml up -d
