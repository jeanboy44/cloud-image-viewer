import numpy as np
import pandas as pd
from pathlib import Path
import imgaug as ia
import imgaug.augmenters as iaa
from PIL import Image

import streamlit as st
from lxml import etree
from pathlib import Path
from xml.etree import ElementTree
from azure.storage.blob import BlobServiceClient
import imgaug as ia
import imgaug.augmenters as iaa

from constants import EXTS, DEFAULT_DIR

XML_EXT = ".xml"
ENCODE_METHOD = "utf-8"
# @st.cache(
#     allow_output_mutation=True,
#     hash_funcs={"_thread.RLock": lambda _: None, "builtins.weakref": lambda _: None},
# )


class SessionStateHandler:
    """Session state handler
    Consider session states as global variables
    """

    def __init__(self):
        """"""

    @classmethod
    def initialize(cls):
        cls.initialize_session_state("connector", Connector())
        cls.initialize_session_state("loaded_data", None)
        cls.initialize_session_state("filtered_data", None)

        cls.initialize_session_state("repo", "Local", slider=True)
        cls.initialize_session_state("root_dir", DEFAULT_DIR, slider=True)
        cls.initialize_session_state("show_annot", False, slider=True)
        cls.initialize_session_state("show_annot_only", False, slider=True)
        cls.initialize_session_state("annotation_dir", "", slider=True)
        cls.initialize_session_state("annotation_dir", "", slider=True)

    @staticmethod
    def initialize_session_state(name, value, slider=False):
        """initailize streamlit session state

        if slider is True,
        this does some tricks to assures that session state is not refreshed when restarted
        this should be used with Callback function for streamlit slider function.
        example)
            def handle_change():
                st.session_state[f"{name}"_] = st.session_state[name]
        """

        if slider is False:
            if name not in st.session_state:
                st.session_state[name] = value

        else:
            # if name not in st.session_state:
            #     st.session_state[f"{name}_"] = value
            #     st.session_state[name] = value
            # else:
            #     st.session_state[name] = st.session_state[f"{name}_"]

            # if "level_1" not in st.session_state:
            #     # Initialize to the saved value in session state if it's available
            #     if "level_1_slider" in st.session_state:
            #         st.session_state.level_1 = st.session_state.level_1_slider
            #     else:
            #         st.session_state.level_1 = 1
            #         st.session_state.level_1_slider = 1
            if name not in st.session_state:
                if f"{name}_" in st.session_state:
                    st.session_state[name] = st.session_state[f"{name}_"]
                else:
                    st.session_state[f"{name}_"] = value
                    st.session_state[name] = value

    @staticmethod
    def root_dir_entered():
        st.session_state.root_dir_ = st.session_state.root_dir
        for key in st.session_state.keys():
            if (key[:5] == "level") & (key[-1] == "_"):
                del st.session_state[f"{key}"]

    @staticmethod
    def level_selected():
        for key in st.session_state.keys():
            if (key[:5] == "level") & (key[-1] == "_"):
                st.session_state[key] = st.session_state[key[:-1]]

    @staticmethod
    def repo_on_change():
        st.session_state.repo_ = st.session_state.repo

    @staticmethod
    def annotation_dir_changed():
        st.session_state.annotation_dir = st.session_state.annotation_dir_

    @staticmethod
    def show_annot_clicked():
        st.session_state.show_annot = st.session_state.show_annot_

    @staticmethod
    def show_annot_only_clicked():
        st.session_state.show_annot_only = st.session_state.show_annot_only_


# Load data and images
class Connector:
    def __init__(self):
        """"""
        self._connected = True
        self.connected_icon = "✅"
        self.name = "Local"
        self.type = "local"
        self.conn = None
        self.default_dir = DEFAULT_DIR

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, value):
        self._connected = value
        if value is True:
            self.connected_icon = "✅"
        else:
            self.connected_icon = "🚫"

    def connect(self, name):
        type_ = st.secrets[name]["type"]
        if type_ == "local":
            self.conn = None
            self.name = name
            self.type = type_
            self.connected = True
            self.default_dir = DEFAULT_DIR
        elif type_ == "azure":
            conn_str = st.secrets[name]["conn_str"]
            container = st.secrets[name]["container"]
            blob_service_client = BlobServiceClient.from_connection_string(conn_str)
            self.conn = blob_service_client.get_container_client(container)
            self.name = name
            self.type = type_
            self.connected = True
            self.default_dir = ""
        else:
            raise ValueError("Unsupported Connection Type")

        # print(self.name)
        # print(self.type)
        # print(self.aaa)
        # st.write(self.name)
        # st.write(self.type)
        # st.write(self.aaa)


@st.cache
def load_data(root_dir, connector):
    if connector.type == "local":
        # load data
        paths = []
        for path in Path(root_dir).rglob("*"):
            if path.suffix in EXTS:
                paths.append(str(path.as_posix()))

        # parse data
        df = pd.DataFrame({"path": paths})
        df["dir"] = [str(Path(path).parent.as_posix()) for path in df.path]
        df["file"] = [str(Path(path).stem) for path in df.path]
        return df
    elif connector.type == "azure":
        paths = []
        for blob in connector.conn.list_blobs(name_starts_with=root_dir):
            # if Path(blob.name) in EXTS:
            paths.append(blob.name)
        df = pd.DataFrame({"path": paths})
        df["dir"] = [str(Path(path).parent.as_posix()) for path in df.path]
        df["file"] = [str(Path(path).stem) for path in df.path]
        return df
    else:
        raise ValueError("Not supported connection.")


# Functions
@st.cache
def load_image(path, connector, resize_ratio=0.2, annotation=False, annotation_dir=""):
    error_msg = None
    seq = iaa.Sequential([iaa.Resize(resize_ratio)])
    if connector.type == "local":
        # with open(path, "rb") as f:
        #     byte = Image
        image = Image.open(path)
    else:
        # with open(path, "rb") as f:
        #     byte = Image
        image = Image.open(path)

    if annotation is True:
        try:

            file_path = str(Path(annotation_dir).joinpath(f"{Path(path).stem}.xml"))
            reader = PascalVocReader(file_path)
            reader.parse_xml()
            # encoded_img = np.fromstring(byte, dtype=np.uint8)
            # image = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
            image = np.asarray(image)
            if len(image.shape) == 2:
                image = np.stack((np.asarray(image),) * 3, axis=-1)
            bbs = ia.BoundingBoxesOnImage(reader.boxes, shape=image.shape)
            images_aug, bbs_aug = seq(images=[image], bounding_boxes=bbs)
            image = bbs_aug.draw_on_image(images_aug[0])
        except Exception as e:
            error_msg = e
            images_aug = seq(images=[np.asarray(image)])
            image = images_aug[0]
    else:
        images_aug = seq(images=[np.asarray(image)])
        image = images_aug[0]

    return image, error_msg


def load_labels():
    """"""
    annots = [f.stem for f in Path(st.session_state.annotation_dir).glob("*.xml")]
    # reader = PascalVocReader(file_path)
    # reader.parse_xml()
    return pd.DataFrame({"file": annots, "annotation": True})


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
