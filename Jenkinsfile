pipeline {
   agent {
        docker {
            image 'python'
            registryUrl 'https://registry.hub.docker.com'
            args '--network host -u root:root'
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
