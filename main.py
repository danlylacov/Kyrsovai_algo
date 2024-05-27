from Registry import PolyclinicRegistry

menu = ["МЕНЮ:",
        "1. Регистрация нового больного",
        "2. Удаление данных о больном",
        "3. Просмотр всех зарегистрированных больных",
        "4. Очистка данных о больных",

        "5. Поиск больного по регистрационному номеру",
        "6. Поиск больного по его ФИО",
        "7. Добавление нового врача",
        "8. Удаление сведений о враче",
        "9. Просмотр всех имеющихся врачей",
        "10. Очистка данных о врачах",
        "11. Поиск врача по ФИО",
        "12. Поиск врача по фрагментам «Должность»",
        "13. Регистрация выдачи больному направления к врачу",
        "14. Регистрация возврата направления к врачу"
        ]

policlinic = PolyclinicRegistry()

policlinic.sick_registry.add_sick("Лулаков Даниил Феликсович", 1990, "СПб, Невский пр. д. 34", "ГУАП", 1)
policlinic.sick_registry.add_sick("Петров Петр Петрович", 1985, "СПб, Новоизмайловский пр. д. 2", "ГУАП", 22)
policlinic.sick_registry.add_sick("Иванов Иван Иванович", 2004, "СПб, пр. Просвещения д. 124", "ГУАП", 3)

policlinic.doctors_registry.add_doctor(real=False)

policlinic.directions_registry.add_direction("01000001", "Сергеев С. С.", "10-10-2000", "11:00")
policlinic.directions_registry.add_direction("22000002", "Дмитриев Д. Д.", "15-06-2007", "12:00")
policlinic.directions_registry.add_direction("22000002", "Максимов М. М.", "23-01-2004", "09:00")


def run():
    while True:
        print()
        try:
            print(*menu, sep='\n')
            n = int(input("\nВведите номер опции (1-14) или 0 для отображения опций: "))


        except ValueError:
            print("Ошибка: Вводить надо число от 1 до 14!")
        print()
        if n == 1:
            policlinic.register_new_sick()
        elif n == 2:
            while True:
                reg_number = input("Регистрационный номер: ")
                try:
                    mov = policlinic.delete_sick(reg_number)
                    print("Данные о больном удалены") if mov == True else print("Больной не найден в данных")
                    break
                except ValueError:
                    print("Ошибка: введите корректно регистрационный номер")
        elif n == 3:
            policlinic.show_all_sick()
        elif n == 4:
            policlinic.clear_sick_data()
            print("Данные о всех больных удалены")
        elif n == 5:
            while True:
                reg_number = input("Регистрационный номер: ")
                try:
                    policlinic.find_sick_by_reg_number(reg_number)
                    break
                except ValueError:
                    print("Ошибка: введите корректно регистрационный номер")
        elif n == 6:
            fullname = input("Введите ФИО больного: ")
            policlinic.find_sick_by_fullname(fullname)
        elif n == 7:
            policlinic.add_new_doctor()
        elif n == 8:
            fullname = input("Введите ФИО врача для удаления: ")
            policlinic.delete_doctor(fullname)
            print("Врач удалён из базы")
        elif n == 9:
            policlinic.show_all_doctors()
        elif n == 10:
            policlinic.clear_doctors_data()
            print("Все данные о врачах были очищены.")
        elif n == 11:
            fullname = input("Введите ФИО врача: ")
            policlinic.find_doctor_by_fullname(fullname)
        elif n == 12:
            position_fragment = input("Введите фрагмент должности: ")
            policlinic.doctors_registry.find_by_position(position_fragment)
        elif n == 13:
            policlinic.register_direction_to_doctor()
        elif n == 14:
            policlinic.register_direction_return()
        else:
            print("Неправильный ввод. Пожалуйста, введите число от 0 до 14.")


if __name__ == "__main__":
    run()
