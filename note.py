import json
import os

# Константы для визуального оформления
STATUS_TODO = "[К выполнению]"
STATUS_IN_PROGRESS = "[В процессе]"
STATUS_WAITING = "[Ожидает]"
STATUS_DONE = "[Выполнено]"
STATUS_CANCELLED = "[Отменено]"

PRIORITY_HIGH = "(Высокий)"
PRIORITY_MEDIUM = "(Средний)"
PRIORITY_LOW = "(Низкий)"

# Цвета (для красоты, опционально, требует установки colorama)
try:
    from colorama import Fore, Style, init
    init()  # Инициализация colorama для Windows
    COLOR_TODO = Fore.RED
    COLOR_IN_PROGRESS = Fore.YELLOW
    COLOR_WAITING = Fore.MAGENTA
    COLOR_DONE = Fore.GREEN
    COLOR_CANCELLED = Fore.WHITE  # Или другой подходящий цвет
    COLOR_PRIORITY_HIGH = Fore.RED
    COLOR_PRIORITY_MEDIUM = Fore.YELLOW
    COLOR_PRIORITY_LOW = Fore.GREEN
    COLOR_RESET = Style.RESET_ALL  # Сброс цвета
except ImportError:
    COLOR_TODO = ""
    COLOR_IN_PROGRESS = ""
    COLOR_WAITING = ""
    COLOR_DONE = ""
    COLOR_CANCELLED = ""
    COLOR_PRIORITY_HIGH = ""
    COLOR_PRIORITY_MEDIUM = ""
    COLOR_PRIORITY_LOW = ""
    COLOR_RESET = ""

# Имя файла для хранения данных
DATA_FILE = "notes.json"


def load_data():
    """Загружает данные из файла JSON."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:  # Указываем кодировку utf-8 при чтении
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("Ошибка: Файл данных поврежден. Начинаем с пустой структуры.")
                return {"notes": [], "tasks": []}
    else:
        return {"notes": [], "tasks": []}


def save_data(data):
    """Сохраняет данные в файл JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:  # Указываем кодировку utf-8 при записи
        json.dump(data, f, indent=4, ensure_ascii=False)  # ensure_ascii=False для корректного отображения кириллицы


def display_items(items, level=0):
    """Отображает список задач и заметок."""
    for i, item in enumerate(items):
        prefix = "  " * level + f"{i+1}. "
        if item["type"] == "task":
            status_str, color = get_status_display(item["status"])
            priority_str, priority_color = get_priority_display(item["priority"])
            item_color = get_item_color(item["priority"]) # получаем цвет для всего элемента

            print(f"{prefix}{item_color}{status_str} {item['title']} {priority_str}{COLOR_RESET}")
        elif item["type"] == "note":
            status_str, color = get_status_display(item["status"])
            priority_str, priority_color = get_priority_display(item["priority"])
            item_color = get_item_color(item["priority"])  # получаем цвет для всего элемента

            print(f"{prefix}{item_color}{status_str} {item['title']} {priority_str}{COLOR_RESET}")


def get_status_display(status):
    """Возвращает строку статуса и цвет в зависимости от статуса элемента (задачи или заметки)."""
    if status == "к выполнению":
        return STATUS_TODO, COLOR_TODO
    elif status == "в процессе":
        return STATUS_IN_PROGRESS, COLOR_IN_PROGRESS
    elif status == "ожидает":
        return STATUS_WAITING, COLOR_WAITING
    elif status == "выполнено":
        return STATUS_DONE, COLOR_DONE
    elif status == "отменено":
        return STATUS_CANCELLED, COLOR_CANCELLED
    else:
        return "[Неизвестный статус]", ""  # Default case


