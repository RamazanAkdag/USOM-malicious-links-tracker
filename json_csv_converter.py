import csv
import datetime
import os

class JsonCsvConverter:

     @staticmethod
     def convertToCsvFile(data_list, headers):
        print("converting to csv file...")

        directory = "data"
        if not os.path.exists(directory):
            os.makedirs(directory)

        today = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
        filename = os.path.join(directory, f"data_{today}.csv")

        with open(filename, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, headers)
            dict_writer.writeheader()
            dict_writer.writerows(data_list)
            print("converted successfully to ", output_file.name)
        
        return filename
        
        
