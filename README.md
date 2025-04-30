# WriterData
Python модуль, который позволяет записывать на данный о пользователях, введенных с клавиатуры или сгенерированных автоматически.
## Использование

### Пример получения готового файла архива, через промежуточный файл csv.
Если необходим только csv файл, сжатие файла можно не делать.
в методе compress_csv_file, есть необязательный параметр delete_source_file отвечающий за удаления файла исходного файла.

```python
from writer1.writer_data import WriterData

writer_data = WriterData(count_line=2000)
file_name = writer_data.write_fake_data_to_file_csv()
writer_data.compress_csv_file(file_name)
```
### Пример получения готового файла архива, напрямую в zip файл.

```python
from writer1.writer_data import WriterData

writer_data = WriterData(count_line=2000)
writer_data.compress_auto_generate()
```
### Пример получения готового файла архива, заданного с клавиатуры.

```python
from writer1.writer_data import WriterData

writer_data = WriterData(count_line=2000)
writer_data.compress_keyboard()
```