def get_priority_display(priority):
    """Возвращает строку приоритета и цвет в зависимости от приоритета элемента (задачи или заметки)."""
    if priority == "высокий":
        return PRIORITY_HIGH, COLOR_PRIORITY_HIGH
    elif priority == "средний":
        return PRIORITY_MEDIUM, COLOR_PRIORITY_MEDIUM
    elif priority == "низкий":
        return PRIORITY_LOW, COLOR_PRIORITY_LOW
    else:
        return "(Неизвестный приоритет)", ""  # Default case

def get_item_color(priority):
    """Возвращает цвет элемента в зависимости от его приоритета."""
    if priority == "высокий":
        return COLOR_PRIORITY_HIGH
    elif priority == "средний":
        return COLOR_PRIORITY_MEDIUM
    elif priority == "низкий":
        return COLOR_PRIORITY_LOW
    else:
        return "" # Default case


def display_note_content(note):
    """Отображает содержимое заметки (включая вложенные элементы)."""
    if "content" in note and note["content"]:
        print(f"\nСодержимое заметки: {note['content']}\n")

    if "children" in note and note["children"]:
        print("Вложенные элементы:")
        display_items(note["children"], level=1)


def add_note(data, title, parent=None):
    """Добавляет новую заметку."""
    new_note = {"type": "note", "title": title, "content": "", "children": [], "status": "к выполнению", "priority": "средний"}  # Добавлены статус и приоритет по умолчанию
    if parent is None:
        data["notes"].append(new_note)
    else:
        parent["children"].append(new_note)
    print(f"Заметка '{title}' добавлена.")


def add_task(data, title, description, parent=None):
    """Добавляет новую задачу."""
    new_task = {"type": "task", "title": title, "description": description, "status": "к выполнению", "priority": "средний"}  # Добавлен приоритет по умолчанию
    if parent is None:
        data["tasks"].append(new_task)
    else:
        parent["children"].append(new_task)
    print(f"Задача '{title}' добавлена.")


def edit_note(note, new_title=None, new_content=None, new_status=None, new_priority=None):
    """Редактирует заголовок, содержимое, статус и/или приоритет заметки."""
    if new_title:
        note["title"] = new_title
    if new_content:
        note["content"] = new_content
    if new_status:
        if new_status in ["к выполнению", "в процессе", "ожидает", "выполнено", "отменено"]:
            note["status"] = new_status
        else:
            print("Ошибка: Недопустимый статус. Допустимые значения: к выполнению, в процессе, ожидает, выполнено, отменено.")
            return
    if new_priority:
        if new_priority in ["высокий", "средний", "низкий"]:
            note["priority"] = new_priority
        else:
            print("Ошибка: Недопустимый приоритет. Допустимые значения: высокий, средний, низкий.")
            return
    print("Заметка отредактирована.")


def edit_task(task, new_title=None, new_description=None, new_status=None, new_priority=None):
    """Редактирует заголовок, описание, статус и/или приоритет задачи."""
    if new_title:
        task["title"] = new_title
    if new_description:
        task["description"] = new_description
    if new_status:
        if new_status in ["к выполнению", "в процессе", "ожидает", "выполнено", "отменено"]:
            task["status"] = new_status
        else:
            print("Ошибка: Недопустимый статус. Допустимые значения: к выполнению, в процессе, ожидает, выполнено, отменено.")
            return
    if new_priority:
        if new_priority in ["высокий", "средний", "низкий"]:
            task["priority"] = new_priority
        else:
            print("Ошибка: Недопустимый приоритет. Допустимые значения: высокий, средний, низкий.")
            return
    print("Задача отредактирована.")


