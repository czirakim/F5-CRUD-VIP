pipeline {
  agent any
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
        sh 'python3 create_profiles.py service1'
      }
    }

    stage('Post_test') {
      steps {
        echo 'Running post-test...'
      }
    }

  }
}