# 📘 User Manual for COVID-19 ETL Pipeline Project  

## 1. Introduction  
This project is an ETL (Extract, Transform, Load) pipeline built with PySpark, PostgreSQL, and Apache Superset to analyze COVID-19 data (2020–2025). It extracts raw data from CSV, transforms it into a clean structured format, and loads it into PostgreSQL for visualization in Superset.


- **Extract**: Reads COVID-19 dataset.  
- **Transform**: Cleans, filters, and organizes the data (cases, deaths, population).  
- **Load**: Stores the processed data into a **PostgreSQL database** for analysis & dashboards in **Apache Superset**.  

---

## 2. Prerequisites  

### ✅ Install These Softwares  
- [Python](https://www.python.org/downloads/)  
- [Git](https://git-scm.com/downloads)  
- [PostgreSQL](https://www.postgresql.org/download/) (default port `5432`)  
- [pgAdmin](https://www.pgadmin.org/download/)
- [PostgreSQL JDBC Driver](https://jdbc.postgresql.org/download/)

---

## 3. Download the Project  

```bash
git clone https://github.com/najibthapa1/CovidData_ETL_Pipeline.git
cd Covid_ETL_Pipeline
```

---

## 4. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # for macOS/Linux
venv\Scripts\activate      # for Windows
```

---

## 5. Install required Libraries

```bash
pip install -r requirements.txt
```

---

## 6. PostgreSQL Setup

### Installing postgresql

```bash
brew install postgresql       #for macOS 
sudo apt install postgresql   #for Ubuntu
```

### Setting user and password

```bash
brew services start postgresql (mac) / sudo -i -u postgres (ubuntu)
psql
alter user postgres with password 'postgres'
ALTER USER
\q
exit
```

### Updating pg_hba.conf file

```bash
sudo nano /etc/postgresql/16/main/pg_hba.conf
```

Scroll down and change the 'peer' keyword to 'md5' in the connection part

Restart the PostgreSQL service 

### Setting up pgAdmin

- Open pgAdmin
- Go to Servers, Right Click -> Register -> Service
- Fill out the fields:
  - hostname:   localhost
  - port: 5432
  - username: postgres
  - password: postgres
    
---

## 7. Run the ETL Pipeline

### Step 1: Extract

```bash
python extract/extract.py /home/...(full path to the directory you want to save the extracted files)
```

### Step 2: Transform

```bash
python transform/transform.py /(extracted files full path)  /(full path to the directory you want to save the transformed files)
```

### Step 3: Load

```bash
python load/load.py /(transformed files full path) db_username db_password
```

After loading success, the data can be viewed from the pgAdmin -> localhost -> Tables

---

## 8. Visualize with Superset (Optional)

### Create a new directory superset and cd into it

```bash

mkdir superset && cd superset
```

### Create a new virtual environment and install apache superset

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install apache_superset
```

### Add parameters required by Apache Superset

```bash
nano ~/.bashrc or nano ~/.zshrc
```

Add the following parameters:

export SUPERSET_SECRET_KEY=YOUR-SECRET-KEY

export FLASK_APP=superset

Save it & 
```bash
source ~/.bashrc or source ~/.zshrc
```

### Installing required libraries
```bash
pip install Pillow
pip install marshmallow==3.26.1
pip install psycopg2-binary
```

### Initializng database and admin user

```bash
superset db upgrade
superset fab create-admin
superset init
```

### Running the superset server in development mode in port 8088

```bash
superset run -p 8088 --wuth-threads-reload --debugger
```

- Go to webbrowser and type localhost:8088.
- Enter the username and password set earlier
- Connect our local postgre server to superset
- Click the + icon > Data > Connect database
- Select postgres, enter your credentials and press connect
- Create a dataset out of daily_country (database - PostgreSQL, Schema - public, Table - daily_country)
- Create charts and dashboard to save the created charts.

---
