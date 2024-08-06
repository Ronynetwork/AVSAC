pipeline {
    agent any
    
    stages {
        stage('Realizando a autentiação no Git') {
            steps {
                script {
                    def destinationDir= 'AVSAC'
                    git credentialsId: 'log-token-git',
                        url: 'https://github.com/Ronynetwork/AVSAC.git',
                        branch: 'main'
                        directory: destinationDir
                }
            }
        }
        stage('Instalação do Docker') {
            steps {
                script {
                    sh 'chmod +x ./Estrutura/docker_setup.sh'
                    sh './Estrutura/docker_setup.sh'
                }
            }
        }
        stage('Configuração do SonarQube') {
            steps {
                script {
                    def sonarContainerExists = sh(script: 'docker ps --filter "name=sonarqube" --format "{{.Names}}"', returnStatus: true)
                    if (sonarContainerExists == 1) {
                        echo "O serviço SonarQube já está em execução, reiniciando o contêiner."
                        sh "docker restart sonarqube" // Reiniciar o contêiner se estiver em execução
                    } 
                    else {
                        echo "Realizando build do SonarQube"
                        sh 'docker compose -f Estrutura/docker-compose-sonar-testes.yml up -d'
                    }
                }
            }
        }
    }
}