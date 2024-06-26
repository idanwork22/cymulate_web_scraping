from pymongo import MongoClient, errors
from src.base import LoguruLogger


class MongoDBClient:
    def __init__(self, connection_string, database_name, collection_name):
        self.connection_string = connection_string
        self.database_name = database_name
        self.collection_name = collection_name
        self.logger = LoguruLogger(__name__).get_logger()
        self.client = None
        self.db = None
        self.collection = None
        self.connect()

    def connect(self):
        """
        Tries to connect to the MongoDB server with the provided connection string
        and sets up the database and collection.
        :return: True if connection is successful, False otherwise
        """
        try:
            self.client = MongoClient(self.connection_string)
            # Attempt to fetch server information to confirm connection
            self.client.server_info()
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            self.logger.debug("Connection to MongoDB successful")
            return True
        except errors.ServerSelectionTimeoutError as err:
            self.logger.debug(f"Connection failed: {err}")
            return False

    def insert_document(self, document):
        """
        Inserts a list of documents into the collection one by one.
        :param document:
        :return: Inserted IDs of the documents
        """
        self.logger.info("Check if the documents already exists")
        result = self.collection.insert_one(document)
        self.logger.debug(
            f"Inserted document into {self.database_name}.{self.collection_name}")
        return result.inserted_id

    def update_document(self, query, new_values):
        """
        Updates a document in the collection based on the given query.

        :param query: Dictionary query to find the document to be updated
        :param new_values: Dictionary with the new values
        :return: Modified count
        """
        result = self.collection.update_one(query,new_values)
        self.logger.debug(
            f"Updated document in {self.database_name}.{self.collection_name} with query {query} and new values {new_values}")
        return result.modified_count

    def delete_documents(self, query):
        """
        Deletes documents in the collection based on the given query.

        :param query: Dictionary query to delete documents
        :return: Deleted count
        """
        result = self.collection.delete_many(query)
        self.logger.debug(
            f"Deleted {result.deleted_count} documents from {self.database_name}.{self.collection_name} with query {query}")
        return result.deleted_count

    def list_collections(self):
        """
        Lists all collections in the database.

        :return: List of collection names
        """
        collections = self.db.list_collection_names()
        self.logger.debug(f"Listed collections in {self.database_name}: {collections}")
        return collections

    def list_databases(self):
        """
        Lists all databases in the MongoDB server.

        :return: List of database names
        """
        databases = self.client.list_database_names()
        self.logger.debug(f"Listed databases: {databases}")
        return databases

    def get_all_documents(self):
        """
        Retrieves all documents from the collection.

        :return: List of documents
        """
        documents = list(self.collection.find())
        self.logger.debug(f"Retrieved all documents from {self.database_name}.{self.collection_name}")
        return documents
