import requests
import time
import json
import threading
import os
from dotenv import load_dotenv

class DataProcessor:
    # Load environment variables
    load_dotenv()
    API_URL = os.getenv("API_URL")
    @staticmethod
    def fetch_page(page, all_res_list):
        url = f"{DataProcessor.API_URL}{page}"
        response = requests.get(url)
        response_dict = json.loads(response.text)
        if 'models' in response_dict:
            all_res_list.extend(response_dict['models'])
        time.sleep(3)

    @staticmethod
    def fetch(pages):
        print(f"fetching from {DataProcessor.API_URL}...")
        all_res_list = []
        threads = [] 
        for i in range(1, pages + 1):
            thread = threading.Thread(target=DataProcessor.fetch_page, args=(i, all_res_list))
            threads.append(thread)
            thread.start()
            if len(threads) >= 5:
                for t in threads:
                    t.join()
                threads = []
        
        for t in threads:
            t.join()
        
        print("\ndatas fetched successfully")
        return all_res_list
