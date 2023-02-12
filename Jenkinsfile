pipeline {
   agent { 
    any {
         image 'python-agent' args '/bin/bash' 
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
                 sh 'python create_vip.py service1'
            }
        }
        
        stage('Post_test') {
            steps {
                echo 'Running post-test...'
            }
        }
    }
}
