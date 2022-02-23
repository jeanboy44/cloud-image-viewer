import os
import yaml
from pathlib import Path
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import BlobPrefix

CONFIG_FILE = "config.yml"


class ConfigHandler:
    def __init__(self):
        with open(CONFIG_FILE, mode="r") as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)


class Connector:
    def __init__(self, type="azure"):
        self.connector = None
        self.connection_type = None
        self._connection_info = None

    @property
    def connection_info(self):
        return self._connection_info

    @connection_info.setter
    def connection_info(self, value):
        self._connection_info = value
        if value is not None:
            self.connection_type = value["type"]

    def connect(self, connection_info=None, return_=False):
        if connection_info is None:
            connection_info = self.connection_info
        else:
            self.connection_info = connection_info

        if self.connection_type == "azure":
            connector = self.connect_azure_blob(
                conn_str=self.connection_info["conn_str"],
                container=self.connection_info["container"],
            )
        else:
            connector = None

        if return_ is True:
            return connector
        else:
            self.connector = connector

    def test(self, connection_info=None):
        if connection_info is None:
            connection_info = self.connection_info
        try:
            conn = self.conn.connect(connection_info, return_=True)
            print("Connected Successfully")
            return self.check_connection(connection_info["type"])
        except:
            print("Wrong connection information")
            return False

    def check_connection(self, connection_type=None):
        if connection_type is None:
            connection_type = self.connection_type

        if connection_type == "azure":
            return self.connector.exists()
        elif connection_type == "aws":
            return False

    def test_azure_blob(self, connector):
        return connector.exists()

    def connect_azure_blob(self, conn_str, container):
        blob_service_client = BlobServiceClient.from_connection_string(conn_str)
        container_client = blob_service_client.get_container_client(container)

        return container_client

    def upload(self, src, dst):
        """"""
        if self.connection_type == "azure":
            self.connector.upload_blob(name=dst, data=src)
        elif self.connection_type == "aws":
            return False

    def download(self):
        """"""

    def get_list(self, path):
        """"""
        # print(f"get_list-path: {path}")
        # for item in self.connector.walk_blobs(name_starts_with=path):
        #     if isinstance(item, BlobPrefix):
        #         for item in self.connector.walk_blobs(name_starts_with=item.name):
        #             print("1")
        #             print(isinstance(item, BlobPrefix))
        #             print(type(item))
        #             print(item)
        #     else:
        #         print("2")
        #         print(isinstance(item, BlobPrefix))
        #         print(type(item))
        #         print(item)
        #     # if isinstance(item, BlobPrefix):
        #     #     print(item.name)
        #     #     self._walk_blob_hierarchy(prefix=item.name)
        #     # else:
        #     #     print(item.name)
        if self.connection_type == "azure":
            path_list = []
            isdir_list = []
            for blob in self.connector.walk_blobs(name_starts_with=path):
                path_list.append(blob.name)
                isdir_list.append(isinstance(blob, BlobPrefix))

            # path_list = [
            #     blob.name for blob in self.connector.walk_blobs(name_starts_with=path)
            # ]
            return path_list, isdir_list
        elif self.connection_type == "aws":
            return False