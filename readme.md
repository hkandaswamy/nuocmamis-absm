![image](https://user-images.githubusercontent.com/77952068/167334431-a61d94c8-aef3-4f08-902f-6f01bcd292fa.png)

## Contributors

- Chon Wa Lam
- Harish Kandaswamy
- Caitlin Phomsopha
- Vanessa Lee
- Daisy Le
- Dominic Nance
- Stephanie Lopez-Bedolla
- Charlie Vue

## Absolute Media Inventory System Upgrade

Absolute Media Inc. (AMI) is a privately-owned media planning and buying company specializing in maximizing the return of their customers' valuable advertising funds. Our client wants a new inventory system that replaces their current one. The new system will reimplement current protocols of their old system (tracking orders of products and issuing packing slips).

The goal of this project is to replace the outdated database with a new system that can be run on modern technology and to be able to access the system with ease.

> The application was built with the following: Front-end: HTML, CSS, JS, Bootstrap | Back-end: REST API: Python Flask, Database: MySQL

## Table of Contents

- [Features](#Features)
- [Setup](#Setup)
- [User Manual](#User-Manual)
- [User Test Report](#User-Test-Report)
- [Maintenance Manual](#Maintenance-Manual)


## Features
- Secured Dashboard
- Login Page
- Clean Dashboard for all administrative needs for 3 different levels of access: Administrator, User, and Operator
- Admin account management panel
- Easy to use search function with multiple fields  
- Conversion of fillable forms to PDF


## Setup
> Python 3+ installation is required


1. Clone this repository and open it in your IDE of choice (PyCharm Community Edition is recommended)

```bash
git clone https://github.com/averylam1/nucmami-absm.git
```

2. Install requirements

```bash
pip install -r requirements.txt
```

(Optional) . If deploying or running on Heroku, the `wkhtmltopdf-pack-ng` package will fulfill this requirement (Skip this). 
Otherwise, you will need to download and install `wkhtmltopdf` from https://wkhtmltopdf.org/downloads.html.

3. Replace SQL Database connection details in 
`sql_credentials.py`

4. Open a terminal and start the Flask server with:

```bash
python app.py
```
or
```bash
flask run
```

Server should be hosted on http://127.0.0.1:5000/ by default.

## User Manual

The user manual provides information on the application's various screens and functions.

[User Manual](https://docs.google.com/document/d/1bV2GLHY63RU_JRNsK3aWp2qgd0Y8NNK6E6ER2F-G3wQ/edit?usp=sharing)

## User Test Report

The user test report provides information on the tests used for this project.

[User Test Report](https://docs.google.com/document/d/1itRE2Oz1bchs3iJFrAFvKswP-0jtBeEHdW5fEiqZFNE/edit?usp=sharing)

## Maintenance Manual

The maintenance manual provides information on how to deploy and maintain the application.

[Maintenance Manual](https://docs.google.com/document/d/1FhVtbX3INcT5bYU51-_CKw6QMOQZtXtu2kVyTt0ESPo/edit?usp=sharing)
