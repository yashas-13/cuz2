#!/bin/bash
set -e

# install backend dependencies
pip install -r backend/requirements.txt

# install frontend dependencies
npm install

# start backend server in background
python backend/run.py &
BACK_PID=$!

# serve frontend using python http server
cd frontend
python -m http.server 8000 &
FRONT_PID=$!
cd ..

# display registration page URL
echo "Backend running at http://localhost:5000"
echo "Open http://localhost:8000/pages/register.html to register a manufacturer account"

# wait for background processes
wait $BACK_PID $FRONT_PID
