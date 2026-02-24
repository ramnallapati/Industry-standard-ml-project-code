import os
import logging
import datetime

# this file is used to log all the executions

log_file = f'{datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}.log'


# creating log file folder
log_path = os.path.join(os.getcwd(),"logs",log_file)
os.makedirs(log_path,exist_ok=True)

log_file_path = os.path.join(log_path,log_file)

logging.basicConfig(
  filename=log_file_path,
  format="[%(asctime)s] %(lineno)d %(name)s - %(message)s",
  level=logging.INFO
)