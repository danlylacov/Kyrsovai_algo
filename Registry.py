import re

from AVLtreeDoctors import AVLTree
from Directions import DirectionsList
from SickRegistration import SickRegistry
from validators import validate_fields_sick


class PolyclinicRegistry:
    def __init__(self):
        self.sick_registry = SickRegistry()
        self.doctors_registry = AVLTree()
        self.directions_registry = DirectionsList()


    def register_new_sick(self):
        flag = True
        while flag:
            try:
                fullname = input("ФИО больного: ")
                year_of_birth = int(input("Год рождения: "))
                address = input("Адрес: ")
                work = input("Место работы: ")
                num_department = int(input("Номер отделения: "))

                flag = validate_fields_sick(fullname, year_of_birth, address, work, num_department)

            except ValueError:
                print("*************************************************")
                print("Ошибка: номер кабинета должен быть числом")
                print("*************************************************")

        self.sick_registry.add_sick(fullname, year_of_birth, address, work, num_department)

    def delete_sick(self, reg_number):
        a = self.sick_registry.remove_sick(reg_number)
        self.directions_registry.remove_directions(reg_number)
        return a

    def show_all_sick(self):
        self.sick_registry.print_all_sick()

    def clear_sick_data(self):
        self.sick_registry.clear_sick_data()


    def find_sick_by_reg_number(self, reg_number):
        data = self.sick_registry.find_sick(reg_number)
        if data is not None:
            fio_doctor = self.directions_registry.find_directions(reg_number)

            print("Данные:", data)
            print("ФИО врачей:", [fio_doctor[i].doctor_fullname for i in range(len(fio_doctor))]) if len(
                fio_doctor) > 0 else print("Нет записей к врачам")
        else:
            print("Больной не найден")


    def find_sick_by_fullname(self, fullname):
        data = []
        for i in self.sick_registry.table:
            if i is not None and fullname == i[1]:
                data.append([i[0], i[1]])
        if len(data) != 0:
            print("Данные больных:")

            for i in data:
                print("Регистрационный номер:", i[0], "ФИО:", i[1])
        else:
            print("Данные не найдены")


    def add_new_doctor(self):
        self.doctors_registry.add_doctor()


    def delete_doctor(self, fullname):
        self.doctors_registry.delete_doctor(fullname)
        self.directions_registry.remove_directions(fullname, by='doctor_fullname')


    def show_all_doctors(self):
        self.doctors_registry.print_tree()


    def clear_doctors_data(self):
        self.doctors_registry.clear()

    def register_direction_to_doctor(self):
        reg_number, doctor_fullname, date, time = self.input_direction_data()
        valid_data = self.validate_direction_data(reg_number, doctor_fullname, date, time)
        doctor_node = self.doctors_registry.find_doctor(doctor_fullname)
        if valid_data and doctor_node:
            schedule_start, schedule_end = doctor_node.schedule.split('-')
            if self.is_time_within_schedule(time, schedule_start, schedule_end):
                if not self.directions_registry.direction_exists(doctor_fullname, date, time):
                    self.directions_registry.register_direction(reg_number, doctor_fullname, date, time)
                    print(f"Направление к врачу {doctor_fullname} на {date} {time} успешно выдано.")
                else:
                    print(f"Направление к врачу {doctor_fullname} на {date} {time} уже существует.")
            else:
                print(f"Время приема {time} не входит в график работы врача {doctor_fullname}.")
        else:
            if not doctor_node:
                print(f"Врач с ФИО '{doctor_fullname}' не найден в системе.")
            else:
                print("Ошибка в введенных данных.")

    def is_time_within_schedule(self, time, schedule_start, schedule_end):
        from datetime import datetime
        time_obj = datetime.strptime(time, '%H:%M')
        start_obj = datetime.strptime(schedule_start, '%H:%M')
        end_obj = datetime.strptime(schedule_end, '%H:%M')
        return start_obj <= time_obj <= end_obj

    def find_doctor_by_fullname(self, doctor_fullname):
        data = self.doctors_registry.find_doctor(doctor_fullname)
        if data is not None:
            print(f"Найден врач: {data.fullname}, Должность: {data.position},"
                  f"Номер кабинета: {data.num_cabinet}, Расписание: {data.schedule}")
            reg_numbers = self.directions_registry.find_directions(doctor_fullname, by='doctor_fullname')
            if len(reg_numbers) > 0:
                for i in reg_numbers:
                    print(i.reg_number, self.sick_registry.find_sick(i.reg_number)[1])
            else:
                print("Записей к врачу нет")
        else:
            print(f"Врач с ФИО не найден.")

    def input_direction_data(self):
        reg_number = input("Введите регистрационный номер больного: ")
        doctor_fullname = input("Введите полное имя врача: ")
        date = input("Введите дату направления (DD-MM-YYYY): ")
        time = input("Введите время направления (HH:MM): ")
        return reg_number, doctor_fullname, date, time

    def validate_direction_data(self, reg_number, doctor_fullname, date, time):
        if not reg_number.isdigit() or len(reg_number) != 8:
            print("Некорректный регистрационный номер. Он должен содержать 8 цифр.")
            return False
        if not re.match("^\d{2}-\d{2}-\d{4}$", date):
            print("Дата должна быть в формате DD-MM-YYYY.")
            return False
        if not re.match("^\d{2}:\d{2}$", time):
            print("Время должно быть в формате HH:MM.")
            return False
        # Проверку на существование доктора можно добавить при наличии всех данных докторов
        return True

    def register_direction_return(self):
        reg_number, doctor_fullname, date, time = self.input_direction_data()
        if self.validate_direction_data(reg_number, doctor_fullname, date, time):
            directions_for_reg_number = self.directions_registry.find_directions(reg_number)
            direction_to_return = next((d for d in directions_for_reg_number
                                        if d.date == date and d.time == time), None)
            if direction_to_return:
                self.directions_registry.remove_directions(direction_to_return)
                print(f"Направление больного с регистрационным номером {reg_number} возвращено.")
            else:
                print(f"Направление больного с регистрационным номером {reg_number} не найдено.")
        else:
            print("Ошибка в введенных данных.")
