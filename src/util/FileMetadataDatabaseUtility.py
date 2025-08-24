# Import necessary libraries
import psycopg2
from src.conf.Configurations import logger, db_config
from fastapi import HTTPException


class FileMetadataDatabaseUtility:
    """
    This class is responsible for managing the file metadata database.
    """

    def __init__(self):
        """
        This function initializes the FileMetadataDatabaseUtility class with the specified database configuration.
        """
        try:

            # Set the database configuration
            self.conn = psycopg2.connect(**db_config)
            self.cursor = self.conn.cursor()

        except Exception as e:
            logger.error(f"Error connecting to the database: {e}")
            raise HTTPException(status_code=500, detail=f"Error connecting to the database: {e}")

        # Create the table if it doesn't exist
        self.__create_table()

    # Create the file_properties table
    def __create_table(self):
        """
        Create the file_metadata table if it doesn't exist.
        """
        try:
            # Drop the table if it exists
            logger.info("Creating table if it doesn't exist...")
            self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS file_properties (
                        id SERIAL PRIMARY KEY,
                        file_name TEXT NOT NULL,
                        file_type TEXT NOT NULL,
                        file_category TEXT NOT NULL,
                        file_size NUMERIC,
                        source_path TEXT,
                        destination_path TEXT NOT NULL,
                        file_creation_date TIMESTAMP,
                        file_modified_date TIMESTAMP,
                        file_hash TEXT,
                        created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        created_by TEXT,
                        version_file TEXT DEFAULT '0',
                        category_id integer

                    );
               """)

        except Exception as e:
            logger.error(f"Error during table creation: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during table creation: {e}")

    # Insert file metadata into the database
    def insert_file_info(self, file_info: dict, file_category: str, category_id: int):
        """
        Insert file metadata into the database.

        :param file_info: A dictionary containing file metadata.
        :param file_category: The category of the file.
        :param category_id: The ID of the category.
        :return: None
        """
        try:

            logger.info(f"Inserting file metadata for: {file_info['file_name']}")
            insert_query = """
              INSERT INTO file_properties  (
                  file_name, file_type,file_category, file_size, 
                  source_path, destination_path,
                  file_creation_date, file_modified_date, 
                  file_hash, created_on, created_by, version_file, category_id
              )VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """

            # Prepare the values to be inserted
            values = (
                file_info['file_name'],
                file_info['file_type'],
                file_category,
                file_info['file_size'],
                file_info['source_path'],
                file_info['destination_path'],
                file_info['file_creation_date'],
                file_info['file_modified_date'],
                file_info['file_hash'],
                file_info['created_on'],
                file_info['created_by'],
                file_info.get('version_file', '0'),
                category_id


            )
            self.cursor.execute(insert_query, values)
            self.conn.commit()

        except Exception as e:
            logger.error(f"Error inserting file metadata: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during file metadata insertion: {e}")

        finally:
            # Close the cursor
            self.cursor.close()
            # Close the connection
            self.conn.close()

    # Check if the file hash already exists in the database
    def check_file_hash(self, file_hash: str):
        """
        Check if the file hash already exists in the database.

        :param file_hash: The hash of the file to check.
        :return: True if the hash exists, False otherwise.
        """
        try:
            logger.info(f"Checking if file hash exists: {file_hash}")
            select_query = "SELECT count(*) FROM file_properties WHERE file_hash = %s;"

            self.cursor.execute(select_query, (file_hash,))

            count = self.cursor.fetchone()[0]

            return count

        except Exception as e:
            logger.error(f"Error checking file hash: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during file hash check: {e}")
        finally:
            # Close the cursor
            self.cursor.close()
            # Close the connection
            self.conn.close()

    # Retrieve all file names and their associated categories from the database
    def get_all_file_names_and_categories(self):
        """
        Retrieve all file names and their associated categories from the database.

        :return: A list of all file names.
        """

        try:
            logger.info("Retrieving all file names from the database.")
            select_query = "SELECT file_name, category_id FROM file_properties;"
            self.cursor.execute(select_query)
            file_names = [row for row in self.cursor.fetchall()]
            return file_names

        except Exception as e:
            logger.error(f"Error retrieving file names: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during file name retrieval: {e}")
        finally:
            # Close the cursor
            self.cursor.close()
            # Close the connection
            self.conn.close()

    def insert_file_obj(self):
        """
        Insert a file object into the database.
        :return: None
        CREATE TABLE document_blob (
            id SERIAL PRIMARY KEY,
            data BYTEA,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );

        """
        try:
            with open("C:\\SOURCE_PATH\\abc.pdf", 'rb') as f:
                file_data = f.read()

            self.cursor.execute(
                "INSERT INTO document_blob (data) VALUES (%s)",
                (Binary(file_data),)
            )
            self.conn.commit()
            print(f"File inserted successfully..")

        except (Exception, psycopg2.Error) as error:
            print(f"Error inserting file: {error}")

        finally:
            if self.conn:
                self.cursor.close()
                self.conn.close()

    def read_file_obj(self):
        """
        Read a file object from the database.
        :return: The file data.
        """
        try:
            self.cursor.execute("SELECT data FROM document_blob WHERE id = %s", (1,))
            file_data = self.cursor.fetchone()[0]

            with open("C:\\DESTINATION_PATH\\surendra.pdf", 'wb') as f:
                f.write(file_data)

            print(f"File read and saved successfully..")

        except (Exception, psycopg2.Error) as error:
            print(f"Error reading file: {error}")

        finally:
            if self.conn:
                self.cursor.close()
                self.conn.close()

if __name__ == "__main__":

    # Example usage
    file_metadata_db = FileMetadataDatabaseUtility()

    # check file hash
    # sample_file_hash = '589c018004c4ea9186fc9e99079c75ab'

    sample_file_hash = "abc"

    res = file_metadata_db.check_file_hash(sample_file_hash)

    print(res)
