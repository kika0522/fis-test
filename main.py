import json
from datetime import datetime


def is_client_eligible_for_credit(client_data: dict) -> bool:
    # Проверка возраста
    birth_date_raw = client_data.get("birthDate")
    birth_date = datetime.strptime(birth_date_raw, "%Y-%m-%dT%H:%M:%S.%fZ")
    age = (datetime.now() - birth_date).days // 365
    if age < 20:
        return False

    # Проверка даты выдачи паспорта для клиентов младше 20 лет
    passport_issued_at = datetime.strptime(
        client_data["passport"]["issuedAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
    )
    age_20_date = birth_date.replace(year=birth_date.year + 20)
    if passport_issued_at < age_20_date and age > 20:
        return False

    # Проверка даты выдачи паспорта для клиентов старше 45 лет
    if age > 45:
        age_45_date = birth_date.replace(year=birth_date.year + 45)
        if passport_issued_at < age_45_date:
            return False

    credit_overdue_15_days_count = 0

    # Проверка кредитной истории
    for credit in client_data["creditHistory"]:
        credit_type = credit["type"]
        overdued_days = credit.get(
            "numberOfDaysOnOverdue", 0
        )  # количество дней на просрочке
        current_overdue = credit.get(
            "currentOverdueDebt", 0
        )  # просроченная задолженность

        if credit_type == "Кредитная карта":
            if current_overdue > 0 or overdued_days > 30:
                return False
        else:
            if current_overdue > 0 or overdued_days > 60:
                return False
            if overdued_days > 15:
                credit_overdue_15_days_count += 1

    # Проверка количества просроченных кредитов
    if credit_overdue_15_days_count > 2:
        return False

    return True


if __name__ == "__main__":
    with open("client_data_valid.json", "r", encoding="utf-8") as file:
        client_data_valid = json.loads(file.read())

    with open("client_data_invalid_passport.json", "r", encoding="utf-8") as file:
        client_data_invalid_passport = json.loads(file.read())

    with open("client_data_invalid_credit_history.json", "r", encoding="utf-8") as file:
        client_data_invalid_credit_history = json.loads(file.read())

    with open("client_data_young.json", "r", encoding="utf-8") as file:
        client_data_young = json.loads(file.read())

    print(
        f"Check client with valid data: {is_client_eligible_for_credit(client_data_valid)}"
    )
    print(
        f"Check client with invalid passport data: {is_client_eligible_for_credit(client_data_invalid_passport)}"
    )
    print(
        f"Check client with invalid credit history: {is_client_eligible_for_credit(client_data_invalid_credit_history)}"
    )
    print(
        f"Check client too young age: {is_client_eligible_for_credit(client_data_young)}"
    )
