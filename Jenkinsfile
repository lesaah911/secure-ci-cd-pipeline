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
        stage('Scan image') {
            steps {
                sh 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image secure-app:${BUILD_NUMBER}'
            }
        }
    }
}