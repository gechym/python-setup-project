def setup_logging() -> None:
    import logging
    import sys
    from pprint import pformat

    import colorlog

    # Tạo một custom formatter có khả năng format dict bằng pprint
    class PrettyDictFormatter(colorlog.ColoredFormatter):
        from logging import LogRecord

        def format(self, record: LogRecord) -> str:
            # Kiểm tra xem message có chứa dict không
            if hasattr(record, "msg") and isinstance(record.msg, str):
                # Nếu có dict trong args, sử dụng pprint để định dạng
                if hasattr(record, "args") and record.args:
                    new_args = []
                    for arg in record.args:
                        if isinstance(arg, dict):
                            # Sử dụng pformat để định dạng dict
                            new_args.append(pformat(arg, indent=2, width=80))
                        else:
                            new_args.append(str(arg))
                    record.args = tuple(new_args)

            return str(super().format(record))

    # Thiết lập root logger
    root_logger = logging.getLogger()

    # Xóa tất cả handlers hiện có (nếu có)
    if root_logger.handlers:
        for handler in root_logger.handlers:
            root_logger.removeHandler(handler)

    # Tạo console handler
    console_handler = colorlog.StreamHandler(stream=sys.stdout)

    # Format log message với màu sắc
    log_format = "\n%(log_color)s%(levelname)-8s%(reset)s %(blue)s[%(asctime)s]%(reset)s %(cyan)s[%(name)s]%(reset)s %(message)s\n"

    # Định dạng thời gian
    date_format = "%Y-%m-%d %H:%M:%S"

    # Thiết lập màu sắc cho các level log
    colors = {
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    }

    # Tạo formatter với colorlog và khả năng format dict
    formatter = PrettyDictFormatter(log_format, datefmt=date_format, log_colors=colors)

    # Gán formatter cho handler
    console_handler.setFormatter(formatter)

    # Thêm handler vào root logger
    root_logger.addHandler(console_handler)

    # Thiết lập level về mức thấp nhất (DEBUG) để hiển thị tất cả các mức log
    root_logger.setLevel(logging.DEBUG)

    noisy_loggers = [
        "httpx",
        "httpcore",
        "httpcore.http11",
        "urllib3",
        "matplotlib",
        "asyncio",
        "requests",
        "chardet",
        "charset_normalizer",
        "openai",
        "openai.api_resources",
        "openai.agents",
    ]

    for logger_name in noisy_loggers:
        logging.getLogger(logger_name).setLevel(logging.WARNING)  # hoặc logging.ERROR nếu muốn im lặng hơn nữa

    # Log một số thông tin khởi động
