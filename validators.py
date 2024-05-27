import re


def validate_fields_sick(fullname, year_of_birth, address, work, num_department):
    f = False

    print("*************************************************")
    if not (fullname and " " in fullname.strip()) or len(fullname) > 30:
        print("Поле 'fullname' должно содержать имя и фамилию и нормальную длину")
        f = True

    current_year = 2024
    if not (1900 <= year_of_birth <= current_year):
        print("Поле 'year_of_birth' содержит нереальный год рождения")
        f = True

    if not address.strip() or len(address) > 30 or len(address) < 4:
        print("Поле 'address' не может быть пустым и должно быть от 4 до 30 символов")
        f = True

    if not work.strip() or len(work) > 30 or len(work) < 3:
        print("Поле 'work' не может быть пустым и должно быть от 3 до 30 символов")
        f = True

    if not (0 < num_department < 100):
        print("Поле 'num_department' содержит неверный номер отдела")
        f = True

    if f == False:
        print("Данные корректны, спасибо!")
    else:
        print()
        print("Пожалуйста, введите данные корректно")
    print("*************************************************")
    return f


def validate_fields_doctor(fullname, position, schedule, num_cabinet):
    f = False

    print("*************************************************")
    if not (fullname and fullname.strip().count(" ") == 2 and len(fullname) < 25):
        print("Поле 'ФИО' должно содержать фамилию и инициалы")
        f = True

    if not position.strip() or len(position) < 5 or len(position) > 10:
        print("Поле 'Должность' не может быть пустым и должно содержать от 5 до 10 символов")
        f = True

    schedule_pattern = re.compile(r'^\d{2}:\d{2}-\d{2}:\d{2}$')
    if not schedule_pattern.match(schedule):
        print("Поле 'Расписание' должно соответствовать формату 'ЧЧ:MM-ЧЧ:MM'. Например, 10:00-18:00")
        f = True

    if not (0 < num_cabinet < 100):
        print("Поле 'Номер кабинета' содержит некорректный номер")
        f = True

    if f == False:
        print("Данные корректны, спасибо!")
    else:
        print()
        print("Пожалуйста, введите данные корректно")
    print("*************************************************")
    return f

    amount_sick += 1
    flag = True
    while flag:
        try:
            fullname = input("Введите полное имя: ")
            year_of_birth = int(input("Введите год рождения: "))
            address = input("Введите адрес: ")
            work = input("Введите место работы: ")
            num_department = int(input("Введите номер отдела: "))

            flag = validate_fields_sick(fullname, year_of_birth, address, work, num_department)

        except ValueError:
            print("*************************************************")
            print("Ошибка: год рождения и номер отдела должны быть числами")
            print("*************************************************")

    reg_number = "0" * (2 - len(str(num_department))) + str(num_department) + "0" * (6 - len(str(amount_sick))) + str(
        amount_sick)

    if (amount_sick / long) < 0.8:
        return add_hash(hash_table, fullname, year_of_birth, address, work, long, reg_number)
    else:
        long *= 2
        hash_table = extend_hash(hash_table, long)
        return add_hash(hash_table, fullname, year_of_birth, address, work, long, reg_number)



def search(text, word):
    n = len(text)
    m = len(word)
    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == word[j]:
            j += 1
        if j == m:
            return True
    return False
