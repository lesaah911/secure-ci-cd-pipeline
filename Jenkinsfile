pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t secure-app:${BUILD_NUMBER} .'
            }
        }
    }
}