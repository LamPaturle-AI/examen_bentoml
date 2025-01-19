# Create and launch virtual environment
mamba create -n bentomlexam python=3.9
mamba activate bentomlexam

# Change directory and download raw data
cd /users/lampaturle/Desktop/SWITCH_PROJECT/Datascientest/examen_bentoml/data/raw
wget https://assets-datascientest.s3.eu-west-1.amazonaws.com/MLOPS/bentoml/admission.csv

# Change directory to examen_bentoml
cd /users/lampaturle/Desktop/SWITCH_PROJECT/Datascientest/examen_bentoml/

# Install libraries
pip install pandas
pip install scikit-learn
pip install bentoml
pip install pyjwt
pip install pytest
pip install requests

# Create tests folders
mkdir tests

# Prepare data
python src/prepare_data.py

# Train and evaluate model
python src/train_model.py

# Show list of models to verify Model(tag="admissions_gbr:xuk3plgvh26gdvrd") has been saved
bentoml models list

# load model
# bentoml models pull admissions_gbr:latest
# bentoml models get admissions_gbr:latest

# Change directory
cd src

# Start service
bentoml serve service.py:gbr_service --reload

# Test service (in another terminal)
mamba activate bentomlexam
cd /users/lampaturle/Desktop/SWITCH_PROJECT/Datascientest/examen_bentoml/
pytest tests/

# Create bento
bentoml build

# Verify bento creation
bentoml list

# Create Docker image
bentoml containerize gbr_service:yphqrhgvrwlgfvrd -t lam_paturle_gbr_service:latest

# Verify image name
docker images

# Test image
docker run --rm -p 3000:3000 lam_paturle_gbr_service:latest

docker run -it lam_paturle_gbr_service:latest bash

# Compress Docker image
docker save -o ./deliverables/bento_image.tar lam_paturle_gbr_service:latest

# Test service
bentoml serve path_to_your_script.py