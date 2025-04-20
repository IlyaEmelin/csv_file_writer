from faker import Faker
import logging

from writer.formater import Formater

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    formater = Formater(count_line=2)

    # formater.write_to_file_csv()
    # formater.compress_csv_file()

    formater.compress_keyboard()

    # formater.compress_auto_generate()
    # compress_auto_generate
