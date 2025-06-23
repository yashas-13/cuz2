#!/bin/bash
set -e

# install backend dependencies
pip install -r backend/requirements.txt

# install frontend dependencies
npm install

# start backend server (also serves frontend) in background
python backend/run.py &
BACK_PID=$!

# display registration page URL
echo "Server running at http://localhost:5000"
echo "Open http://localhost:5000/pages/register.html to register a manufacturer account"

# wait for the server process
wait $BACK_PID
