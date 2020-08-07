from website.models import DeliveryType, UserAddress, ContactInfo, Advert, Order, User


class PlaceOrderService:

    def __init__(self, delivery_type: DeliveryType, address: UserAddress, ci: ContactInfo, advert: Advert):
        self.delivery_type = delivery_type
        self.address = address
        self.ci = ci
        self.advert = advert

    def place_order(self):
        if self.validate_data():
            order = Order()
            order.advert = self.advert
            order.advert.set_reserved()
            order.set_status_created()
            order.set_delivery(self.delivery_type, self.address)
            order.contact_info = self.ci
            order.save()


    def validate_data(self):
        return True


class OrderService:

    @staticmethod
    def get_orders_for_user(user: User):
        return Order.objects.filter(buyer=user)

    @staticmethod
    def get_all_orders():
        return Order.objects.all()
