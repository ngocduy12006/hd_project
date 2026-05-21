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
            docker compose -p vietnam-staging down || true
            docker compose -p vietnam-staging up -d

            echo "Checking container status..."
            docker ps -a

            echo "Checking container logs..."
            docker logs vietnam-container || true

            echo "Waiting for app to start..."
            sleep 8

            docker exec vietnam-container python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/', timeout=5); print('Deployment check passed')"
        '''
    }
}

        
    }
}