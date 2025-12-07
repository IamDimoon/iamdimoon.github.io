import datetime
from decimal import Decimal

DATE_FORMAT = '%Y-%m-%d'


def add(items, title, amount, expiration_date=None):
    """
    Добавляет продукт в словарь goods.
    
    Args:
        items: словарь goods
        title: название продукта
        amount: количество продукта (Decimal для весовых, int для штучных)
        expiration_date: срок годности (строка в формате DATE_FORMAT или None)
    """
    # Проверяем,на налмичие него словаре
    if title not in items:
        items[title] = []
    
    # Если дата передана как строка, преобразуем её
    if isinstance(expiration_date, str):
        expiration_date = datetime.datetime.strptime(expiration_date, DATE_FORMAT).date()
    
    # 
    items[title].append({
        'amount': Decimal(str(amount)),
        'expiration_date': expiration_date
    })


def add_by_note(items, note):
    parts = note.split()
    
    # Если частей меньше 2 то все непр
    if len(parts) < 2:
        return
    
    date_str = None
    try:
        datetime.datetime.strptime(parts[-1], DATE_FORMAT)
        date_str = parts[-1]
        # Убираем дату из частей
        parts = parts[:-1]
    except ValueError:
        # Последняя часть - не дата
        pass
    
    try:
        amount_value = Decimal(parts[-1])
        title = ' '.join(parts[:-1])
    except:
        try:
            amount_value = int(parts[-1])
            title = ' '.join(parts[:-1])
        except:
            title = ' '.join(parts)
            amount_value = Decimal('1')
    
    # Вызываем функцию add c этой хуйнёй
    add(items, title, amount_value, date_str)


def find(items, needle):
    # ААААА67 67 67 
    result = []
    needle_lower = needle.lower()
    
    # Перебираем все ключи (названия продуктов)
    for title in items:
        if needle_lower in title.lower():
            result.append(title)
    
    return result


def amount(items, needle):
    # Находим все продукты, с needle
    found_products = find(items, needle)
    
    if not found_products:
        return Decimal('0')
    
    total = Decimal('0')
    
    # Суммируем количество из всех партий найденных продуктов
    for product in found_products:
        for batch in items[product]:
            total += batch['amount']
    
    return total


# Тестирование программы
if __name__ == "__main__":
    # Создаём словарь goods с начальными данными
    goods = {
        'Пельмени Универсальные': [
            {'amount': Decimal('0.5'), 'expiration_date': datetime.date(2023, 7, 15)},
            {'amount': Decimal('2'), 'expiration_date': datetime.date(2023, 8, 1)},
        ],
        'Вода': [
            {'amount': Decimal('1.5'), 'expiration_date': None}
        ],
    }
    
    print("Начальное состояние холодильника:")
    for product, batches in goods.items():
        print(f"{product}:")
        for batch in batches:
            print(f"  - {batch['amount']}, годен до: {batch['expiration_date']}")
    
    print("\n" + "="*50 + "\n")
    
    print("1. Тестируем функцию add():")
    
    # Добавляем новый продукт без даты
    add(goods, 'Молоко', Decimal('1.0'), None)
    print("Добавлено Молоко 1.0 без даты")
    
    # продукт удже датой как строкой
    add(goods, 'Сыр', Decimal('0.3'), '2023-10-10')
    print("Добавлен Сыр 0.3 с датой '2023-10-10'")
    
    # datetime.date
    add(goods, 'Яйца', 10, datetime.date(2023, 7, 20))
    print("Добавлены Яйца 10 шт с датой datetime.date(2023, 7, 20)")
    
    # новая партия
    add(goods, 'Пельмени Универсальные', Decimal('1.5'), '2023-08-15')
    print("Добавлена новая партия Пельмени Универсальные 1.5 с датой '2023-08-15'")
    
    # дата на будущее
    add(goods, 'Консервы', 5, '2123-12-31')
    print("Добавлены Консервы 5 шт с датой '2123-12-31' (через 100 лет)")
    
    print("\n" + "="*50 + "\n")
    
    print("2. Тестируем функцию add_by_note():")
    
    # заметка
    add_by_note(goods, "Колбаса 0.5")
    print("Добавлено по заметке: 'Колбаса 0.5'")
    
    # Заметка с датой
    add_by_note(goods, "Хлеб 1 2023-07-10")
    print("Добавлено по заметке: 'Хлеб 1 2023-07-10'")
    
    # Заметка с названием из нескольких слов
    add_by_note(goods, "Сок яблочный 1.0 2023-09-01")
    print("Добавлено по заметке: 'Сок яблочный 1.0 2023-09-01'")
    
    # Заметка с целым числом
    add_by_note(goods, "Йогурт 4 2023-07-05")
    print("Добавлено по заметке: 'Йогурт 4 2023-07-05'")
    
    print("\n" + "="*50 + "\n")
    
    # find
    print("3. Тестируем функцию find():")
    
    print("Поиск 'пель' (регистр не важен):", find(goods, 'пель'))
    print("Поиск 'ПЕЛЬМЕНИ':", find(goods, 'ПЕЛЬМЕНИ'))
    print("Поиск 'вода':", find(goods, 'вода'))
    print("Поиск 'сыр':", find(goods, 'сыр'))
    print("Поиск 'сок':", find(goods, 'сок'))
    print("Поиск 'несуществующий':", find(goods, 'несуществующий'))
    
    print("\n" + "="*50 + "\n")
    
    print("4. Тестируем функцию amount():")
    
    print("Общее количество пельменей:", amount(goods, 'Пельмени'))
    print("Общее количество воды:", amount(goods, 'Вода'))
    print("Общее количество молока:", amount(goods, 'Молоко'))
    print("Общее количество сыра:", amount(goods, 'Сыр'))
    print("Общее количество яиц:", amount(goods, 'Яйца'))
    print("Общее количество сока:", amount(goods, 'Сок'))
    
    print("\n" + "="*50 + "\n")
    
    # итог
    print("Финальное состояние холодильника:")
    print("-" * 30)
    
    for product, batches in sorted(goods.items()):
        total = sum(batch['amount'] for batch in batches)
        print(f"{product}: {total} (партий: {len(batches)})")
        for batch in batches:
            date_str = batch['expiration_date'] if batch['expiration_date'] else "без срока"
            print(f"  - {batch['amount']}, годен до: {date_str}")