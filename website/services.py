from website.models import DeliveryType, UserAddress, ContactInfo, Advert, Order, User, Category, AdvertStatus


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
            return order

    def validate_data(self):
        return True


class OrderService:

    @staticmethod
    def get_orders_for_user(user: User):
        return Order.objects.filter(buyer=user)

    @staticmethod
    def get_all_orders():
        return Order.objects.all()


class CategoryService:

    @staticmethod
    def get_category_and_descendants(category_url):
        category = Category.objects.get(url=category_url)
        self_and_descendants = CategoryService.__get_all_descendants(category, set())
        self_and_descendants.add(category)
        return self_and_descendants

    @staticmethod
    def __get_all_descendants(category, result_set):
        for category in category.category_set.all():
            result_set.add(category)
            CategoryService.__get_all_descendants(category, result_set)
        return result_set


class AdvertService:

    ADVERT_STATUS_ACTIVE = AdvertStatus.objects.get_by_label("ADVERT_ACTIVE")

    @staticmethod
    def get_active_adverts_for_categories(category_list):
            return Advert.objects.filter(category__in=category_list,
                                           status=AdvertService.ADVERT_STATUS_ACTIVE)


    @staticmethod
    def get_active_adverts():
            return Advert.objects.filter(status=AdvertService.ADVERT_STATUS_ACTIVE)

