from faker import Faker
import logging

from writer.writer_data import WriterData

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    writer_data = WriterData(count_line=2000)

    # Пример получения готового файла архива, через промежуточный файл csv.
    # Автогенерация фейковых данных
    file_name = writer_data.write_fake_data_to_file_csv()
    writer_data.compress_csv_file(file_name)

    # Пример получения готового файла архива ввод с клавиатуры
    # writer_data.compress_keyboard()

    # Пример получения готового файла архива, автогенерация фейковых данных
    writer_data.compress_auto_generate()
