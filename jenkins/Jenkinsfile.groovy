pipeline {
    agent any  // Use any available Jenkins agent

    environment {
        DOCKER_IMAGE = 'my-python-app'  // Docker image name
        DOCKER_TAG = 'latest'           // Image tag
        DOCKERFILE_PATH = 'docker/Dockerfile'  // Path to the Dockerfile
        BUILD_CONTEXT = '.'  // The build context (root of the repository)

        DOCKER_REGISTRY = 'docker.io'   // Optional: Docker registry URL (if pushing to remote)
        DOCKER_CREDENTIALS = 'docker-credentials' // Jenkins credential ID for Docker registry
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from your Git repository
                git branch: 'main', url: 'https://github.com/hkvoluntary/cicd_docker.git'
            }
        }

        stage('Input for Build Type') {
            steps {
                script {
                    // Prompt the user to select the build target (Development or Production)
                    def userInput = input(
                        message: 'Select the Build Type',
                        parameters: [
                            choice(name: 'BUILD_TYPE', choices: ['development', 'production'], description: 'Select the environment to build.')
                        ]
                    )
                    
                    // Set the build type based on user input
                    env.BUILD_TYPE = userInput
                }
            }
        }

        //stage('Build Docker Image') {
        //    steps {
        //        script {
                    // Build the Docker image using the user-selected build type (development or production)
        //            echo "Building Docker image for ${env.BUILD_TYPE} environment"

                    // Use the selected build target (development or production)
        //            sh """
        //                docker build --target ${env.BUILD_TYPE} -t ${DOCKER_IMAGE}:${DOCKER_TAG} -f ${DOCKERFILE_PATH} ${BUILD_CONTEXT}
        //            """
        //        }
        //    }
        //}

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image using the user-selected build type (development or production)
                    echo "Building Docker image for ${env.BUILD_TYPE} environment"
                    // Build Docker image                    
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}","--target ${env.BUILD_TYPE} -f ${DOCKERFILE_PATH} ${BUILD_CONTEXT}")

                    
                    //docker.build("--target ${env.BUILD_TARGET} ${DOCKER_IMAGE}:${DOCKER_TAG} -f ${DOCKERFILE_PATH}")
                }
            }
        }
    }
    

    post {
        always {
            // Always run this section to clean up or notify
            echo 'Pipeline finished.'
        }
        success {
            echo 'Build and Docker image creation succeeded.'
        }
        failure {
            echo 'Pipeline failed. Investigate the error.'
        }
    }
}