def delete_item(data, index, item_type, parent=None):
    """Удаляет заметку или задачу."""
    try:
        index = int(index) - 1
        if index < 0:
            print("Ошибка: Некорректный индекс.")
            return

        if parent is None:
            if item_type == "note":
                if index < len(data["notes"]):
                    deleted_title = data["notes"][index]["title"]
                    del data["notes"][index]
                    print(f"Заметка '{deleted_title}' удалена.")
                else:
                    print("Ошибка: Заметка с таким индексом не найдена.")

            elif item_type == "task":
                if index < len(data["tasks"]):
                    deleted_title = data["tasks"][index]["title"]
                    del data["tasks"][index]
                    print(f"Задача '{deleted_title}' удалена.")
                else:
                    print("Ошибка: Задача с таким индексом не найдена.")

            else:
                print("Ошибка: Неверный тип элемента для удаления.")
        else:
            if index < len(parent["children"]):
                deleted_title = parent["children"][index]["title"]
                del parent["children"][index]
                print(f"Элемент '{deleted_title}' удален.")
            else:
                print("Ошибка: Элемент с таким индексом не найден.")

    except ValueError:
        print("Ошибка: Введите числовой индекс.")


def view_item(data, index, item_type, parent=None):
    """Отображает детали заметки или задачи."""
    try:
        index = int(index) - 1
        if index < 0:
            print("Ошибка: Некорректный индекс.")
            return

        if parent is None:
            if item_type == "note":
                if index < len(data["notes"]):
                    note = data["notes"][index]
                    display_note_content(note)
                    status_str, color = get_status_display(note["status"])  # Get display string and color
                    priority_str, priority_color = get_priority_display(note["priority"])
                    print(f"Статус: {color}{status_str}{COLOR_RESET}")
                    print(f"Приоритет: {priority_color}{priority_str}{COLOR_RESET}\n")
                    return data["notes"][index]  # Возвращаем объект для дальнейшей навигации
                else:
                    print("Ошибка: Заметка с таким индексом не найдена.")
            elif item_type == "task":
                if index < len(data["tasks"]):
                    task = data["tasks"][index]
                    status_str, color = get_status_display(task["status"])  # Get display string and color
                    priority_str, priority_color = get_priority_display(task["priority"])

                    print(f"\nЗадача: {task['title']}")
                    print(f"Описание: {task['description']}")
                    print(f"Статус: {color}{status_str}{COLOR_RESET}")
                    print(f"Приоритет: {priority_color}{priority_str}{COLOR_RESET}\n")
                    return None  # Задачи не содержат вложенных элементов, поэтому ничего не возвращаем.
                else:
                    print("Ошибка: Задача с таким индексом не найдена.")
            else:
                print("Ошибка: Неверный тип элемента для просмотра.")
        else:
            if index < len(parent["children"]):
                item = parent["children"][index]
                if item["type"] == "note":
                    display_note_content(item)
                    status_str, color = get_status_display(item["status"])  # Get display string and color
                    priority_str, priority_color = get_priority_display(item["priority"])
                    print(f"Статус: {color}{status_str}{COLOR_RESET}")
                    print(f"Приоритет: {priority_color}{priority_str}{COLOR_RESET}\n")

                    return item
                elif item["type"] == "task":
                    status_str, color = get_status_display(item["status"])  # Get display string and color
                    priority_str, priority_color = get_priority_display(item["priority"])
                    print(f"\nЗадача: {item['title']}")
                    print(f"Описание: {item['description']}")
                    print(f"Статус: {color}{status_str}{COLOR_RESET}")
                    print(f"Приоритет: {priority_color}{priority_str}{COLOR_RESET}\n")
                    return None
            else:
                print("Ошибка: Элемент с таким индексом не найден.")
    except ValueError:
        print("Ошибка: Введите числовой индекс.")
    return None


