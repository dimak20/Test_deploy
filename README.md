# Task manager project

A project for managing tasks, projects, teams and employees.

[Task Manager Project deployed to Render](https://task-manager-project-pw7u.onrender.com/)

```
Test account credentials
Email: 
johndoe@email.com
Password: 
testAcc1
```

## Installing / Getting started

Python3 must be already installed!
Before starting the server make sure to set correct values in the `.env` file

```shell
git clone https://github.com/DSahalatyi/task-manager-project/
cd task_manager_project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver # Starts django server
```

## Features

Authentication functionality including:
* User email invitation system
* Login, Registration & Password Recovery

Employee management system
* Ability to update employee's position
* Ability to create teams for employees that can later be assigned to projects

Task management system
* Ability to create and manage projects
* Ability to create and manage tasks

User dashboard (used as homepage)
* Accumulation of previously mentioned features gathered in one place

