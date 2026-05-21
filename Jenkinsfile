pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building Docker image for Vietnam App...'
                sh 'docker build -t vietnamapp:${BUILD_NUMBER} .'
            }
        }

        stage('Test') {
            steps {
                echo 'Testing Vietnam App...'
                sh 'docker run --rm vietnamapp:${BUILD_NUMBER} python -m pytest'
            }
        }

        stage('Quality'){
            steps {
                echo 'Evaluating Code Quality...'
                sh 'docker run --rm vietnam:${BUILD_NUMBER} python -m flake8 vietnam.py test'
            }
        }
    }
}