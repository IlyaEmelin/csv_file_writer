# WriterData
Python модуль, который позволяет записывать на данный о пользователях, введенных с клавиатуры или сгенерированных автоматически.
## Использование

### Типы генераторов данных
Классы генераторов данных
- **CsvFileGenerator** - генератор данных который вычитывает данные из csv файлов.
- **FakerGenerator** - генератор данных который создает фейковые данные.
- **KeyboardGenerator** - генератор данных который читает их с клавиатуры.

### Проверка сгенерированных данных 
Класс проверки сгенерированных данных
- **CountRow** - проверка количества колонок в каждой строчке
- **GeoChecking** - проверка адресов на валидность на основе www.openstreetmap.org данный валидатор является медленным до 1 секунд на значение.
Применять его на больших данных не стоить.

### Сохранение данных 
Классы которые, сохраняют данные в файл.
По умолчанию все файлы появятся в папке result.  
- **CsvWriter** - результат файл с типом csv.
- **CompressorZipWriter** - результат файл с типом zip, внутри будет лежать файл csv.
- **Compressor7zWriter** - результат файл с типом 7z, внутри будет лежать файл csv.

### Пример использования классов
```python
from checker.geo_checking import GeoChecking
from checker.geo_type import GeoType
from checker.count_row import CountRow
from generator.fake_generator import FakerGenerator
from writer.compressor_7z_writer import Compressor7zWriter
from writer.csv_writer import CsvWriter
from writer.compressor_zip_writer import CompressorZipWriter

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
    index_cols_to_check=(9,),
    checker=GeoChecking(GeoType.FULL_ADDRESS),
)
# Проверка значения почтового кода. Это длительная операция до 1 секунды
# для одного значения
faker_generator.add_checker(
    index_cols_to_check=(8,),
    checker=GeoChecking(GeoType.POSTAL_CODE),
)
# Проверка значения страны. Это длительная операция до 1 секунды
# для одного значения
faker_generator.add_checker(
    index_cols_to_check=(7,),
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
csv_writer = CsvWriter()
csv_writer.write(faker_generator.generate_data(count_line=20))
```

