pipeline {
    agent any
    stages {
        stage('Scan secrets') {
            steps {
                sh 'docker run --rm -v dockersproject_jenkins_home:/data zricethezav/gitleaks:latest detect --source=/data/workspace/secure-ci-cd-pipeline --no-banner'
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t secure-app:${BUILD_NUMBER} .'
            }
        }
    }
}