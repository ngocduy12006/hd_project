pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building Docker image for Vietnam App...'
                sh 'docker build -t vietnamapp:${BUILD_NUMBER} .'
            }
        }
    }
}