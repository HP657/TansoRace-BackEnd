import os, uvicorn, pymysql, bcrypt, datetime, jwt, openai, json

os, uvicorn, pymysql, bcrypt, datetime, jwt, openai, json = (
    os,
    uvicorn,
    pymysql,
    bcrypt,
    datetime,
    jwt,
    openai,
    json
)

from datetime import datetime, timedelta

datetime, timedelta = datetime, timedelta

from pydantic import BaseModel

BaseModel = BaseModel

from typing import Union

Union = Union

from PIL import Image

Image = Image

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf

tf = tf

import numpy as np

np = np

import pandas as pd
pd = pd

from sentence_transformers import SentenceTransformer

SentenceTransformer = SentenceTransformer

from sklearn.metrics.pairwise import cosine_similarity

cosine_similarity = cosine_similarity
