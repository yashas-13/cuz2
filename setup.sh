#!/bin/bash
# Simple setup script to install dependencies and run the backend and frontend.

set -e

# create python virtual environment if not exists
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate

pip install --upgrade pip
pip install -r backend/requirements.txt

# run backend
python backend/run.py &
BACKEND_PID=$!

# give the backend a moment to start
sleep 2

# serve frontend
(cd frontend && python -m http.server 8000 &) 
FRONTEND_PID=$!

echo "Backend running at http://localhost:5000" 
echo "Registration page at http://localhost:8000/pages/register.html" 

# wait for user to stop
read -p "Press enter to stop servers" _
kill $BACKEND_PID $FRONTEND_PID
