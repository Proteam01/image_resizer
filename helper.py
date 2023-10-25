import logging

logging.basicConfig(level=logging.INFO, filename='resizer.log', filemode='a',
                    format='%(asctime)s:%(levelname)s:%(name)s:%(lineno)d - %(message)s')
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())