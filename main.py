import logging

# from writer1.writer_data import WriterData
from checker.geo_checking import GeoChecking
from checker.geo_type import GeoType
from checker.count_row import CountRow
from core.path_helper import get_path
from generator.fake_generator import FakerGenerator
from writer.compressor_7z_writer import Compressor7zWriter
from writer.csv_writer import CsvWriter
from writer.compressor_zip_writer import CompressorZipWriter

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # writer_data = WriterData(count_line=2)

    # Пример получения готового файла архива, через промежуточный файл csv.
    # Автогенерация фейковых данных
    # file_name = writer_data.write_fake_data_to_file_csv()
    # writer_data.compress_csv_file(file_name)

    # Пример получения готового файла архива ввод с клавиатуры
    # writer_data.compress_keyboard()

    # Пример получения готового файла архива, автогенерация фейковых данных
    # writer_data.compress_auto_generate()
    # writer_data.test()

    faker_generator = FakerGenerator()

    count_row_checker = CountRow()
    # faker_generator.add_checker(
    #     index_cols_to_check=None,
    #     checker=count_row_checker,
    # )
    # faker_generator.add_checker(
    #     index_cols_to_check=(9,),
    #     checker=GeoChecking(GeoType.FULL_ADDRESS),
    # )
    # faker_generator.add_checker(
    #     index_cols_to_check=(8,),
    #     checker=GeoChecking(GeoType.POSTAL_CODE),
    # )
    # faker_generator.add_checker(
    #     index_cols_to_check=(7,),
    #     checker=GeoChecking(GeoType.COUNTRY),
    # )
    #
    # writer_zip = CompressorZipWriter()
    # writer_zip.write(faker_generator.generate_data(count_line=20))

    writer_7z = Compressor7zWriter()
    writer_7z.write(
        faker_generator.generate_data(
            count_line=500_00,
        ),
        volume=1024 * 256,
    )

    csv_writer = CsvWriter()
    csv_writer.write(faker_generator.generate_data(count_line=500_00))
