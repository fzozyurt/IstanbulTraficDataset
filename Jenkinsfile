pipeline {
  agent any
  stages {
    stage('Install Python') {
      steps {
        sh '''apt-get update
apt install python3 -y
apt install python3-pip -y'''
      }
    }

    stage('Required') {
      steps {
        sh 'pip3 install -r requirements.txt'
      }
    }

    stage('Start Script') {
      steps {
        sh 'python Scripts/main.py'
      }
    }

  }
}