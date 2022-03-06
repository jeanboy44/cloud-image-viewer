import cv2
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

from constants import EXTS, XML_EXT, DEFAULT_DIR

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

    @staticmethod
    def initialize_session_state(name, value, slider=False):
        """initailize streamlit session state

        if slider is True,
        this does some tricks to assures that session state is not refreshed when restarted
        this should be used with Callback function for streamlit slider function.
        example)
            def handle_change():
                st.session_state[name] = st.session_state[f"{name}"_]
        """

        if slider is False:
            if name not in st.session_state:
                st.session_state[name] = value

        else:
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
        st.session_state.annotation_dir_ = st.session_state.annotation_dir

    @staticmethod
    def show_annot_clicked():
        st.session_state.show_annot_ = st.session_state.show_annot

    @staticmethod
    def show_annot_only_clicked():
        st.session_state.show_annot_only_ = st.session_state.show_annot_only


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


@st.cache
def load_data(root_dir, connector):
    if connector.type == "local":
        paths = []
        for path in Path(root_dir).rglob("*"):
            if path.suffix in EXTS:
                paths.append(str(path.as_posix()))
    elif connector.type == "azure":
        paths = []
        for blob in connector.conn.list_blobs(name_starts_with=root_dir):
            if Path(blob.name).suffix in EXTS:
                paths.append(blob.name)
    else:
        raise ValueError("Not supported connection.")

    # parse data
    df = pd.DataFrame({"path": paths})
    df["dir"] = [str(Path(path).parent.as_posix()) for path in df.path]
    df["file"] = [str(Path(path).stem) for path in df.path]
    return df


# Functions
@st.cache
def load_image(path, connector, resize_ratio=0.2, annotation=False, annotation_dir=""):
    error_msg = None
    seq = iaa.Sequential([iaa.Resize(resize_ratio)])
    if connector.type == "local":
        with open(path, "rb") as f:
            byte = f.read()
    else:
        blob_client = connector.conn.get_blob_client(path)
        byte = blob_client.download_blob().content_as_bytes()
    encoded_img = np.fromstring(byte, dtype=np.uint8)
    image = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    if annotation is True:
        try:

            file_path = str(Path(annotation_dir).joinpath(f"{Path(path).stem}.xml"))
            reader = PascalVocReader(file_path)
            reader.parse_xml()
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


@st.cache
def load_labels(annotation_dir, connector):
    """"""
    if connector.type == "local":
        annots = [f.stem for f in Path(annotation_dir).glob("*{XML_EXT}")]
    elif connector.type == "azure":
        annots = []
        for blob in connector.conn.list_blobs(name_starts_with=annotation_dir):
            if Path(blob.name).suffix == XML_EXT:
                annots.append(blob.name)
    else:
        raise ValueError("Unsupported Connection Type")

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
