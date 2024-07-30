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
    }
}