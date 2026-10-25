
pipeline {
    agent any

    parameters {
        choice(
            name: 'VERSION',
            choices: ['v1', 'v2', 'v3'],
            description: 'Select Password Manager version'
        )
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Nirmal-Priya/password-manager-24MIS0552.git'

                bat """
                    git fetch --tags --force
                    git checkout -f tags/${params.VERSION}
                """
            }
        }

        stage('Build') {
            steps {
                bat '''
                    python --version
                    python -m pip install -r requirements.txt
                    python -m py_compile app.py
                '''
            }
        }
    }

    post {
        success {
            echo 'Password Manager Jenkins Build Successful!'
        }

        failure {
            echo 'Password Manager Jenkins Build Failed!'
        }
    }
}
