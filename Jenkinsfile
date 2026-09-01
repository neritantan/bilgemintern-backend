@Library('bilgemintern') _

pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t bilgemintern-backend:latest .'
                // docker run
                sh 'docker run -d --name app -p 8000:8000 bilgemintern-backend:latest'
            }
        }
        stage('Test') {
            steps {
                // Run required tests to verify the application is working.
                sh 'sleep 30' // Wait for the application to start
                withCredentials([string(credentialsId: 'host-ip', variable: 'HOST_IP')]) {
                    sh 'curl -f $HOST_IP:8000'
                }
            }
        }

        stage('Push') {
            steps {
                script {
                    env.HASH = shortHash()
                    pushToGhcr(image: 'bilgemintern-backend', tag: env.HASH)
                }
            }
        }
        stage('Deploy') {
            steps {
                deployToDev()
            }
        }
    }
    post {
        always {
            sh 'docker stop app || true'
            sh 'docker rm app || true'
            sh 'docker rmi bilgemintern-backend:latest || true'
        }
        cleanup {
            cleanWs()
        }
    }
}
