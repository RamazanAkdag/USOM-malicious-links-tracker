from fetcher import DataProcessor
from json_csv_converter import JsonCsvConverter
from data_comparator import DataComparator
import os
import dotenv
from mail import MailSender

def main():
    # load env file
    dotenv.load_dotenv()

    data = DataProcessor.fetch(5)
    if not data:
        print("No data fetched.")
        return

    headers = data[0].keys()
    file = JsonCsvConverter.convertToCsvFile(data, headers)

    data_dir = "/app/data"
    files = sorted(os.listdir(data_dir), reverse=True)
    print(files)
  
    if len(files) < 2:
        print("Error: files count is not enough to compare")
    else:
        file1 = os.path.join(data_dir, files[1])
        file2 = os.path.join(data_dir, files[0])
        diff = DataComparator.compare(file2, file1)

        # for sending mail
        diff_filename = os.getenv("MAIL_FILE", "diff.csv")
        diff.to_csv(diff_filename, index=False)

        MailSender.sendMail(diff_filename)

        os.remove(diff_filename)
        print(f"Deleted the difference file: {diff_filename}")
        delete_file = os.path.join(data_dir, files[-1])
        os.remove(delete_file)
        print(f"Deleted the latest file: {delete_file}")

if __name__ == "__main__":
    main()

    
