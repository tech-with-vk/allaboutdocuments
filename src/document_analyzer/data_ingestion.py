import os
import fitz
import uuid
from datetime import datetime
from logger.custom_logger import CustomLogger
from exception.custom_exception import AllAboutDocumentsException


class DocumentHandler:
    """
    Handles PDF-related activities such as reading and saving.
    Initializes a unique session directory for each session,
    and logs all operations for tracking and debugging.
    """

    def __init__(self, file_location=None, session_id=None) -> None:
        try:
            # Initialize logger
            self.logger = CustomLogger().get_logger(__name__)

            # Set base storage directory (default: ./data/document_analyzer)
            self.file_location = file_location or os.getenv(
                "DATA_STORAGE_PATH",
                os.path.join(os.getcwd(), "data", "document_analyzer"),
            )

            # Generate a detailed session ID
            self.session_id = self.generate_session_id(session_id)

            # Create a session-specific directory
            self.session_directory = os.path.join(self.file_location, self.session_id)
            os.makedirs(self.session_directory, exist_ok=True)

            # Log successful initialization
            self.logger.info(
                "Document Handler successfully initialized",
                session_id=self.session_id,
                session_directory=self.session_directory,
            )
        except Exception as e:
            self.logger.error(f"Failed to initialize Document Handler: {e}")
            raise AllAboutDocumentsException(
                "Failed to initialize Document Handler", e
            ) from e

    @staticmethod
    def generate_session_id(session_id=None):
        """
        Generate a unique session ID using user, hostname, timestamp, and a short UUID.
        """
        if session_id:
            return session_id

        # hostname = socket.gethostname()
        user_identifier = os.getenv("USER", "anonymous")

        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S%fZ")
        unique_part = uuid.uuid4().hex[:6]

        # return f"session_{user_identifier}_{hostname}_{timestamp}_{unique_part}"
        return f"session_{user_identifier}_{timestamp}_{unique_part}"

    def save_pdf(self, file_to_be_analyzed):
        """
        Saves a PDF file to the session-specific directory after validating its format.

        Parameters:
            file_to_be_analyzed: An object representing the PDF file.
            It must have a `name` attribute (filename with extension)
            and a `getbuffer()` method that returns the binary content of the file.

        Returns:
            str: The full path where the PDF file was saved.

        Raises:
            AllAboutDocumentsException: If the file is not a PDF or if saving fails for any reason.
        """
        try:
            # Extract the base file name from the file object
            pdf_file_name = os.path.basename(file_to_be_analyzed.name)

            # Validate that the file has a .pdf extension (case-insensitive)
            if not file_to_be_analyzed.name.lower().endswith(".pdf"):
                raise AllAboutDocumentsException(
                    "Invalid file type. We currently support PDFs only"
                )

            # Construct the full path where the PDF will be saved
            the_pdf_is_saved_here = os.path.join(self.session_directory, pdf_file_name)

            # Write the binary contents of the file to the target location
            with open(the_pdf_is_saved_here, "wb") as pdf_file:
                pdf_file.write(file_to_be_analyzed.getbuffer())

            # Log successful save with relevant metadata
            self.logger.info(
                "The PDF file saved successfully",
                saved_file=pdf_file_name,
                saved_path=the_pdf_is_saved_here,
                session_for_the_analysis=self.session_id,
            )

            # Return the path where the file was saved
            return the_pdf_is_saved_here

        except Exception as e:
            # Log the error and raise a custom exception with the original error attached
            self.logger.error(f"Error while saving PDF file: {e}")
            raise AllAboutDocumentsException("Error while saving PDF file", e) from e

    def read_pdf(self, path_of_the_file_to_be_analyzed):
        """
        Placeholder method for reading a PDF file.
        """
        try:
            text_chunks = []
            with fitz.open(path_of_the_file_to_be_analyzed) as document:
                for page_number, page in enumerate(document, start=1):
                    text_chunks.append(
                        f"\n--- Page {page_number} ---\n{page.get_text()}"
                    )
            text = ".\n".join(text_chunks)

            self.logger.info(
                "The PDF file read successfully",
                saved_path=path_of_the_file_to_be_analyzed,
                session_for_the_analysis=self.session_id,
                number_of_pages=len(text_chunks),
            )

            return text

        except Exception as e:
            self.logger.error(f"Error while reading the PDF file: {e}")
            raise AllAboutDocumentsException(
                "Error while reading the PDF file", e
            ) from e


# Entry point of the script
if __name__ == "__main__":
    # Import required modules
    from pathlib import Path

    # Define the path to the PDF file that will be analyzed
    path_of_the_file_to_be_analyzed = (
        r"D:\\00.LLMOPS\\allaboutdocuments\\data\\document_analyzer\\Generative AI.pdf"
    )

    # Dummy class to mimic a PDF document object with basic functionality
    class DummyPdfDocument:
        def __init__(self, path_of_the_file_to_be_analyzed):
            # Extract just the filename from the full path
            self.name = Path(path_of_the_file_to_be_analyzed).name
            # Store the full path of the PDF file
            self._path_of_the_file_to_be_analyzed = path_of_the_file_to_be_analyzed

        def getbuffer(self):
            # Open the file in binary read mode and return its contents
            with open(self._path_of_the_file_to_be_analyzed, "rb") as f:
                return f.read()

    # Create an instance of the dummy PDF document
    dummy_pdf_document = DummyPdfDocument(path_of_the_file_to_be_analyzed)

    # Create an instance of the document handler
    handler = DocumentHandler(session_id="test_session_id")

    try:
        # Attempt to save the PDF using the document handler
        saved_path = handler.save_pdf(dummy_pdf_document)
        print(saved_path)  # Print the path where the PDF was saved

        # Attempt to read the PDF using the document handler
        content = handler.read_pdf(saved_path)
        print("PDF Content: ")
        print(content[:500])  # Print first 500 characters

    except Exception as e:
        # Catch and print any errors that occur during processing
        print(f"Error : {e}")
