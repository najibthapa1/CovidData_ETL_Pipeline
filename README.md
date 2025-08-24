COVID-19 ETL Pipeline

This project is an ETL (Extract, Transform, Load) pipeline built with PySpark, PostgreSQL, and Apache Superset to analyze COVID-19 data (2020–2025). It extracts raw data from CSV, transforms it into a clean structured format, and loads it into PostgreSQL for visualization in Superset.

🚀 Features
	•	Extracts COVID-19 dataset from local files.
	•	Cleans, casts datatypes, and aggregates data with PySpark.
	•	Loads processed data into PostgreSQL.
	•	Visualizes data using Apache Superset with charts & dashboards.
	•	Logging enabled for Extract, Transform, Load phases.

📂 Project Structure
ETL_project/
│── extract/            # Extract raw dataset
│   └── execute.py
│
│── transform/          # Clean and transform data
│   └── execute.py
│
│── load/               # Load transformed data into PostgreSQL
│   └── execute.py
│
│── utility/            # Utility functions (logging, configs)
│   └── utility.py
│
│── .gitignore          # Ignore logs, JSON configs, cache
│── requirements.txt    # Python dependencies
│── README.md           # Documentation

🛠️ Requirements

1. Clone the repository
git clone https://github.com/your-username/ETL_project.git
cd ETL_project

2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # for macOS/Linux
venv\Scripts\activate      # for Windows

3.  Install dependencies
pip install -r requirements.txt

▶️ Running the ETL Pipeline
1.	Run Extract:
python extract/execute.py

2.	Run Transform:
python transform/execute.py

3.	Run Load:
python load/execute.py
