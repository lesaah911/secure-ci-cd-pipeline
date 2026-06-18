pipeline {
    agent any
    stages {
        stage('Scan secrets') {
            steps {
                sh 'docker run --rm -v $(pwd):/repo zricethezav/gitleaks:latest detect --source=/repo --no-banner'
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t secure-app:${BUILD_NUMBER} .'
            }
        }
    }
}