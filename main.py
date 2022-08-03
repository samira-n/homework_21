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
        user_input = input('Введите данные:')
        #user_input = "Доставить 3 кола из склад в магазин"

        if user_input == 'stop':
            break

        request = Request(user_input)

        store.items = store_items

        from_ = None
        to = None

        # from_ = store if request.from_ == 'склад' else shop  # склад
        # to = store if request.to == 'склад' else shop  # магазин

        if request.from_ == request.to:
            print('Пункт назначение == Пункт отправки')
            continue

        if request.from_ == 'склад':
            if request.product in store.items:
                print(f'Нужный товар есть в пункте \"{request.from_}\"')
            else:
                print(f'В пункте {request.from_} нет данного товара ')
                break

            if store.items[request.product] >= request.amount: #если кол-во товара на складе больше запрошенного
                print(f'Нужное количество есть в пункте \"{request.from_}\"')
            else:
                print(f'В пункте \"{request.from_}\" не хватает {request.amount - store.items[request.product]}')
                break

            if shop.get_free_space >= request.amount:
                print(f'В пункте \"{request.to}\" достаточно места')
            else:
                print(shop.get_free_space)
                print(f'В пункте \"{request.to}\" не хватает {request.amount - shop.get_free_space}')
                continue

            if request.to == 'магазин' and shop.get_unique_items_count == 5 and request.product not in shop.items: # уникальное значение для магазина должно быть больше пяти
                print('В магазине достаточно уникальных значений')
                continue

            store.remove(request.product, request.amount)
            print(' ')
            print(f'Курьер забрал {request.amount} {request.product} из пункта \"{request.from_}\"')
            print(f'Курьер везет {request.amount} {request.product}  из пункта \"{request.from_}\" в пункт \"{request.to}\"')
            shop.add(request.product, request.amount)
            print(f'Курьер доставил {request.amount} {request.product} в пункт \"{request.to}\"')

        else:
            if request.product in shop.items:
                print(f'Нужный товар есть в пункте \"{request.from_}\"')
            else:
                print(f'В пункте {request.from_} нет данного товара ')
                continue

            if shop.items[request.product] >= request.amount:  # если кол-во товара на складе больше запрошенного
                print(f'Нужное количество есть в пункте \"{request.from_}\"')
            else:
                print(f'В пункте \"{request.from_}\" не хватает {request.amount - shop.items[request.product]}')
                continue

            if store.get_free_space >= request.amount:
                print(f'В пункте \"{request.to}\" достаточно места')
            else:
                print(store.get_free_space)
                print(f'В пункте \"{request.to}\" не хватает {request.amount - store.get_free_space}')
                continue


            shop.remove(request.product, request.amount)
            print(' ')
            print(f'Курьер забрал {request.amount} {request.product} из пункта \"{request.from_}\"')
            print(
                f'Курьер везет {request.amount} {request.product}  из пункта \"{request.from_}\" в пункт \"{request.to}\"')
            store.add(request.product, request.amount)
            print(f'Курьер доставил {request.amount} {request.product} в пункт \"{request.to}\"')

        print(' ')
        print('На складе:')
        for title, count in store.items.items():
            print(f'{title}: {count}')

        print(' ')
        print('В магазине:')
        for title, count in shop.items.items():
            print(f'{title}: {count}')


        break


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