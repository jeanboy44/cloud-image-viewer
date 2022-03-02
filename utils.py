import streamlit as st
from lxml import etree
from xml.etree import ElementTree
from azure.storage.blob import BlobServiceClient
import imgaug as ia
import imgaug.augmenters as iaa

XML_EXT = ".xml"
ENCODE_METHOD = "utf-8"
# @st.cache(
#     allow_output_mutation=True,
#     hash_funcs={"_thread.RLock": lambda _: None, "builtins.weakref": lambda _: None},
# )
def connect(repo):
    if repo == "Local":
        container_client = None
    else:
        conn_str = st.secrets[repo]["conn_str"]
        container = st.secrets[repo]["container"]
        blob_service_client = BlobServiceClient.from_connection_string(conn_str)
        container_client = blob_service_client.get_container_client(container)

    return container_client


class PascalVocReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.boxes = []
        self.verified = False
        try:
            self.parse_xml()
        except:
            pass

    def get_boxes(self):
        return self.boxes

    def add_box(self, label, bnd_box):
        x_min = int(float(bnd_box.find("xmin").text))
        y_min = int(float(bnd_box.find("ymin").text))
        x_max = int(float(bnd_box.find("xmax").text))
        y_max = int(float(bnd_box.find("ymax").text))

        bbox = ia.BoundingBox(x1=x_min, y1=y_min, x2=x_max, y2=y_max, label=label)
        self.boxes.append(bbox)

    def parse_xml(self):
        assert self.file_path.endswith(XML_EXT), "Unsupported file format"
        parser = etree.XMLParser(encoding=ENCODE_METHOD)
        xml_tree = ElementTree.parse(self.file_path, parser=parser).getroot()
        filename = xml_tree.find("filename").text
        try:
            verified = xml_tree.attrib["verified"]
            if verified == "yes":
                self.verified = True
        except KeyError:
            self.verified = False

        for object_iter in xml_tree.findall("object"):
            bnd_box = object_iter.find("bndbox")
            label = object_iter.find("name").text
            self.add_box(label, bnd_box)
        return True


# import os
# import yaml
# from pathlib import Path
# from azure.storage.blob import BlobServiceClient
# from azure.storage.blob import BlobPrefix

# CONFIG_FILE = "config.yml"


# class ConfigHandler:
#     def __init__(self):
#         with open(CONFIG_FILE, mode="r") as f:
#             self.config = yaml.load(f, Loader=yaml.FullLoader)


# class Connector:
#     def __init__(self, type="azure"):
#         self.connector = None
#         self.connection_type = None
#         self._connection_info = None

#     @property
#     def connection_info(self):
#         return self._connection_info

#     @connection_info.setter
#     def connection_info(self, value):
#         self._connection_info = value
#         if value is not None:
#             self.connection_type = value["type"]

#     def connect(self, connection_info=None, return_=False):
#         if connection_info is None:
#             connection_info = self.connection_info
#         else:
#             self.connection_info = connection_info

#         if self.connection_type == "azure":
#             connector = self.connect_azure_blob(
#                 conn_str=self.connection_info["conn_str"],
#                 container=self.connection_info["container"],
#             )
#         else:
#             connector = None

#         if return_ is True:
#             return connector
#         else:
#             self.connector = connector

#     def test(self, connection_info=None):
#         if connection_info is None:
#             connection_info = self.connection_info
#         try:
#             conn = self.conn.connect(connection_info, return_=True)
#             print("Connected Successfully")
#             return self.check_connection(connection_info["type"])
#         except:
#             print("Wrong connection information")
#             return False

#     def check_connection(self, connection_type=None):
#         if connection_type is None:
#             connection_type = self.connection_type

#         if connection_type == "azure":
#             return self.connector.exists()
#         elif connection_type == "aws":
#             return False

#     def test_azure_blob(self, connector):
#         return connector.exists()

#     def connect_azure_blob(self, conn_str, container):
#         blob_service_client = BlobServiceClient.from_connection_string(conn_str)
#         container_client = blob_service_client.get_container_client(container)

#         return container_client

#     def upload(self, src, dst):
#         """"""
#         if self.connection_type == "azure":
#             self.connector.upload_blob(name=dst, data=src)
#         elif self.connection_type == "aws":
#             return False

#     def download(self, src, dest):
#         """"""
#         blob_client = self.connector.get_blob_client(src)
#         with open(dest, "wb") as download_file:
#             download_file.write(blob_client.download_blob().readall())

#     def get_list(self, path):
#         """"""
#         # print(f"get_list-path: {path}")
#         # for item in self.connector.walk_blobs(name_starts_with=path):
#         #     if isinstance(item, BlobPrefix):
#         #         for item in self.connector.walk_blobs(name_starts_with=item.name):
#         #             print("1")
#         #             print(isinstance(item, BlobPrefix))
#         #             print(type(item))
#         #             print(item)
#         #     else:
#         #         print("2")
#         #         print(isinstance(item, BlobPrefix))
#         #         print(type(item))
#         #         print(item)
#         #     # if isinstance(item, BlobPrefix):
#         #     #     print(item.name)
#         #     #     self._walk_blob_hierarchy(prefix=item.name)
#         #     # else:
#         #     #     print(item.name)
#         if self.connection_type == "azure":
#             path_list = []
#             isdir_list = []
#             for blob in self.connector.walk_blobs(name_starts_with=path):
#                 path_list.append(blob.name)
#                 isdir_list.append(isinstance(blob, BlobPrefix))

#             # path_list = [
#             #     blob.name for blob in self.connector.walk_blobs(name_starts_with=path)
#             # ]
#             return path_list, isdir_list
#         elif self.connection_type == "aws":
#             return False


# class FileSystem:
#     def __init__(self):
#         self.name =None

#     def get_list(self, dir):
#         """"""
#         path_list = []
#         isdir_list = []
#         for path in Path(dir).glob("*"):
#             print(path)
#             path_list.append(path)
#             isdir_list.append(os.path.isdir(path))

#         return path_list, isdir_list
