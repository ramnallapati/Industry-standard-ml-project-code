import sys
from networksecurity.logging import logger

class NetworkSecurityException(Exception):
  def __init__(self,error_message,error_details:sys):
    self.error_message = error_message
    _,_,exec_tb = error_details.exc_info()
    
    self.line_no = exec_tb.tb_lineno
    self.file_name = exec_tb.tb_frame.f_code.co_filename
    
  def __str__(self):
    return "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
  self.file_name,
  self.line_no,
  str(self.error_message))
     
     
# checking it is working or not
# if __name__ == "__main__":
#   try:
#     logger.logging.info("Enter the try block")
#     a = 1/10
#     print("this will not be printed",a)
#   except Exception as e:
#     raise NetworkSecurityException(e,sys)