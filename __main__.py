import pandas as pd
import numpy as np
import os
import data_processing.data_loader as dl

if __name__ == "__main__":
    df = dl.generate_dataframe(dl.load_dialog_data())