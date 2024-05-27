class SickRegistry:
    def __init__(self, initial_size=4):
        self.table = [None] * initial_size
        self.amount_sick = 0
        self.table_size = initial_size

    def primary_hash(self, key):
        return sum(int(i) ** 2 + 147 for i in key) % self.table_size

    def secondary_hash(self, key):
        return 1 + sum(int(i) for i in key) % (self.table_size - 1)

    def double_hashing(self, key, i):
        return (self.primary_hash(key) + i * self.secondary_hash(key)) % self.table_size

    def add_sick(self, fullname, year_of_birth, address, work, num_department):
        self.amount_sick += 1
        reg_number = "0" * (2 - len(str(num_department))) + str(num_department) + "0" * (
                6 - len(str(self.amount_sick))) + str(self.amount_sick)

        if (self.amount_sick / self.table_size) >= 0.8:
            self.table_size *= 2
            self.table = self.extend_hash(self.table_size)

        i = 0
        idx = self.double_hashing(reg_number, i)
        while self.table[idx] is not None:
            i += 1
            idx = self.double_hashing(reg_number, i)

        self.table[idx] = [reg_number, fullname, year_of_birth, address, work]

    def extend_hash(self, new_size):
        old_table = self.table
        self.table = [None] * new_size
        self.table_size = new_size
        for entry in old_table:
            if entry is not None:
                i = 0
                idx = self.double_hashing(entry[0], i)
                while self.table[idx] is not None:
                    i += 1
                    idx = self.double_hashing(entry[0], i)
                self.table[idx] = entry
        return self.table

    def find_sick(self, reg_number):
        i = 0
        idx = self.double_hashing(reg_number, i)
        while self.table[idx] is not None:
            if self.table[idx][0] == reg_number:
                return self.table[idx]
            i += 1
            idx = self.double_hashing(reg_number, i)
        return None

    def remove_sick(self, reg_number):
        i = 0
        idx = self.double_hashing(reg_number, i)
        while self.table[idx] is not None:
            if self.table[idx][0] == reg_number:
                self.table[idx] = None
                self.table = self.rehash_table()
                return True
            i += 1
            idx = self.double_hashing(reg_number, i)
        return False

    def rehash_table(self):
        old_table = self.table[:]
        new_table = [None] * self.table_size
        for entry in old_table:
            if entry is not None:
                i = 0
                idx = self.double_hashing(entry[0], i)
                while new_table[idx] is not None:
                    i += 1
                    idx = self.double_hashing(entry[0], i)
                new_table[idx] = entry
        return new_table

    def clear_sick_data(self):
        self.table = [None] * self.table_size
        self.amount_sick = 0

    def print_all_sick(self):
        for entry in self.table:
            if entry is not None:
                print(f"Номер регистрации: {entry[0]}, ФИО: {entry[1]}, Год рождения: {entry[2]}, Адрес: {entry[3]}, Место работы: {entry[4]}")

