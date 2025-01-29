import requests
from datetime import datetime, timedelta

# Группы с их ID
groups = {
    138: "Внесение изменений в изделие",
    128: "ЗАМЕРЫ",
    82: "Заявки на нестандарт"
}

# URL для получения задач
task_detail_url = "https://simplepro.bitrix24.ru/rest/43/7pwrbykl4qx2gmk7/tasks.task.list.json"


def get_previous_month_date_range():
    """
    Возвращает начало и конец предыдущего месяца в формате для API.
    """
    today = datetime.now()
    # Последний день предыдущего месяца
    last_day_previous_month = today.replace(day=1) - timedelta(days=1)
    # Первый день предыдущего месяца
    first_day_previous_month = last_day_previous_month.replace(day=1)

    # Преобразуем в формат API (с учетом временного сдвига +3 часа)
    start_date_api = first_day_previous_month.strftime('%Y-%m-%dT00:00:00')
    end_date_api = last_day_previous_month.strftime('%Y-%m-%dT23:59:59')

    return start_date_api, end_date_api


def fetch_task_statistics(start_date_api, end_date_api):
    """
    Получает статистику завершенных задач для каждой группы за указанный период.
    """
    results = {group_name: {} for group_name in groups.values()}

    for group_id, group_name in groups.items():
        params = {
            "order": {"ID": "ASC"},  # Сортировка по ID
            "filter": {
                "GROUP_ID": group_id,  # Ищем задачи по группе
                ">=CLOSED_DATE": start_date_api,  # Завершенные задачи после start_date
                "<=CLOSED_DATE": end_date_api,  # Завершенные задачи до end_date
                "STATUS": "5"  # Только завершенные задачи
            },
            "select": ["id", "title", "responsibleId", "responsible", "closedDate"]  # Поля, которые нужно получить
        }

        try:
            response = requests.post(task_detail_url, json=params)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе группы {group_name}: {e}")
            continue
        except ValueError:
            print(f"Ошибка обработки JSON для группы {group_name}")
            continue

        tasks = data.get("result", {}).get("tasks", [])
        if tasks:
            for task in tasks:
                responsible = task.get("responsible", {})
                responsible_name = responsible.get("name", "Неизвестный")
                closed_date = task.get("closedDate", "Неизвестно")
                task_title = task.get("title", "Без названия")

                # Инициализация данных для ответственного
                if responsible_name not in results[group_name]:
                    results[group_name][responsible_name] = {"count": 0, "tasks": []}

                # Увеличиваем счетчик завершенных задач
                results[group_name][responsible_name]["count"] += 1

                # Добавляем информацию о задаче
                results[group_name][responsible_name]["tasks"].append({
                    "title": task_title,
                    "closed_date": closed_date
                })

    return results

def print_statistics(results):
    """
    Выводит статистику завершенных задач в читаемом формате.
    """
    for group_name, responsible_stats in results.items():
        print(f"\nГруппа: {group_name}")
        if not responsible_stats:
            print("  Нет завершенных задач за указанный период.")
            continue
        for responsible_name, stats in responsible_stats.items():
            print(f"  Ответственный: {responsible_name}")
            print(f"    Завершенные задачи: {stats['count']}")
            print("    Список задач:")
            for task in stats["tasks"]:
                print(f"      - {task['title']} (Дата завершения: {task['closed_date']})")

def main():
    start_date_api, end_date_api = get_previous_month_date_range()
    results = fetch_task_statistics(start_date_api, end_date_api)
    print_statistics(results)

if __name__ == "__main__":
    main()
