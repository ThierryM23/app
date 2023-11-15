.venv\Scripts\Activate

set FLASK_APP=app.py
$env:FLASK_APP = "app.py"
cd www
flask run --debug --reload