1. Prepare the Environment
- Create a project folder /admissions_prediction.
- Place your bento_image.tar in this folder.
- Open the folder in VSCode to simplify terminal management.

2. Set Up the Python Environment
- Use mamba or conda to create and activate a Python 3.9 virtual environment:
    mamba create -n bentoml-env python=3.9
    mamba activate bentoml-env

3. Load and Run the Docker Image
- Load the BentoML Docker image:
    docker load < bento_image.tar

- Run the Docker container to serve the BentoML API on port 3000:
    docker run --rm -p 3000:3000 lam_paturle_gbr_service:latest

- Confirm the service is running by visiting the Swagger UI at:
    http://localhost:3000
    
4. Run Tests in a Separate Container
- Open a second terminal in the project folder.
- Activate the same virtual environment:
    mamba activate bentoml-env

- Launch an interactive container with access to the service running on localhost:3000:
    docker run --rm --network="host" -it lam_paturle_gbr_service:latest bash

- Inside the interactive container, run your tests:
    pytest

- Exit the interactive container after the tests are complete:
    exit

5. Stop the Service
- End the service running in the first terminal with
    ^C

Troubleshooting Commands
- Check Activity on Port 3000:
    lsof -i :3000

- Stop a Stuck Docker Container:
    docker ps  # Find the container ID
    docker stop <container_id>
