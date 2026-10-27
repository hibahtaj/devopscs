pipeline {
    agent any
    environment {
        IMAGE_NAME = 'YOUR_DOCKERHUB_USERNAME/quickbite'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build Docker Image') {
            steps { sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .' }
        }
        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                          docker push "$IMAGE_NAME:$IMAGE_TAG"
                          docker logout'''
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                sh '''sed "s|DOCKER_IMAGE_PLACEHOLDER|$IMAGE_NAME:$IMAGE_TAG|g" k8s/deployment.yaml | kubectl apply -f -
                      kubectl apply -f k8s/service.yaml
                      kubectl rollout status deployment/quickbite --timeout=120s'''
            }
        }
    }
}