def main():
    """Основная функция программы."""
    data = load_data()
    current_context = None  # Отслеживание текущего контекста (в какой заметке мы находимся)

    while True:
        print("\n--- Заметки ---")
        if current_context is None:
            print("Корневой уровень")
            print("Заметки:")
            display_items(data["notes"])
            print("\nЗадачи:")
            display_items(data["tasks"])
        else:
            print(f"Вы находитесь в заметке: {current_context['title']}")
            display_items(current_context["children"])

        print("\nКоманды:")
        print("+n|t <название> - Добавить заметку|задачу")
        print("e|d|v [n|t] <индекс> - Редактировать|Удалить|Просмотреть заметку (n) или задачу (t)")
        print(".. - Вернуться на уровень выше")
        print("q - Выход")

        command = input("Введите команду: ").split()

        if not command:
            continue

        action = command[0]

        if action == "+n":
            if len(command) > 1:
                title = " ".join(command[1:])
                add_note(data, title, parent=current_context)
                save_data(data)
            else:
                print("Ошибка: Укажите название заметки.")

        elif action == "+t":
            if len(command) > 2:
                title = command[1]
                description = " ".join(command[2:])
                add_task(data, title, description, parent=current_context)
                save_data(data)
            else:
                print("Ошибка: Укажите название и описание задачи.")

        elif action == "e":
            if len(command) > 2:
                item_type = command[1]
                index = command[2]
                if item_type == "n":
                    if current_context is None:
                        if int(index) - 1 < len(data["notes"]):
                            note_to_edit = data["notes"][int(index) - 1]
                            new_title = input("Новый заголовок (оставьте пустым, чтобы пропустить): ")
                            new_content = input("Новое содержимое (оставьте пустым, чтобы пропустить): ")
                            new_status = input(
                                f"Новый статус (к выполнению, в процессе, ожидает, выполнено, отменено, оставьте пустым, чтобы пропустить) [{note_to_edit['status']}]: ")
                            new_priority = input(
                                f"Новый приоритет (высокий, средний, низкий, оставьте пустым, чтобы пропустить) [{note_to_edit['priority']}]: ")
                            edit_note(note_to_edit, new_title, new_content, new_status, new_priority)
                            save_data(data)
                        else:
                            print("Ошибка: Заметка с таким индексом не найдена.")
                    else:
                        if int(index) - 1 < len(current_context["children"]):
                            note_to_edit = current_context["children"][int(index) - 1]
                            if note_to_edit["type"] == "note":
                                new_title = input("Новый заголовок (оставьте пустым, чтобы пропустить): ")
                                new_content = input("Новое содержимое (оставьте пустым, чтобы пропустить): ")
                                new_status = input(
                                    f"Новый статус (к выполнению, в процессе, ожидает, выполнено, отменено, оставьте пустым, чтобы пропустить) [{note_to_edit['status']}]: ")
                                new_priority = input(
                                    f"Новый приоритет (высокий, средний, низкий, оставьте пустым, чтобы пропустить) [{note_to_edit['priority']}]: ")
                                edit_note(note_to_edit, new_title, new_content, new_status, new_priority)
                                save_data(data)
                            else:
                                print("Ошибка: Это задача, а не заметка.")
                        else:
                            print("Ошибка: Заметка с таким индексом не найдена.")


                elif item_type == "t":
                    if current_context is None:
                        if int(index) - 1 < len(data["tasks"]):
                            task_to_edit = data["tasks"][int(index) - 1]
                            new_title = input("Новый заголовок (оставьте пустым, чтобы пропустить): ")
                            new_description = input("Новое описание (оставьте пустым, чтобы пропустить): ")
                            new_status = input(
                                f"Новый статус (к выполнению, в процессе, ожидает, выполнено, отменено, оставьте пустым, чтобы пропустить) [{task_to_edit['status']}]: ")
                            new_priority = input(
                                f"Новый приоритет (высокий, средний, низкий, оставьте пустым, чтобы пропустить) [{task_to_edit['priority']}]: ")
                            edit_task(task_to_edit, new_title, new_description, new_status, new_priority)
                            save_data(data)
                        else:
                            print("Ошибка: Задача с таким индексом не найдена.")
                    else:
                        if int(index) - 1 < len(current_context["children"]):
                            task_to_edit = current_context["children"][int(index) - 1]
                            if task_to_edit["type"] == "task":
                                new_title = input("Новый заголовок (оставьте пустым, чтобы пропустить): ")
                                new_description = input("Новое описание (оставьте пустым, чтобы пропустить): ")
                                new_status = input(
                                    f"Новый статус (к выполнению, в процессе, ожидает, выполнено, отменено, оставьте пустым, чтобы пропустить) [{task_to_edit['status']}]: ")
                                new_priority = input(
                                    f"Новый приоритет (высокий, средний, низкий, оставьте пустым, чтобы пропустить) [{task_to_edit['priority']}]: ")
                                edit_task(task_to_edit, new_title, new_description, new_status, new_priority)
                                save_data(data)
                            else:
                                print("Ошибка: Это заметка, а не задача.")
                        else:
                            print("Ошибка: Задача с таким индексом не найдена.")
                else:
                    print("Ошибка: Укажите тип элемента (n для заметки, t для задачи).")

            else:
                print("Ошибка: Укажите тип элемента и индекс для редактирования.")

        elif action == "d":
            if len(command) > 2:
                item_type = command[1]
                index = command[2]

                if item_type == "n":
                    delete_item(data, index, "note", parent=current_context)
                    save_data(data)
                elif item_type == "t":
                    delete_item(data, index, "task", parent=current_context)
                    save_data(data)
                else:
                    print("Ошибка: Укажите тип элемента (n для заметки, t для задачи).")
            else:
                print("Ошибка: Укажите тип элемента и индекс для удаления.")

        elif action == "v":
            if len(command) > 2:
                item_type = command[1]
                index = command[2]

                if item_type == "n":
                    if current_context is None:
                        note_to_view = data["notes"][int(index)-1]
                        status_str, color = get_status_display(note_to_view["status"])  # Get display string and color
                        priority_str, priority_color = get_priority_display(note_to_view["priority"])
                        print(f"Статус: {color}{status_str}{COLOR_RESET}")
                        print(f"Приоритет: {priority_color}{priority_color}{COLOR_RESET}\n")
                        new_context = view_item(data, index, "note")


                        if new_context:
                            current_context = new_context  # Переходим в контекст выбранной заметки
                    else:

                        note_to_view = current_context["children"][int(index)-1]
                        status_str, color = get_status_display(note_to_view["status"])  # Get display string and color
                        priority_str, priority_color = get_priority_display(note_to_view["priority"])
                        print(f"Статус: {color}{status_str}{COLOR_RESET}")
                        print(f"Приоритет: {priority_color}{priority_color}{COLOR_RESET}\n")

                        new_context = view_item(data, index, "note", parent=current_context)
                        if new_context:
                            current_context = new_context
                elif item_type == "t":
                    view_item(data, index, "task", parent=current_context)  # Задачи не содержат вложенных элементов, поэтому никуда не переходим.
                else:
                    print("Ошибка: Укажите тип элемента (n для заметки, t для задачи).")
            else:
                print("Ошибка: Укажите тип элемента и индекс для просмотра.")

        elif action == "..":
            if current_context is not None:
                # Возвращаемся на уровень вверх. Если мы в корне, ничего не делаем.
                # Нужно хранить историю, чтобы возвращаться не только на один уровень.
                # Но для простоты пока так.
                def find_parent(data, node):
                    """Находит родительскую заметку для заданного узла."""
                    # Проверяем корневые заметки
                    for note in data["notes"]:
                        if note is node:
                            return None  # Это корневая заметка, родителя нет

                    # Рекурсивный поиск в дочерних элементах
                    def search_children(parent, node):
                        if "children" in parent:
                            for child in parent["children"]:
                                if child is node:
                                    return parent
                                else:
                                    found = search_children(child, node)
                                    if found:
                                        return found
                        return None

                    for note in data["notes"]:
                        found = search_children(note, node)
                        if found:
                            return found

                    return None  # Родитель не найден

                parent = find_parent(data, current_context)
                current_context = parent  # переходим к родителю.
            else:
                print("Вы уже находитесь на корневом уровне.")

        elif action == "q":
            print("Выход.")
            break

        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()