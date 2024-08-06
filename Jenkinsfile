pipeline {
    agent any
    
    stages {
        stage('Realizando a autentiação no Git') {
            steps {
                script {
                    git credentialsId: 'log-token-git',
                        url: 'https://github.com/Ronynetwork/AVSAC.git',
                        branch: 'main'
                }
            }
        }
        stage('Instalação do Docker') {
            steps {
                script {
                    echo 'chmod +x ./Estrutura/docker_setup.sh'
                    echo './Estrutura/docker_setup.sh'
                }
            }
        }
        stage('Configuração do SonarQube') {
            steps {
                script{
                    echo "realizando build do SonarQube"
                    echo "docker compose -f Estrutra/docker-compose-sonar.yml up -d"
                }
            }
        }
    }
}