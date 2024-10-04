from app import create_app
import logging
from os import makedirs

log_dir = "logs"
makedirs(log_dir, exist_ok=True)
    
# Configure logging globally
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",  # Add a standard log format
    handlers=[
        logging.FileHandler("logs/paper_retrieval.log"),  # Log to file
        logging.StreamHandler()  # Log to console
    ]
)

# Create the Flask app
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5502)
