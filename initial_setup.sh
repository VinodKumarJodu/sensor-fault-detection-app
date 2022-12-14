echo [$(date)]: "Upgrading Pip"
pip3 install --upgrade pip setuptools==60.10.0
echo [$(date)]: "Configuring Github with VS Code :: START"
git config --global user.name "VinodKumarJodu"
git config --global user.email "vinodkumarjodu@gmail.com"
echo [$(date)]: "Configuring Github with VS Code :: END"
echo [$(date)]: "Environment Variables Setup :: START"
export MONGO_DB_URL="mongodb+srv://vinodkumarjodu:vinodkumarjodu@cluster0.iw6azf8.mongodb.net/?retryWrites=true&w=majority"
echo [$(date)]: "Environment Variables Setup :: END"