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
                sh 'docker run --rm \
             -e SECRET_KEY=mysecretkey \
             -e ADMIN_USERNAME=admin \
             -e ADMIN_PASSWORD=admin123 \
             vietnamapp:${BUILD_NUMBER} python -m pytest'
            }
        }

        stage('Quality'){
            steps {
                echo 'Evaluating Code Quality...'
                sh 'docker run --rm vietnamapp:${BUILD_NUMBER} python -m flake8 vietnam.py test'
            }
        }

        stage('Security'){
            steps {
                echo 'Testing Security...'
                sh 'docker run --rm vietnamapp:${BUILD_NUMBER} python -m bandit -r . -x ./test,./tests,./venv,./.venv'
            }
        }

        stage('Deploy') {
        steps {
        sh '''
            docker stop vietnam-container || true
            docker rm vietnam-container || true

            docker run -d \
            --name vietnam-container \
            -p 5001:5000 \
            -e SECRET_KEY=mysecretkey \
            -e ADMIN_USERNAME=admin \
            -e ADMIN_PASSWORD=admin123 \
            vietnam:${BUILD_NUMBER}
        '''
        }
        }
    }
}