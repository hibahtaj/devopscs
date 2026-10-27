pipeline {
    agent any

    environment {
        PATH = "/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin:${env.PATH}"
        IMAGE_NAME = 'hibahtaj/quickbite'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push "$IMAGE_NAME:$IMAGE_TAG"
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl set image deployment/quickbite-deployment \
                    quickbite-container=$IMAGE_NAME:$IMAGE_TAG

                    kubectl rollout status deployment/quickbite-deployment --timeout=180s
                '''
            }
        }
    }

    post {
        success {
            echo 'QuickBite CI/CD Pipeline Completed Successfully!'
        }

        failure {
            echo 'QuickBite CI/CD Pipeline Failed!'
        }
    }
}
