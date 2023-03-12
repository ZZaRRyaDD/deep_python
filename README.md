Создание виртуального окружения и установка зависимостей:

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Запуск тестов:

```bash
pytest
```

Получение отчета о покрытии тестами:

```bash
coverage run -m pytest
coverage report -m
coverage html 
```

Проверка линтерами:

```bash
flake8 ./homework_*
pylint ./homework_*
```
