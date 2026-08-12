from Pipeline.database.postgres_conn import postgres_conn

import numpy as np
import pandas as pd

def db_data():

    conn = postgres_conn()


    query = 