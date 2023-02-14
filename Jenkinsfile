pipeline {
  agent any
  parameters {
    string(name: 'service', defaultValue: 'default_value', description: 'service parameter')
        }
  stages {
    stage('Build') {
      steps {
        script {
          withCredentials([string(credentialsId: 'Authorization_string', variable: 'Authorization_string')]) {
            env.Authorization_string = "${Authorization_string}"
                    }
                }
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
        sh 'python3 $WORKSPACE/create_vip.py ${service} 2>&1'
      }
    }

    stage('Post_test') {
      steps {
        echo 'Running post-test...'
      }
    }

  }
}