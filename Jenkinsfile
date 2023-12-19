pipeline {
  agent any
  stages {
    stage('Install Python') {
      steps {
        sh '''apt-get update
apt install python3'''
      }
    }

    stage('Required') {
      steps {
        sh '''python -m pip install --upgrade pip
'''
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