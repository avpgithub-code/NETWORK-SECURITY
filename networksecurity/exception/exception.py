import sys
from networksecurity.logging.logger import ns_logger # Safe: logger doesn't import this back

class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error(error_message, error_detail)
        #----------------------------------------------------------
        # Log the error the moment the exception is created
        ns_logger.log_error(self.error_message)
    #----------------------------------------------------------
    def get_detailed_error(self, error, error_detail: sys):
        _, _, exc_tb = error_detail.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_num = exc_tb.tb_lineno
        return f"Error in [{file_name}] line [{line_num}]: {str(error)}"
#----------------------------------------------------------
if __name__ == "__main__":
    # Test the exception and logger integration
    try:
        x = 1 / 0
    except Exception as e:
        # This will print the error AND save it to logs/system.log
        raise CustomException(e, sys)