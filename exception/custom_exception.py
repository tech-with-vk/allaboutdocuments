import sys
import traceback
# from logger.custom_logger import CustomLogger


# logger = CustomLogger().get_logger(__file__)


class AllAboutDocumentsException(Exception):
    """Custom Exception class for All About Documents portal"""

    def __init__(self, error_message, original_exception: Exception):
        # Capture the current exception info from the interpreter
        # _, _, exception_traceback = sys.exc_info()
        _, _, exception_traceback = original_exception.__traceback__

        # Extract filename and line number safely
        self.file_name = (
            exception_traceback.tb_frame.f_code.co_filename
            if exception_traceback
            else "N/A"
        )
        self.linenumber = (
            exception_traceback.tb_lineno if exception_traceback else "N/A"
        )
        self.error_message = str(error_message)

        # Format the traceback string
        self.traceback_str = (
            "".join(
                traceback.format_exception(
                    type(original_exception), original_exception, exception_traceback
                )
            )
            if exception_traceback
            else "Traceback not available"
        )

        # Pass full message to the base Exception
        full_message = (
            f"\n\tError in [{self.file_name}] at line number [{self.linenumber}]\n"
            f"\tMessage: {self.error_message}\n"
            f"\tTraceback: {self.traceback_str}"
        )

        super().__init__(full_message)

    def __str__(self):
        """This is the string representation of the exception module"""
        return f"""
            Error in [{self.file_name}] at line number [{self.linenumber}]
            Message: {self.error_message}
            Traceback : {self.traceback_str}
            """


if __name__ == "__main__":
    # from logger.custom_logger import CustomLogger

    # logger = CustomLogger().get_logger(__name__)
    # logger.info("🔍 Running test for AllAboutDocumentsException...\n")

    try:
        # Trigger an intentional error
        a = 1 / 0
    except Exception as e:
        # logger.error(
        #     "An exception occurred. Raising custom exception now.", exc_info=True
        # )
        raise AllAboutDocumentsException("Test exception during development", e)