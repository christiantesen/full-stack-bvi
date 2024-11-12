#INIT
- cd backend
IN BACKEND
- python -m venv .venv
LINUX -BASH
- source .venv/bin/activate
WINDOWS -BASH
- source .venv/Scripts/activate
#INSTALL
IN .VENV
- pip install -r requirements.txt
#DEPLOY
EXECUTE -DEV
- uvicorn main:app --reload
EXECUTO -PROD
- uvicorn main:app --PORT