#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Create tables
python -c "from app.database import engine, Base; from app.models import Question, Company, Topic; Base.metadata.create_all(bind=engine)"
