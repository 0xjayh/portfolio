# Samuel Ojayhagbega — Portfolio Web App
## Setup Guide

---

## Project Structure

portfolio-webapp/
├── index.html                  <- Public portfolio
├── admin/
│   ├── index.html              <- Admin CMS panel
│   └── .htaccess               <- Apache password protection (server only)
├── api/
│   ├── app.py                  <- Flask REST API + frontend routes
│   ├── db.py                   <- MySQL connection
│   ├── passenger_wsgi.py       <- cPanel Passenger entry point
│   ├── schema.sql              <- Run once in phpMyAdmin
│   └── .env.example            <- Copy to .env and fill in credentials
│   └── .env                    <- YOUR credentials (never committed)
├── requirements.txt            <- Python dependencies
├── run.py                      <- Local dev server
├── .gitignore
└── .github/
    └── workflows/
        └── deploy.yml          <- GitHub Actions CI/CD

---

## LOCAL DEVELOPMENT

### Step 1 — Create and activate virtual environment

Mac/Linux:
    python3 -m venv venv
    source venv/bin/activate

Windows:
    python -m venv venv
    venv\Scripts\activate

You should see (venv) in your terminal prompt.

### Step 2 — Install dependencies

    pip install -r requirements.txt

No --break-system-packages needed — the venv is isolated.

### Step 3 — Create your .env file

    cp api/.env.example api/.env

Open api/.env and fill in your local MySQL credentials:

    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=your_local_mysql_password
    DB_NAME=portfolio

### Step 4 — Set up local MySQL

In MySQL run:
    CREATE DATABASE portfolio;

Then in phpMyAdmin or MySQL CLI, run api/schema.sql to create tables.

### Step 5 — Run the app

    python run.py

Visit:
    http://localhost:5000        -> public portfolio
    http://localhost:5000/admin  -> admin panel
    http://localhost:5000/api/health

### To deactivate the virtual environment when done:

    deactivate

---

## SERVER DEPLOYMENT (Truehost cPanel)

### Step 1 — MySQL Database
1. cPanel -> MySQL Databases -> create database and user
2. phpMyAdmin -> run api/schema.sql

### Step 2 — Upload files
Push via GitHub Actions (see below) or upload manually via File Manager.

### Step 3 — Create .env on the server
In File Manager, create api/.env with your server DB credentials.
Never upload your local .env — create it directly on the server.

### Step 4 — Python App in cPanel
1. cPanel -> Setup Python App -> Create Application
2. Application root: public_html/api
3. Application URL: yourdomain.com/api
4. Startup file: passenger_wsgi.py
5. Run pip install from the cPanel Python App interface

### Step 5 — Admin password protection
In cPanel Terminal:
    htpasswd -c /home/YOURUSERNAME/.htpasswd samuel

Update admin/.htaccess:
    AuthUserFile /home/YOURUSERNAME/.htpasswd

---

## GITHUB CI/CD

1. Create a private GitHub repo
2. Push this project:
    git init
    git add .
    git commit -m "Initial deploy"
    git branch -M main
    git remote add origin https://github.com/YOU/portfolio.git
    git push -u origin main

3. Add secrets in repo -> Settings -> Secrets -> Actions:
    FTP_SERVER    -> ftp.yourdomain.com
    FTP_USERNAME  -> your FTP username
    FTP_PASSWORD  -> your FTP password

4. Every git push to main auto-deploys to your server.
   api/.env is excluded — it stays on the server only.

---

## DAILY CONTENT WORKFLOW

Design/code changes -> git push -> auto-deployed in ~30 seconds
Content changes     -> log into yourdomain.com/admin -> save instantly
