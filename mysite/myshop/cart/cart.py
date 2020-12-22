from decimal import Decimal
from django.conf import settings
from shop.models import Products

class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False, size='M'):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        product_id = str(product.id) + '/' + size
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price),
                                     'size': size}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product, Size='M'):
        """
        Удаление товара из корзины.
        """
        product_id = str(product.id) + '/' + Size
        if product_id in self.cart:
            self.cart[product_id]['quantity'] -= 1
            self.save()
            print( self.cart[product_id]['quantity'])
            if self.cart[product_id]['quantity'] ==0:
                del self.cart[product_id]
                self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = self.cart.keys()
        product_id = []
        pr = []
        # получение объектов product и добавление их в корзину
        for prod in product_ids:
            pr.append(prod)
            prod = prod[:prod.find('/')]
            product_id.append(int(prod))
        pr.sort()
        product_id.sort()
        for i in range(0, len(product_id)):
            product = Products.objects.filter(id=product_id[i])
            self.cart[str(pr[i])]['product'] = product[0]


        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True