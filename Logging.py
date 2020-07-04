import logging
from logging.handlers import TimedRotatingFileHandler
from PyQt5.QtCore import QTime
from threading import Thread

# 처음 프로그램 실행 전에 프로그램 위치에 logs 폴더와 logs 폴더 안에 trade 폴더를 만들어야 함



# 메인 로거 클래스
# 파일 입출력으로 인한 blocking을 막기 위해 별도 스레드
# 메인 스레드와 큐를 이용해 통신
class Logger(Thread):

    # 추가할 로그 레벨
    # "KIWOOM" 레벨 : 키움 api 사용 관련 로그
    # "TRADE" 레벨 : 체결 내역 관련 로그
    KIWOOM_LEVEL = 60
    TRADE_LEVEL = 90

    # trade_ui_signal : 체결 내역 ui에 로그를 출력하기 위해 연결할 시그널
    # log_ui_signal : 로그 내역 ui에 로그를 출력하기 위해 연결할 시그널
    # queue : 다른 스레드와 상호작용 하기 위한 큐
    def __init__(self, queue):
        Thread.__init__(self)

        self.log_queue = queue
        # 데몬 스레드 설정
        self.daemon = True

        # 로그 레벨 추가(기존 - ERROR : 40, INFO : 20, DEBUG : 10, 등등)

        logger = logging.getLogger('chardet.charsetprober')
        logger.setLevel(logging.INFO)

        # 루트 로거 생성
        # 루트 로거에 콘솔 출력 핸들러 부착
        # format - asctime : 시간, name : 로거이름, levelname : 로깅레벨, messge : 메시지
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

        console_formatter = logging.Formatter(fmt='[%(asctime)s][%(levelname)s] %(message)s', datefmt='%H:%M:%S')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)

        # 루트 로거의 자식 "Program" 로거 생성
        # 프로그램 진행 상황에 대한 info, error, kiwoom, condition, signal, trade 레벨 수준 로그 출력
        # 출력대상은 로그 파일과 로그내역 ui
        # 로그가 기록될 파일은 매일 자정을 기준으로 새로운 파일에 기록
        # backupConfig에 설정된 값만큼 파일 갯수 저장, 해당 설정 값 이상의 파일이 있으면 오래된 순서대로 파일 자동 삭제
        # 파일 이름은 ./logs/program_log
        self.prog_logger = logging.getLogger("Program")

        # import os
        # os.chmod('logs/program_log', "0777")

        prog_file_formatter = logging.Formatter(fmt='[%(asctime)s][%(levelname)s] %(message)s', datefmt='%H:%M:%S')
        prog_file_handler = TimedRotatingFileHandler('logs/program_log', when='midnight', encoding='utf-8', backupCount=60)
        prog_file_handler.setFormatter(prog_file_formatter)
        prog_file_handler.setLevel(logging.INFO)
        # prog_file_handler.setLevel(logging.DEBUG)
        self.prog_logger.addHandler(prog_file_handler)



    def run(self):
        try:
            while True:
                # 큐를 통해 다른 스레드에서 함수 수신
                request = self.log_queue.get()

                # 큐를 통해 받은 함수 호출
                request[0](self,*request[1])
        except Exception:
            self.error("log thread error")
            raise
        finally:
            # 처리되지 않는 로그를 모두 처리한다.
            logging.shutdown()
            self.info("log thread shutdown")

    # 큐에 함수를 넣는 로그 출력 함수 데코레이터
    def queue_put_decorator(func):
        def func_wrapper(self, *args, **kwargs):
            self.log_queue.put((func,args))
        return func_wrapper

    # debug level 로그 출력 함수
    # 다른 스레드에서 해당 함수를 큐를 통해 Logger 스레드에 전달
    @queue_put_decorator
    def debug(self, msg):
        self.prog_logger.debug(msg)

    # info level 로그 출력 함수
    # 다른 스레드에서 해당 함수를 큐를 통해 Logger 스레드에 전달
    @queue_put_decorator
    def info(self, msg):
        self.prog_logger.info(msg)

    # warning level 로그 출력 함수
    # 다른 스레드에서 해당 함수를 큐를 통해 Logger 스레드에
    @queue_put_decorator
    def warning(self, msg):
        self.prog_logger.warning(msg)

    # error level 로그 출력 함수
    # 다른 스레드에서 해당 함수를 큐를 통해 Logger 스레드에
    @queue_put_decorator
    def error(self, msg):
        self.prog_logger.error(msg)




