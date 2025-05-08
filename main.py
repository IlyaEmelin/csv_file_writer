import logging

from checker.geo_checking import GeoChecking
from checker.geo_type import GeoType
from checker.count_row import CountRow
from generator.fake_generator import (
    FakerGenerator,
    FULL_ADDRESS_INDEX,
    POSTCODE_INDEX,
    COUNTRY_INDEX,
)
from generator.mimesis_generator import MimesisGenerator

from compression.compressor_7z_compressor import Compressor7zCompressor
from compression.compressor_zip_compressor import CompressorZipCompressor

from writer.csv_writer import CsvWriter
from writer.excel_writer import ExcelWriter
from writer.text_writer import TextWriter

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Пример использование создания данных
    # Генератор Fake-данных на основе проекта faker
    # (медленнее в 5 раз проекта mimesis)
    faker_generator = FakerGenerator()

    # Добавление класса который проверяет количество колонок в каждой строчке
    faker_generator.add_checker(
        index_cols_to_check=None,
        checker=CountRow(),
    )
    # Проверка значения полного адреса. Это длительная операция до 1 секунды
    # для одного значения
    faker_generator.add_checker(
        index_cols_to_check=(FULL_ADDRESS_INDEX,),
        checker=GeoChecking(GeoType.FULL_ADDRESS),
    )
    # Проверка значения почтового кода. Это длительная операция до 1 секунды
    # для одного значения
    # faker_generator.add_checker(
    #     index_cols_to_check=(POSTCODE_INDEX,),
    #     checker=GeoChecking(GeoType.POSTAL_CODE),
    # )
    # Проверка значения страны. Это длительная операция до 1 секунды
    # для одного значения
    faker_generator.add_checker(
        index_cols_to_check=(COUNTRY_INDEX,),
        checker=GeoChecking(GeoType.COUNTRY),
    )

    # Запись в csv файл
    csv_writer = CsvWriter()
    csv_writer.write(faker_generator.generate_data(count_line=10))

    # Запись в text файл
    text_writer = TextWriter()
    text_writer.write(faker_generator.generate_data(count_line=10))

    # Запись в excel файл
    text_writer = ExcelWriter()
    text_writer.write(faker_generator.generate_data(count_line=10))

    # Сжатие в ZIP - архив
    writer_zip = CompressorZipCompressor()
    writer_zip.write(
        CsvWriter(),
        faker_generator.generate_data(count_line=10),
    )

    # Сжатие в 7z - архив
    big_writer_7z = Compressor7zCompressor()
    big_writer_7z.write(
        CsvWriter(),
        faker_generator.generate_data(count_line=10),
        volume=1024 * 256,
    )

    # Сжатие в ZIP - архив excel файла
    writer_zip = CompressorZipCompressor()
    writer_zip.write(
        ExcelWriter(),
        faker_generator.generate_data(count_line=10),
    )

    # Сжатие в 7z - архив csv файла c 2_000_000 записей
    # Генератор Fake-данных на основе проекта mimesis (быстрее в 5 раз)
    mimesis_generator = MimesisGenerator()
    big_writer_7z = Compressor7zCompressor()
    big_writer_7z.write(
        CsvWriter(),
        mimesis_generator.generate_data(count_line=2_000_000),
        volume=1024 * 1024 * 16,
    )
