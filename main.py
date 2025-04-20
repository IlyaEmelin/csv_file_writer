from faker import Faker
import logging

from writer.formater import Formater

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    formater = Formater()
    formater.write_to_file_csv()
    formater.compress_csv_file()
