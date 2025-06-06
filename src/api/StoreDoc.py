# Import necessary libraries
from src.util.FileUtilities import FileUtilities
from src.conf.Configurations import logger, categories
from fastapi import HTTPException, UploadFile
from io import BytesIO
from src.util.FileMetadataDatabaseUtility import FileMetadataDatabaseUtility


class FileUploader:
    """
    A class to handle file uploads and metadata extraction.
    """

    def __init__(self, file_category, file: UploadFile):
        """
        Initialize the FileUploader with a specified upload path.
        :param file_category: The category of the file being uploaded.
        :param file: The file to be uploaded.
        """
        self.file_category = file_category
        self.base_path_upload = categories[file_category]
        self.file_utilities = FileUtilities()
        self.file = file
        self.flag = False
        self.category_id = 1

    # Upload a single file and extract its metadata.
    def upload_single_file(self):
        """
        Upload a single file and extract its metadata.
        :return: A tuple (message, flag) indicating the result.
        """
        # Reset pointer before file operations
        self.file.seek(0)

        # Save the file in the destination folder
        self.file_utilities.save_file_in_destination_folder(self.file, self.base_path_upload)

        # Extract metadata from the uploaded file
        metadata_dict = self.file_utilities.get_metadata(self.file.name, self.base_path_upload)
        logger.info(f"Metadata extracted successfully for {self.file.name}")

        # Add version information to the metadata and category ID
        logger.info(f"Checking if the file version {self.file.name} already exists in the destination folder...")
        versioned_files, self.category_id = self.file_utilities.list_versioned_files(self.file.name, self.base_path_upload)

        # Add version information to the metadata
        if versioned_files:
            self.file_utilities.remove_file(self.file.name, self.base_path_upload)

            updated_file = ""
            for versioned_file in versioned_files:
                if (metadata_dict['file_creation_date'] <= versioned_file['file_creation_date'] and
                        metadata_dict['file_modified_date'] < versioned_file['file_modified_date']):
                    logger.info(f"File {self.file.name} already exists in the destination folder.")
                    updated_file = versioned_file['file_name']

            if updated_file:
                return (
                    f"Seems like you are trying to upload an older version of {updated_file}. "
                    f"Please check the updated file in the destination folder.",
                    self.flag
                )
            else:
                self.flag = True
                return (
                    f"Seems like you are trying to upload a new version of {versioned_files[0]['file_name']}. "
                    f"Please check the older file in the destination folder. "
                    f"If you want to update the file, please click on continue.",
                    self.flag
                )

        # Store metadata in the database
        try:
            count = FileMetadataDatabaseUtility().check_file_hash(metadata_dict['file_hash'])

            if count > 0:
                self.file_utilities.remove_file(self.file.name, self.base_path_upload)
                return f"File {self.file.name} already exists in the database.", self.flag

            FileMetadataDatabaseUtility().insert_file_info(metadata_dict, file_category=self.file_category, category_id=self.category_id)
            logger.info(f"Metadata stored successfully for {self.file.name}")

            return "File uploaded successfully!", self.flag
        except Exception as e:
            self.file_utilities.remove_file(self.file.name, self.base_path_upload)
            logger.error(f"Error storing metadata: {e}")
            raise HTTPException(status_code=500, detail=f"Error storing metadata: {e}")

    # Insert metadata into the database after confirmation.
    def insert_metadata(self):
        """
        Insert metadata into the database after confirmation.
        :return: A tuple (message, flag) indicating the result.
        """
        # 🔁 Reset pointer before file operations
        self.file.seek(0)

        # Save the file in the destination folder
        self.file_utilities.save_file_in_destination_folder(self.file, self.base_path_upload)

        # Extract metadata from the uploaded file
        metadata_dict = self.file_utilities.get_metadata(self.file.name, self.base_path_upload)
        logger.info(f"Metadata extracted successfully for {self.file.name}")


        metadata_dict['version_file'] = self.file_utilities.extract_version(self.file.name)

        # Store metadata in the database
        try:
            count = FileMetadataDatabaseUtility().check_file_hash(metadata_dict['file_hash'])

            if count > 0:
                self.file_utilities.remove_file(self.file.name, self.base_path_upload)
                return f"File {self.file.name} already exists in the database.", self.flag

            FileMetadataDatabaseUtility().insert_file_info(metadata_dict, file_category=self.file_category, category_id=self.category_id)
            logger.info(f"Metadata stored successfully for {self.file.name}")

            return "File uploaded successfully!", self.flag

        except Exception as e:
            self.file_utilities.remove_file(self.file.name, self.base_path_upload)
            logger.error(f"Error storing metadata: {e}")
            raise HTTPException(status_code=500, detail=f"Error storing metadata: {e}")


# Local testing
if __name__ == "__main__":

    sample_file = UploadFile(
        filename="Scan May 5, 2025.pdf",
        file=BytesIO(open(r"C:\Users\Karnatapus\Downloads\Scan May 5, 2025.pdf", 'rb').read())
    )

    uploader = FileUploader("YourCategoryNameHere", sample_file)  # Replace with a valid category
    print(uploader.upload_single_file())
