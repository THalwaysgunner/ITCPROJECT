import glob
import os
import logging.handlers
import time


LOG_FILENAME = 'logs/log_scraper.log'

# Set up a specific logger with our  output level
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Check if log exists and should therefore be rolled
needRoll = os.path.isfile(LOG_FILENAME)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, backupCount=50)

logger.addHandler(handler)

# This is a stale log, so roll it
if needRoll:
    # Add timestamp
    logger.debug('\n---\nLog closed on %s.\n---\n' % time.asctime())

    # Roll over on application start
    logger.handlers[0].doRollover()

# Add timestamp
logger.debug('\n---\nLog started on %s.\n---\n' % time.asctime())

# See what files are created so we can track it in the logs folder
log_files = glob.glob('%s*' % LOG_FILENAME)

print('\n'.join(log_files))