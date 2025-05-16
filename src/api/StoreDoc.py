# Import necessary libraries
from src.util.FileUtilities import FileUtilities
from src.conf.Configurations import logger, categories
from fastapi import HTTPException
from fastapi import UploadFile
from io import BytesIO
from src.util.FileMetadataDatabaseUtility import FileMetadataDatabaseUtility


class FileUploader:
    """
    A class to handle file uploads and metadata extraction.
    """
    def __init__(self, category):
        """
        Initialize the FileUploader with a specified upload path.
        :param upload_path: The path where files will be uploaded.

        """
        self.category = category
        self.base_path_upload = categories[category]

        self.file_utilities = FileUtilities()

        self.flag = False

    def upload_single_file(self, file: UploadFile):
        """
        Upload a single file and extract its metadata.

        :param file: The file to be uploaded.
        :return: A dictionary containing the metadata of the uploaded file.
        """

        # # Check if the file already exists in the destination folder
        # logger.info(f"Checking if the file {file.name} already exists in the destination folder...")
        # file_exits = self.file_utilities.has_file_in_destination_folder(file.name, self.base_path_upload)
        #
        # # check if the file already exists in the destination folder
        # if file_exits:
        #     return file_exits, self.flag

        # Save the file in the destination folder
        self.file_utilities.save_file_in_destination_folder(file, self.base_path_upload)

        # Extract metadata from the uploaded file
        metadata_dict = self.file_utilities.get_metadata(file.name, self.base_path_upload)
        logger.info(f"Metadata extracted successfully for {file.name}")

        # Check if the file version already exists
        logger.info(f"Checking if the file version {file.name} already exists in the destination folder...")
        versioned_files = self.file_utilities.list_versioned_files(file.name, self.base_path_upload)

        if versioned_files:

            # todo: need to remove once we implement Continue or user acceptance button.
            self.file_utilities.remove_file(file.name, self.base_path_upload)

            for versioned_file in versioned_files:
                updated_file = ""
                if metadata_dict['file_creation_date'] <= versioned_file['file_creation_date'] and metadata_dict['file_modified_date'] < versioned_file['file_modified_date']:
                    logger.info(f"File {file.name} already exists in the destination folder.")
                    updated_file = versioned_file['file_name']
            if updated_file:
                self.flag = True
                return f"Seems like you are trying to upload a older version of the {updated_file}. Please check the updated file in the destination folder.", self.flag
            else:
                return f"Seems like you are trying to upload a new version of the {versioned_files[0]['file_name']}. Please check the older file in the destination folder.If you want to update the file please click on continue", self.flag

        # Store metadata in the database
        try:

            # Check if the file already exists in the database with the same hash
            count = FileMetadataDatabaseUtility().check_file_hash(metadata_dict['file_hash'])

            if count > 0:
                self.file_utilities.remove_file(file.name, self.base_path_upload)
                return f"File {file.name} already exists in the database.", self.flag


            FileMetadataDatabaseUtility().insert_file_info(metadata_dict, file_category=self.category)
            logger.info(f"Metadata stored successfully for {file.name}")

            return "File uploaded successfully!", self.flag
        except Exception as e:
            # Remove the file if metadata storage fails
            logger.info(f"Removing the file {file.name} due to metadata storage failure...")
            self.file_utilities.remove_file(file.name, self.base_path_upload)

            logger.error(f"Error storing metadata: {e}")
            raise HTTPException(status_code=500, detail=f"Error storing metadata : {e}")


if __name__ == "__main__":

    sample_file = UploadFile(filename="Scan May 5, 2025.pdf",
                             file=BytesIO(open(r"C:\Users\Karnatapus\Downloads\Scan May 5, 2025.pdf", 'rb').read()))

    file_uploader = FileUploader()

    file_uploader.upload_single_file(sample_file)

