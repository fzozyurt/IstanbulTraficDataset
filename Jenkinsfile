pipeline {
  agent any
  stages {
    stage('Install Python') {
      steps {
        sh '''apt-get update
apt install python3 -y'''
      }
    }

    stage('Required') {
      steps {
        sh 'pip install -r requirements.txt'
      }
    }

    stage('Start Script') {
      steps {
        sh 'python Scripts/main.py'
      }
    }

  }
}