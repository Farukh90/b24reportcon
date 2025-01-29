from constants import B24REPORT_BOT, B24REPORT_CHAT_ID, B24REPORT_THREADS
from src.b24request import (fetch_task_statistics_report, generate_html_report,
                            generate_statistics_report,
                            get_previous_month_date_range)
from src.tg_alert_cls import TelegramAlert


def main():
    start_date_api, end_date_api = get_previous_month_date_range()
    results = fetch_task_statistics_report(start_date_api, end_date_api)
    tg_api_obj = TelegramAlert(B24REPORT_BOT, B24REPORT_CHAT_ID, B24REPORT_THREADS)
    # report = generate_statistics_report(results)
    report = generate_html_report(results)
    tg_api_obj.send_message(report, "отчеты по выполненным работам b24")


if __name__ == "__main__":
    main()
