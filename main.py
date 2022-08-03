from abc import ABC, abstractmethod




class Storage(ABC):
    @abstractmethod
    def __init__(self, items, capacity):
        self._items = items
        self._capacity = capacity

    @abstractmethod
    def add(self, title, count):
        pass

    @abstractmethod
    def remove(self, title, count):
        pass

    @property
    @abstractmethod
    def get_free_space(self):
        pass

    @property
    @abstractmethod
    def items(self):
        pass

    @property
    @abstractmethod
    def get_unique_items_count(self):
        pass


class Store(Storage):
    def __init__(self):
        self._items = {}
        self._capacity = 100

    def add(self, title, count): #функция добавления товара
        if title in self._items:
            self._items[title] += count #увеличиваем кол-во items, если товар уже есть в словаре
        else:
            self._items[title] = count #иначе просто добавляем в словарь
        self._capacity -= count  #уменьшаем кол-во свободного места

    def remove(self, title, count): #функция удаления товара
        res = self._items[title] - count
        if res > 0:
            self._items[title] = res #перезаписываем кол-во items, если остается какое-то кол-во
        else:
            del self._items[title] #удаляем товар, которого уже нет
        self._capacity += count  # освобождаем кол-во свободного места

    @property
    def get_free_space(self): #функция получения свободного места на складе
        return self._capacity

    @property
    def items(self): #функция получения содержания склада в словаре
        return self._items

    @items.setter
    def items(self, new_items):
        self._items = new_items
        self._capacity -= sum(self._items.values())

    @property
    def get_unique_items_count(self): #функция получения количества уникальных товаров
        return len(self._items.keys())


class Shop(Store):
    def __init__(self):
        super().__init__()
        self._capacity = 20


class Request:
    def __init__(self, info): #info - какая-то строка
        self.info = self._split_info(info)
        self.from_ = self.info[4]
        self.to = self.info[6]
        self.amount = int(self.info[1])
        self.product = self.info[2]

    @staticmethod
    def _split_info(info):
        #print(info)
        #print(info.split(" "))
        return info.split(" ")

    def __repr__(self):
        return f'Доставить {self.amount} {self.product} из {self.from_} в {self.to}'


def main():
    while(True):
        user_input = "Доставить 13 печеньки из склад в магазин"

        if user_input == 'stop':
            break

        request = Request(user_input)

        store.items = store_items
        #print(store.items)
        #print(store.get_free_space)

        from_ = store if request.from_ == 'склад' else shop     #склад
        to = store if request.to == 'склад' else shop           #магазин

        if request.product in from_.items:

            print(f'Нужный товар есть в пункте \"{request.from_}\"')
        else:
            print(f'В пункте {request.from_} нет данного товара ')
            continue

        if from_.items[request.product] >= request.amount: #если кол-во товара на складе больше запрошенного
            print(f'Нужное количество есть в пункте \"{request.from_}\"')
        else:
            print(f'В пункте \"{request.from_}\" не хватает {request.amount - from_.items[request.product]}')
            continue

        if to.get_free_space >= request.amount:
            print(f'В пункте \"{request.to}\" достаточно места')
        else:
            print(to.get_free_space)
            print(f'В пункте \"{request.to}\" не хватает {request.amount - to.get_free_space}')
            continue

        if request.to == 'магазин' and to.get_unique_items_count == 5 and request.product not in to.items: # уникальное значение для магазина должно быть больше пяти
            print('В магазине достаточно уникальных значений')
            continue

        from_.remove(request.product, request.amount)
        print(f'Курьер забрал {request.amount} {request.product} из пункта \"{request.from_}\"')
        print(f'Курьер везет {request.amount} {request.product}  из пункта \"{request.from_}\" в пункт \"{request.to}\"')
        to.add(request.product, request.amount)
        print(f'Курьер доставил {request.amount} {request.product} в пункт \"{request.to}\"')

        print(' ')
        print('На складе:')
        for title, count in store.items.items():
            print(f'{title}: {count}')

        print(' ')
        print('В магазине:')
        for title, count in shop.items.items():
            print(f'{title}: {count}')


        #break


if __name__ == "__main__":

    store = Store()
    shop = Shop()

    #print(request)

    store_items = {
        'кукуруза': 10,
        'кола': 10,
        'конфеты': 18,
        'печеньки': 7,
    }
    main()