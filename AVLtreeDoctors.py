from validators import search, validate_fields_doctor


class Node:
    def __init__(self, fullname, position, num_cabinet, schedule):
        self.fullname = fullname
        self.position = position
        self.num_cabinet = num_cabinet
        self.schedule = schedule
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.right) - self.get_height(node.left)

    def search_doctor(self, node, nodes_list, fragment=""):
        if node is not None:
            self.search_doctor(node.left, nodes_list, fragment)
            if fragment == "":
                nodes_list.append(
                    f"ФИО: {node.fullname}, Должность: {node.position}, Номер кабинета: {node.num_cabinet}, Расписание: {node.schedule}")
            else:
                if search(node.position, fragment):
                    nodes_list.append(
                        f"ФИО: {node.fullname}, Должность: {node.position}, Номер кабинета: {node.num_cabinet}, Расписание: {node.schedule}")
            self.search_doctor(node.right, nodes_list, fragment)
        return nodes_list

    def print_tree(self):
        nodes_list = []
        self.search_doctor(self.root, nodes_list)
        if len(nodes_list) > 0:
            for node in nodes_list:
                print(node)
        else:
            print("Список врачей пуст")

    def fix_height(self, node):
        node.height = max(self.get_height(node.left), self.get_height(node.right)) + 1

    def rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self.fix_height(y)
        self.fix_height(x)
        return x

    def rotate_left(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self.fix_height(x)

        self.fix_height(y)
        return y

    def balance(self, node):
        self.fix_height(node)
        balance = self.get_balance(node)

        if balance > 1:
            if self.get_balance(node.right) < 0:
                node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        if balance < -1:
            if self.get_balance(node.left) > 0:
                node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        return node

    def insert(self, node, fullname, position, num_cabinet, schedule):
        if not node:
            return Node(fullname, position, num_cabinet, schedule)

        if fullname < node.fullname:
            node.left = self.insert(node.left, fullname, position, num_cabinet, schedule)
        elif fullname > node.fullname:
            node.right = self.insert(node.right, fullname, position, num_cabinet, schedule)
        else:
            return node

        return self.balance(node)

    def find_by_position(self, fragment):
        ans = []
        self.search_doctor(self.root, ans, fragment=fragment)
        if len(ans) > 0:
            for node in ans:
                print(node)
        else:
            print("Нет врачей с подходящей должностью")

    def delete_doctor(self, fullname):
        self.root = self.delete_node(self.root, fullname)

    def find_min(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def delete_node(self, node, fullname):
        if not node:
            return node

        if fullname < node.fullname:
            node.left = self.delete_node(node.left, fullname)
        elif fullname > node.fullname:
            node.right = self.delete_node(node.right, fullname)
        else:
            if not node.left:
                return node.right

            elif not node.right:
                return node.left

            temp = self.find_min(node.right)
            node.fullname = temp.fullname
            node.position = temp.position
            node.num_cabinet = temp.num_cabinet
            node.schedule = temp.schedule
            node.right = self.delete_node(node.right, temp.fullname)

        if node is None:
            return node

        return self.balance(node)

    def add_doctor(self, real=True):
        if real:
            flag = True
            while flag:
                try:
                    fullname = input("Введите полное имя: ")
                    position = input("Введите должность: ")
                    num_cabinet = int(input("Введите номер кабинета: "))
                    schedule = input("Введите расписание (формат: 10:00-18:30): ")

                    flag = validate_fields_doctor(fullname, position, schedule, num_cabinet)

                except ValueError:
                    print("*************************************************")
                    print("Ошибка: номер кабинета должен быть числом")
                    print("*************************************************")
            self.root = self.insert(self.root, fullname, position, num_cabinet, schedule)
        else:
            self.root = self.insert(self.root, "Иванов И. И.", "Терапевт", 11, "09:00-17:00")
            self.root = self.insert(self.root, "Катинова М. В.", "Терапевт", 34, "10:00-18:30")
            self.root = self.insert(self.root, "Максимов О. В.", "Окулист", 75, "10:23-11:23")
            self.root = self.insert(self.root, "Сидоров В. Н.", "Хирург", 35, "11:00-19:00")

    def find_doctor(self, fullname):
        return self.find_doctor_node(self.root, fullname)

    def find_doctor_node(self, node, fullname):
        if node is None:
            return None
        if fullname < node.fullname:
            return self.find_doctor_node(node.left, fullname)
        elif fullname > node.fullname:
            return self.find_doctor_node(node.right, fullname)
        else:
            return node

    def clear(self):
        self.root = None
