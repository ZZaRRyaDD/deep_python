# Результаты

## 1. Сравнение использования weakref и слотов

### Запуск

```py
python compare_classes_cru.py
```

### Прогон классов с обычными атрибутами:

![Обычные атрибуты](screenshots/simple_classes_cru.png)

### Прогон классов со слотами:

![Слоты](screenshots/slots_classes_cru.png)

### Прогон классов со слабыми ссылками:

![Слабые ссылки](screenshots/weakref_classes_cru.png)

## 2. Профилирование

### Запуск

```py
python -m memory_profiler compare_classes_memory.py
```

### Прогон классов с обычными атрибутами:

![Обычные атрибуты](screenshots/simple_classes_memory.png)

### Прогон классов со слотами:

![Слоты](screenshots/slots_classes_memory.png)

### Прогон классов со слабыми ссылками:

![Слабые ссылки](screenshots/weakref_classes_memory.png)