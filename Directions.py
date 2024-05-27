class DirectionNode:
    def __init__(self, reg_number, doctor_fullname, date, time):
        self.reg_number = reg_number
        self.doctor_fullname = doctor_fullname
        self.date = date
        self.time = time
        self.next = None


class DirectionsList:
    def __init__(self):
        self.head = None

    def add_direction(self, reg_number, doctor_fullname, date, time):
        new_node = DirectionNode(reg_number, doctor_fullname, date, time)
        if self.head is None:
            self.head = new_node
            new_node.next = self.head
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = new_node
            new_node.next = self.head

    def remove_directions(self, identifier, by='reg_number'):
        if not self.head:
            return

        current = self.head
        prev = None
        while True:
            match = (
                    (by == 'reg_number' and current.reg_number == identifier) or
                    (by == 'doctor_fullname' and current.doctor_fullname == identifier)
            )
            if match:
                if prev is not None:
                    prev.next = current.next
                    if current == self.head:
                        self.head = current.next
                    if current.next == self.head:
                        prev.next = self.head
                else:
                    if current.next == self.head:
                        self.head = None
                    else:
                        # Находим последний элемент и переключаем его на следующий после головного
                        while current.next != self.head:
                            current = current.next
                        current.next = self.head.next
                        self.head = self.head.next
                break

            prev = current
            current = current.next
            if current == self.head:
                break

    def find_directions(self, identifier, by='reg_number'):
        directions = []

        current = self.head
        if current is None:
            return directions
        while True:
            if ((by == 'reg_number' and current.reg_number == identifier) or
                    (by == 'doctor_fullname' and current.doctor_fullname ==
                    identifier)):
                directions.append(current)
            current = current.next
            if current == self.head:
                break
        return directions

    def direction_exists(self, doctor_fullname, date, time):
        if self.head is None:
            return False

        current = self.head
        while True:
            if current.doctor_fullname == doctor_fullname and current.date == date and current.time == time:
                return True

            current = current.next
            if current == self.head:
                break

        return False

    def register_direction(self, reg_number, doctor_fullname, date, time):
        if self.direction_exists(doctor_fullname, date, time):
            return False

        else:
            self.add_direction(reg_number, doctor_fullname, date, time)
            return True

    def to_array(self):
        array = []
        current = self.head
        if self.head is not None:
            while True:
                array.append(current)
                current = current.next
                if current == self.head:
                    break
        return array

    def from_array(self, array):
        self.head = None
        for node in array:
            self.add_direction(node.reg_number, node.doctor_fullname, node.date, node.time)

    def counting_sort(self):
        array = self.to_array()
        if not array:
            return

        max_reg_number = max(int(node.reg_number) for node in array)

        count = [0] * (max_reg_number + 1)

        for node in array:
            count[int(node.reg_number)] += 1


        for i in range(1, len(count)):
            count[i] += count[i - 1]

        output = [None] * len(array)
        for node in reversed(array):
            count[int(node.reg_number)] -= 1
            output[count[int(node.reg_number)]] = node

        self.from_array(output)

    def print_list(self):
        if self.head is None:
            print("Список направлений пуст.")
            return

        current = self.head
        while True:
            print(
                f"Рег. номер: {current.reg_number}, ФИО врача: {current.doctor_fullname}, Дата: {current.date}, Время: {current.time}")
            current = current.next
            if current == self.head:
                break
