def frontendImage="${DOCKERHUB}/frontend"
def backendImage="${DOCKERHUB}/backend"
def backendDockerTag=""
def frontendDockerTag=""
def dockerRegistry=""
def registryCredentials="dockerhub"


pipeline {
    agent {
        label 'agent'
    }
    
    tools {
        terraform 'Terraform'
    }

    parameters {
        string(name: 'backendDockerTag', defaultValue: '', description: 'Backend docker image tag')
        string(name: 'frontendDockerTag', defaultValue: '', description: 'Frontend docker image tag')
    }

    stages {
        stage('Get Code') {
            steps {
                checkout scm // Get some code from a GitHub repository
            }
        }

        stage('Clean running containers') {
            steps {
                sh "docker rm -f frontend backend"
            }
        }
        
        stage('Adjust version') {
            steps {
                script{
                    backendDockerTag = params.backendDockerTag.isEmpty() ? "latest" : params.backendDockerTag
                    frontendDockerTag = params.frontendDockerTag.isEmpty() ? "latest" : params.frontendDockerTag
                    
                    currentBuild.description = "Backend: ${backendDockerTag}, Frontend: ${frontendDockerTag}"
                }
            }
        }

        stage('Deploy application') {
            steps {
                script {
                    withEnv(["FRONTEND_IMAGE=$frontendImage:$frontendDockerTag", 
                             "BACKEND_IMAGE=$backendImage:$backendDockerTag"]) {
                       docker.withRegistry("$dockerRegistry", "$registryCredentials") {
                            sh "docker-compose up -d"
                        }
                    }
                }
            }
        }

        stage('Selenium tests') {
            steps {
                sh "pip3 install -r test/selenium/requirements.txt"
                sh "python3 -m pytest test/selenium/frontendTest.py"
            }
        }

        stage('Run terraform') {
            steps {
                dir('Terraform') {                
                    git branch: 'main', url: 'https://github.com/Panda-Academy-Workshops/Terraform'
                    withAWS(credentials:'aws', region: 'us-east-1') {
                        sh "terraform init -backend-config=bucket=${BUCKET} && terraform apply -auto-approve -var bucket_name=${BUCKET}"
                    } 
                }
            }
        }
        stage('Run Ansible') {
               steps {
                   script {
                        sh "ansible-galaxy install -r requirements.yml"
                        withEnv(["FRONTEND_IMAGE=$frontendImage:$frontendDockerTag", 
                                 "BACKEND_IMAGE=$backendImage:$backendDockerTag"]) {
                            ansiblePlaybook inventory: 'inventory', playbook: 'playbook.yml'
                        }
                   }
               }
            }
        stage('Show terraform output') {
            steps {
                dir('Terraform') {                
                    withAWS(credentials:'aws', region: 'us-east-1') {
                            echo '###########################\n\n LOAD BALANCER ADRESS \n\n###########################'
                            sh 'terraform output'
                            echo '###########################\n###########################'
                    } 
                }
            }
        }
        }
    post {
        always {
            sh "docker-compose down"
            cleanWs()
        }
    }
}
