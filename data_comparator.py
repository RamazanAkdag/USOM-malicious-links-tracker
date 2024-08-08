import pandas as pd

class DataComparator:

    @staticmethod
    def compare(newFile, oldFile):
        print("comparing ", newFile, " and ", oldFile, "files...")
        df_new = pd.read_csv(newFile)
        df_old = pd.read_csv(oldFile)
        
        new_entries = df_new[~df_new['id'].isin(df_old['id'])]
        print("files compared successfully...")
        return new_entries

