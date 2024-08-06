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