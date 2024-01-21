import logging
import os
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" # log file name
logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE) #log path for saving multiple log files in a logs folder
os.makedirs(logs_path, exist_ok=True) #creates a logs folder. If already present, then due to exist_ok=True, just appends the log files in that folder.

LOG_FILE_PATH= os.path.join(logs_path,LOG_FILE) #log file path

#logging the activity with basicConfig in a systematic format
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

