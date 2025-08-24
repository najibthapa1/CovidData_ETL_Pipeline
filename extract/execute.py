import os, sys, requests, time
from zipfile import ZipFile
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utility.utility import setup_logging, format_time
#---------------------------------------
#ONLY NEEDED IF ZIP DOWNLOAD IS REQUIRED
#---------------------------------------
# def download_zip_file(url, output_dir, logger):
#     response = requests.get(url, stream=True)
#     os.makedirs(output_dir, exist_ok=True)
    
#     if response.status_code == 200:
#         filename = os.path.join(output_dir, "downloaded.zip")
#         with open(filename, "wb") as f:
#             for chunk in response.iter_content(chunk_size=8192):
#                 if chunk:
#                     f.write(chunk)
#         logger.info(f"Downloaded zip file: {filename}")
#         return filename
#     else:
#         logger.error(f"Failed to download file. Status code: {response.status_code}")
#         raise Exception(f"Failed to download file. Status code: {response.status_code}")
    
# def extract_zip_file(zip_filename, output_dir, logger):
#     with ZipFile(zip_filename, 'r') as zip_file:
#         zip_file.extractall(output_dir)
#     logger.info(f"Extracted zip file to: {output_dir}")
#     logger.info("Removing the zip file")
#     os.remove(zip_filename)
# ---------------------------------------------------------------------

if __name__ == "__main__":

    logger = setup_logging("extract.log")
    if len(sys.argv) < 2:
        logger.debug("Extraction path is required")
        logger.debug("Example usage:")
        logger.debug("python3 execute.py /Users/najibthapa1/projectData/Extract")
    else:
        try:
            logger.debug("Starting Extraction Engine...")
            start = time.time()
            EXTRACT_PATH = sys.argv[1]

            # -------------------------------
            # CSV Direct Download
            # -------------------------------
            CSV_URL = "https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv"
            csv_file = os.path.join(EXTRACT_PATH, "compact.csv")
            logger.debug(f"Downloading CSV from {CSV_URL} ...")
            r = requests.get(CSV_URL)
            r.raise_for_status()  # Ensure download succeeded
            with open(csv_file, "wb") as f:
                f.write(r.content)
            logger.info(f"CSV downloaded to {csv_file}")

            # -------------------------------
            # ZIP download/extraction
            # -------------------------------
            # URL = "https://storage.googleapis.com/kaggle-data-sets/494724/2364896/bundle/archive.zip?...(long URL)..."
            # zip_file = download_zip_file(URL, EXTRACT_PATH, logger)
            # extract_zip_file(zip_file, EXTRACT_PATH, logger)

            end = time.time()
            logger.info("Extraction Successfully Completed!")

        except Exception as e:
            logger.error(f"Error: {e}")