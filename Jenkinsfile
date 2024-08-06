pipeline {
    agent any
    
    stages {
        stage('Realizando a autentiação no Git') {
            steps {
                script {
                    git credentialsId: 'log-token-git',
                        url: 'https://github.com/Ronynetwork/Project.git',
                        branch: 'main'
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