# CSV_Report_Processing

To run this program you should create your own virtual environment.

Firstly, clone repository to the destination folder on your local machine.

Next, create virtual environemt using pip in your destination
```
python3 -m venv /path/to/cloned/repository/venv
```
Launch virtual environment by accessing activate.bat 
```
cd path/to/cloned/repository
cd venv/Scripts
activate.bat
```
Be sure to have rounded brackets. It indicates that you have launched virtual environment.

Go back to main folder and install required packages from requirements.txt:
```
cd..
cd..
pip install -r requirements.txt
```
To check if you have properly installed packages to your virtual environemt, write
```
pip freeze
```
and then check content with requrements.txt file

Now you can launch program by writing
```
python filtering_csv.py
```
To launch tests write
```
pytest -v
```
