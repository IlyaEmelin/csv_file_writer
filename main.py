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
from writer.compressor_7z_writer import Compressor7zWriter
from writer.csv_writer import CsvWriter
from writer.compressor_zip_writer import CompressorZipWriter

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # Пример использование создания данных
    # Генератор Fake-данных
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
    faker_generator.add_checker(
        index_cols_to_check=(POSTCODE_INDEX,),
        checker=GeoChecking(GeoType.POSTAL_CODE),
    )
    # Проверка значения страны. Это длительная операция до 1 секунды
    # для одного значения
    faker_generator.add_checker(
        index_cols_to_check=(COUNTRY_INDEX,),
        checker=GeoChecking(GeoType.COUNTRY),
    )

    # Сжатие в ZIP - архив
    writer_zip = CompressorZipWriter()
    writer_zip.write(faker_generator.generate_data(count_line=20))

    # Сжатие в 7z - архив
    writer_7z = Compressor7zWriter()
    writer_7z.write(
        faker_generator.generate_data(
            count_line=20,
        ),
        volume=1024 * 256,
    )

    # без сжатия напрямую в Csv файл
    # from datetime import datetime
    #
    # now = datetime.now()
    #
    csv_writer = CsvWriter()
    csv_writer.write(faker_generator.generate_data(count_line=20))
    #
    # print("Time delta:", datetime.now() - now)
