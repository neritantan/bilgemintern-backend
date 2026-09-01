@Library('bilgemintern') _

pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                hello('backend')

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
                    env.HASH = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                }

                withCredentials([usernamePassword(credentialsId: 'ghcr-login', passwordVariable: 'GHCR_PAT', usernameVariable: 'GHCR_USER')]) {
                    sh 'echo $GHCR_PAT | docker login ghcr.io -u $GHCR_USER --password-stdin'

                    script {
                        def img = "ghcr.io/${env.GHCR_USER}/bilgemintern-backend:${env.HASH}"

                        if (sh(script: "docker manifest inspect ${img} > /dev/null 2>&1", returnStatus: true) != 0) {
                            sh "docker tag bilgemintern-backend:latest ${img}"
                            sh "docker push ${img}"
                        }
                        else {
                            echo "Image ${img} already exists in GHCR. Skipping push."
                        }
                    }
                }

                sh 'echo "Pushed to GHCR successfully."'
            }
        }

        stage('Deploy') {
            steps {
                // SSH to the dev server and deploy the application.
                sh 'echo "Deploying to dev server..."'

                script {
                    withCredentials([
                        sshUserPrivateKey(credentialsId: 'server-ssh', keyFileVariable: 'SSH_KEY', usernameVariable: 'SSH_USER'),
                    ]) {

                        sh """
                        ssh -i \$SSH_KEY -o StrictHostKeyChecking=no \$SSH_USER@dev '
                            docker stop app || true
                            docker rm app || true
                            docker pull ghcr.io/neritantan/bilgemintern-backend:${env.HASH}
                            docker run -d --name app -p 80:8000 ghcr.io/neritantan/bilgemintern-backend:${env.HASH}
                            docker image prune -a -f --filter "until=24h"
                        '
                        """
                    }
                }
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
