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
            sleep 2

            docker exec vietnam-container python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/', timeout=5); print('Deployment check passed')"
         '''
        }
    }

    stage('Release') {
    steps {
        withCredentials([string(credentialsId: 'github-api-token', variable: 'GITHUB_TOKEN')]) {
            sh '''
                set -e

                RELEASE_VERSION="v1.0.${BUILD_NUMBER}"
                COMMIT_HASH=$(git rev-parse --short HEAD)

                git config user.name "Jenkins CI"
                git config user.email "jenkins@example.com"

                echo "Creating Git tag: ${RELEASE_VERSION}"

                git tag -a "${RELEASE_VERSION}" -m "Release ${RELEASE_VERSION}"

                git push https://x-access-token:${GITHUB_TOKEN}@github.com/ngocduy12006/hd_project.git "${RELEASE_VERSION}"

                echo "Created release tag: ${RELEASE_VERSION}"

                echo "Creating GitHub Release: ${RELEASE_VERSION}"

                curl -sS -L -X POST \
                  -H "Accept: application/vnd.github+json" \
                  -H "Authorization: Bearer ${GITHUB_TOKEN}" \
                  -H "X-GitHub-Api-Version: 2022-11-28" \
                  https://api.github.com/repos/ngocduy12006/hd_project/releases \
                  -d "{
                    \\"tag_name\\": \\"${RELEASE_VERSION}\\",
                    \\"name\\": \\"Release ${RELEASE_VERSION}\\",
                    \\"body\\": \\"Automated release created by Jenkins after successful deployment. Build number: ${BUILD_NUMBER}. Commit: ${COMMIT_HASH}.\\",
                    \\"draft\\": false,
                    \\"prerelease\\": false
                  }"

                echo "GitHub Release created successfully: ${RELEASE_VERSION}"
            '''
        }
    }
}
   
    }

}