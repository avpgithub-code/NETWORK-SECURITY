import logging
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler

class NetworkSecurityLogger:
    def __init__(
        self, log_dir='logs', 
        log_file='network_security.log', 
        max_bytes=5*1024*1024, backup_count=3):
        #----------------------------------------------------------
        # Convert string inputs to Path objects immediately
        #----------------------------------------------------------
        self.log_dir = Path(log_dir)
        self.log_file = log_file
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        #----------------------------------------------------------
        self.logger = logging.getLogger('NetworkSecurityLogger')
        self.logger.setLevel(logging.INFO)
        self._setup_logger()
    #----------------------------------------------------------
    def _setup_logger(self):
        #----------------------------------------------------------
        # Path.mkdir handles directory creation cleanly (exist_ok=True replaces 'if not exists')
        self.log_dir.mkdir(parents=True, exist_ok=True)
        #----------------------------------------------------------
        # Use the / operator or .joinpath() for clean path concatenation
        log_path = self.log_dir / self.log_file
        #----------------------------------------------------------
        # RotatingFileHandler accepts Path objects directly in modern Python
        handler = RotatingFileHandler(
            filename=log_path, 
            maxBytes=self.max_bytes, 
            backupCount=self.backup_count)
        #----------------------------------------------------------
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        #----------------------------------------------------------
        # Avoid adding multiple handlers if the logger is re-initialized
        if not self.logger.handlers:
            self.logger.addHandler(handler)
    #----------------------------------------------------------
    def log_info(self, message):
        self.logger.info(message)
    #----------------------------------------------------------
    def log_warning(self, message):
        self.logger.warning(message)
    #----------------------------------------------------------
    def log_error(self, message):
        self.logger.error(message)
    #----------------------------------------------------------
    def log_debug(self, message):
        self.logger.debug(message)
#----------------------------------------------------------
# CREATE THE INSTANCE FOR USE IN OTHER MODULES
#----------------------------------------------------------
ns_logger = NetworkSecurityLogger()
#----------------------------------------------------------
# Example usage:
#----------------------------------------------------------
if __name__ == "__main__":
    # ns_logger = NetworkSecurityLogger()
    ns_logger.log_info("Network security monitoring started.")
    ns_logger.log_warning("Potential threat detected.")
    ns_logger.log_error("Error in network security module.")
    ns_logger.log_debug("Debugging network security issue.")
#----------------------------------------------------------