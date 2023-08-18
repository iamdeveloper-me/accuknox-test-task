# accuknox-test-task


# Social Networking Application

Here is the desired social networking application where you can make friends by sending them the invitation to join you. 

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Configuration](#configuration)
  - [Environment Variables](#environment-variables)
  - [Database Configuration](#database-configuration)
- [Usage](#usage)
- [Docker Configuration](#Docker-Configuration)


## Introduction

Here is the desired social networking application where you can make friends by sending them the invitation to join you. 

## Features

- send/accept/reject friend request
- list friends(list of users who have accepted friend request)
- List pending friend requests(received friend request)
- search filters
 

## Getting Started

Follow these steps to set up and run the App on your local machine.

### Prerequisites

- Python (3.6+)
- pip
- Virtual environment (recommended)
- Docker (not neccessary)

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/iamdeveloper-me/accuknox-test-task

2. Create a virtual environment (optional but recommended):

    ```sh
    python -m venv venv
    source venv/bin/activate

3. Install the required dependencies:

    ```sh
    pip install -r requirements.txt

### Configuration
    
    Configure the app based on your needs:

### Environment Variables

    Create a .env file in the root directory and define the following environment variables:
    
    ```sh
    SECRET_KEY=your_secret_key
    DEBUG=True
    DATABASE_URL=your_database_url

### Database Configuration

Specify your database settings in the settings.py file.


### Usage

1. Apply Migrations

    ```sh
    python manage.py makemigrations
    python manage.py migrate

2. Create a superuser (if needed):

    ```sh
    python manage.py createsuperuser

3. Start the development server:

    ```sh
    python manage.py runserver

4. Access the app at http://127.0.0.1:8000.

### Docker Configuration 

1. Install Docker and Docker-Compose

    Follow the guidelines to install docker  - https://docs.docker.com/engine/install/

2. Run the docker container setup for setting up and run the app

    ```sh 
    docker-compose up --build