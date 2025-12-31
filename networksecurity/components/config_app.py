from dataclasses import dataclass
import networksecurity.components.constants as constants


@dataclass
class MongoDBAtlasConfig:
    """Configuration object to store ingestion metadata."""
    mongo_db_uri: str = constants.MONGO_DB_URI
    db_name: str = constants.MONGO_DB
    collection_name: str = constants.MONGO_DB_COLLECTION
    file_path: str = constants.network_data_file_and_path