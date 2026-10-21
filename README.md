# SOC Incident Manager

A lightweight Security Operations Center incident-management application built with Python, Flask, and SQLite.

The application provides a simple workflow for registering, investigating, tracking, and closing cybersecurity incidents.

## Features

* Incident dashboard
* Security incident creation
* Incident severity classification
* Incident categorization
* Alert source tracking
* Analyst assignment
* Investigation notes
* Incident status management
* Persistent SQLite storage
* Incident deletion
* Basic incident statistics
* Responsive dark UI

## Incident Workflow

New
↓
Investigating
↓
Contained
↓
Closed

## Technology Stack

* Python
* Flask
* SQLite
* HTML
* CSS
* Jinja2

## Installation

Clone the repository:

git clone [https://github.com/dmytrooliinyk-cyber/soc-incident-manager.git](https://github.com/dmytrooliinyk-cyber/soc-incident-manager.git)

cd soc-incident-manager

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

..venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Run the application:

python app.py

Then open:

[http://127.0.0.1:5000](http://127.0.0.1:5000)

The SQLite database is created locally when the application starts and is not stored in the repository.

## Project Structure

soc-incident-manager/

app.py
requirements.txt

static/
style.css

templates/
index.html
new_incident.html
incident.html

SECURITY.md
CONTRIBUTING.md
README.md

## Scope

This project is designed as a local portfolio and learning application for practicing security incident tracking and basic SOC workflows.

It is not intended to replace a production incident-response or case-management platform.





