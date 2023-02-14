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
        sh 'python3 $WORKSPACE/Tests/pre_create_test.py ${service} 2>&1'
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
        sh 'python3 $WORKSPACE/Tests/post_create_test.py ${service} 2>&1'
      }
    }
    
    stage('Create graph') {
      steps {
        echo 'Running post-test...'
        sh 'python3 $WORKSPACE/graph.py ${service} 2>&1'
      }
    }

    stage('Publish HTML Report') {
      steps {
        publishHTML(target: [
            allowMissing: false, 
            alwaysLinkToLastBuild: false, 
            keepAll: false, 
            reportDir: '$WORKSPACE', 
            reportFiles: 'edges_${service}.html', 
            reportName: '${service}'
        ])
      }
    }
  }
}