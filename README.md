# 📘 User Manual for COVID-19 ETL Pipeline Project  

## 1. Introduction  
This project is an ETL (Extract, Transform, Load) pipeline built with PySpark, PostgreSQL, and Apache Superset to analyze COVID-19 data (2020–2025). It extracts raw data from CSV, transforms it into a clean structured format, and loads it into PostgreSQL for visualization in Superset.


- **Extract**: Reads COVID-19 dataset.  
- **Transform**: Cleans, filters, and organizes the data (cases, deaths, population).  
- **Load**: Stores the processed data into a **PostgreSQL database** for analysis & dashboards in **Apache Superset**.  

---

## 2. Prerequisites  

### ✅ Install These Softwares  
- [Python 3.8+](https://www.python.org/downloads/)  
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

scroll down and change 'peer' keyword to 'md5' in the connection part

restart the postgresql service 

### Setting up pgAdmin

- Open pgAdmin
- Go to Servers Right Click -> Register -> Service
- Fill out the fields:
  - hostname :   localhost
  - post : 5432
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

---

## 8. Visualize with Superset
