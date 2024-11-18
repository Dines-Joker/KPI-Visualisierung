import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import config

def connect_to_cosmos(container_id=None):
    """Connects to Cosmos DB and returns the specified container."""
    client = cosmos_client.CosmosClient(config.settings['host'], {'masterKey': config.settings['master_key']})
    try:
        db = client.get_database_client(config.settings['database_id'])
        container = db.get_container_client(container_id if container_id else config.settings['container_id'])
        print(f"Connected to Cosmos DB container '{container_id}' successfully.")
        return container
    except exceptions.CosmosResourceExistsError:
        print(f"Failed to connect to Cosmos DB container '{container_id}'.")
        return None
