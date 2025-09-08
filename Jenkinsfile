pipeline {
  agent any

  options {
    timestamps()
    ansiColor('xterm')
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Setup Python') {
      steps {
        sh '''
          python3 -V || true
          python3 -m venv .venv
          . .venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
        '''
      }
    }

    stage('Tests (parallel)') {
      parallel {
        stage('Unit & Smoke') {
          steps {
            sh '. .venv/bin/activate && pytest tests/unit -n auto --junitxml=test-results/unit.xml --cov=app --cov-report=xml --cov-report=html --cov-fail-under=80'
          }
          post {
            always {
              junit 'test-results/unit.xml'
              archiveArtifacts artifacts: 'coverage.xml, htmlcov/**', allowEmptyArchive: true
            }
          }
        }
        stage('Integration') {
          steps {
            sh '. .venv/bin/activate && pytest -m "integration" -n auto --junitxml=test-results/integration.xml'
          }
          post { always { junit 'test-results/integration.xml' } }
        }
        stage('Regression') {
          steps {
            sh '. .venv/bin/activate && pytest -m "regression" -n auto --junitxml=test-results/regression.xml'
          }
          post { always { junit 'test-results/regression.xml' } }
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        sh 'docker build -t ci-cd-regression:${BUILD_NUMBER} .'
      }
    }
  }
  post {
    always {
      archiveArtifacts artifacts: 'test-results/*.xml', allowEmptyArchive: true
    }
  }
}
