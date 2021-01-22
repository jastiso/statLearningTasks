ENV_NAME=psiturk
conda env remove -n ${ENV_NAME}
conda env create -f environment.yml 
