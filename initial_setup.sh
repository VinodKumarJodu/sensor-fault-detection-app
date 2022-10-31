echo [$(date)]: "START"
echo [$(date)]: "Creating conda env with python 3.8"
conda create -p venv python=3.8 -y
echo [$(date)]: "activate env"
source activate ./venv
echo [$(date)]: "Running setup.py"
python setup.py install
echo [$(date)]: "Completed running setup.py"
echo [$(date)]: "intalling dev requirements"
pip install -r requirements_dev.txt
echo [$(date)]: "Setting Environment Variables for MONGO_DB_URL"
export MONGO_DB_URL="mongodb+srv://vinodkumarjodu:vinodkumarjodu@cluster0.iw6azf8.mongodb.net/?retryWrites=true&w=majority"
echo [$(date)]: "END"