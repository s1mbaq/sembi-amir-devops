pipeline {
    agent any
    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
        timeout(time: 15, unit: 'MINUTES')
    }
    environment {
        STUDENT_NAME = 'Amir'
        STUDENT_SURNAME = 'Sembi'
        STUDENT_GROUP = 'IT2-2307'
        STUDENT_ID = '37693'
        IMAGE_NAME = 'sembi-amir-devops'
        CONTAINER_NAME = 'sembi-amir-container'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh '''
                    rm -rf build
                    mkdir -p build
                    git rev-parse HEAD > build/commit.txt
                    cat build/commit.txt
                    printf 'Student: %s %s\nGroup: %s\nStudent ID: %s\n' \
                      "$STUDENT_NAME" "$STUDENT_SURNAME" "$STUDENT_GROUP" "$STUDENT_ID"
                '''
            }
        }
        stage('Build') {
            steps {
                sh '''
                    python3 scripts/validate_personalization.py
                    python3 -m compileall -q app tests
                    printf 'Python bytecode compilation passed.\n' > build/build.txt
                '''
            }
        }
        stage('Test') {
            steps {
                sh '''
                    if python3 -m unittest discover -s tests -v > build/tests.txt 2>&1; then
                        cat build/tests.txt
                    else
                        cat build/tests.txt
                        exit 1
                    fi
                '''
            }
        }
        stage('Docker Build') {
            steps {
                sh '''
                    docker version
                    docker build -t "$IMAGE_NAME:$BUILD_NUMBER" -t "$IMAGE_NAME:latest" .
                    docker image inspect "$IMAGE_NAME:$BUILD_NUMBER" > build/image.txt
                '''
            }
        }
        stage('Docker Run') {
            steps {
                sh '''
                    if docker container inspect "$CONTAINER_NAME" >/dev/null 2>&1; then
                        docker rm -f "$CONTAINER_NAME"
                    fi
                    docker run -d --name "$CONTAINER_NAME" -p 8080:8080 \
                        -e STUDENT_NAME -e STUDENT_SURNAME -e STUDENT_GROUP -e STUDENT_ID \
                        "$IMAGE_NAME:$BUILD_NUMBER"
                    ready=0
                    for attempt in $(seq 1 45); do
                        state=$(docker inspect --format '{{.State.Health.Status}}' "$CONTAINER_NAME")
                        if [ "$state" = healthy ]; then
                            ready=1
                            break
                        fi
                        sleep 1
                    done
                    docker logs "$CONTAINER_NAME"
                    if [ "$ready" -ne 1 ]; then
                        echo 'Container did not become healthy.'
                        exit 1
                    fi
                    docker exec "$CONTAINER_NAME" python -c 'import json,os,urllib.request; data=json.load(urllib.request.urlopen("http://127.0.0.1:8080/api/student",timeout=3)); keys={"name":"STUDENT_NAME","surname":"STUDENT_SURNAME","group":"STUDENT_GROUP","student_id":"STUDENT_ID"}; assert all(data[k]==os.environ[v] for k,v in keys.items()), data; print("HTTP student data verified:",data)'
                    docker ps --filter "name=$CONTAINER_NAME" > build/container.txt
                    cat build/container.txt
                '''
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'build/*.txt', allowEmptyArchive: true
        }
        success {
            echo 'Application deployed and HTTP check passed.'
        }
        failure {
            echo 'Pipeline failed. Open the first failed stage and read its Console Output.'
        }
    }
}
