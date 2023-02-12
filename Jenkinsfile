pipeline {
    agent {
        docker {
            image 'python:3.9'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    stages {
        stage('Build') {
            steps {
                echo 'Building the project...'
            }
        }
        
        stage('Pre-test') {
            steps {
                echo 'Running pre-test...'
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Deploying the application...'
            }
        }
        
        stage('Post_test') {
            steps {
                echo 'Running post-test...'
            }
        }
    }
}
