import logging

## Setup Loggers to Different .py Just import logging AND LoggerFunction to others and call LoggerFunction.setup_logger(name,log_file,level,formatter)
def setup_logger(name, log_file,level,formatter,filemode='a'):
    formatter3 = logging.Formatter(formatter)
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter3)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

## Print to console ALL information from ALL files that are at least level INFO or above
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter2 = logging.Formatter('%(asctime)s : %(name)s : %(message)s')
console.setFormatter(formatter2)
logging.getLogger().addHandler(console)