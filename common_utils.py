import logging
from colorlog import ColoredFormatter
import time
import os
import csv
in_logger = None
def get_logger(log_file_suffix=''):
    global in_logger
    if in_logger is not None:
        return in_logger
    # 创建 logger
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)

    # 创建文件处理器，将日志记录到文件
    os.makedirs('./log', exist_ok=True)
    file_handler = logging.FileHandler('./log/pywasm_%s_%s.log'%(time.time(), log_file_suffix))
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    # 创建控制台处理器，将日志输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    # 定义带颜色的日志格式
    colored_formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    console_handler.setFormatter(colored_formatter)
    # 添加处理器到 logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # 记录不同级别的日志
    logger.debug('这是调试信息')
    logger.info('这是信息消息')
    logger.warning('这是警告消息')
    logger.error('这是错误消息')
    logger.critical('这是严重错误消息')
    in_logger = logger
    return logger

def write_csv(data, file):
    print('Write to ' + file)
    if not os.path.exists(file):
        with open(file, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)
    else:
        with open(file, 'a+') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data) 

def write_txt(str,file):
    print('Write to ' + file)
    with open(file, 'w') as f:
        f.write(str)
    