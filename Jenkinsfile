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
                    sh 'chmod +x ./Estrutura/docker_setup.sh'
                    sh './Estrutura/docker_setup.sh'
                }
            }
        }
        stage('Configuração do SonarQube') {
            steps {
                script {
                    def sonarContainerName = sh(script: 'docker ps --filter "name=sonarqube" --format "{{.Names}}"', returnStdout: true).trim()
                    echo "${sonarContainerName}"
                    if (sonarContainerName) {
                        echo "O serviço SonarQube já está em execução, reiniciando o contêiner."
                        sh "docker restart sonarqube" // Reiniciar o contêiner se estiver em execução
                    } 
                    else {
                        echo "Realizando build do SonarQube"
                        sh 'docker compose -f Estrutura/docker-compose-sonar.yml up -d'
                    }
                }
            }
        }
        stage('Delay') {
            steps {
                script {
                    echo 'Aguardando 40 segundos para a inicialização completa do SonarQube...'
                    sleep time:40, unit: 'SECONDS'
                }
            }
        }
        stage('Análise do Código') {
            steps {
                script {
                    // Defina o caminho completo para o sonar-scanner
                    def scannerHome = tool 'sonar-scanner';
                    
                    // Obtendo as configurações do SonarQube definidas no Jenkins pelo SonarQube Servers
                    withSonarQubeEnv('AVSAC') {
                        // Exportando SONAR_CONFIG_NAME e SONAR_URL como variáveis de ambiente
                        env.SONAR_PROJECT_KEY = "${SONAR_CONFIG_NAME}"
                        env.SONAR_URL = "${SONAR_HOST_URL}"

                        // Executando a análise do código sem especificar sonar.sources
                        sh """
                        ${scannerHome}/bin/sonar-scanner \
                        -Dsonar.sources=./teste_scripts/ \
                        -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                        -Dsonar.host.url=${SONAR_URL} \
                        -Dsonar.login=${SONAR_AUTH_TOKEN} 
                        """
                    }
                }              
            }
        }
        stage('Quality Gate') {
            steps{
                waitForQualityGate abortPipeline: false
            }
        }
        stage('Notification in jenkins') {
            steps {
                sh 'chmod +x ./Estrutura/notification/script_notification.py'
                sh 'python3 ./Estrutura/notification/script_notification.py'
                
                publishHTML(target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'Estrutura/notification',
                    reportFiles: 'sonarqube-notification.html',
                    reportName: 'SonarQube Notification'
                ])
            }
        }
        stage('subindo ngnix com o index da pagina analisada'){
            steps{
                script{
                    def ngnixContainerName = sh(script: 'docker ps --filter "name=ngnix-app" --format "{{.Names}}"', returnStdout: true)
                    if (ngnixContainerExists) {
                        echo "O serviço Nginx já está em execução, reiniciando o contêiner."
                        sh "docker restart ngnix-app" // Reiniciar o contêiner se estiver em execução
                    } 
                    else {
                        echo "Realizando build do Nginx"
                        sh 'docker compose -f ./Estrutura/docker-compose-ngnix.yml up -d'
                    }
                }
            }
        }
    }
}
