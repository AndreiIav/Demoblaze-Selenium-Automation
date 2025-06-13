class ProductToCartFlow:
    def __init__(self, product_page, products_page):
        self.product_page = product_page
        self.products_page = products_page

    def add_product_to_cart_and_get_product(self, category_button, product_name):
        """
        Adds a product to cart, constructs a Product object and returns the
        Product object.

        Args:
            category_button (str): Product category. Accepted values: "phones",
                "laptops", "monitors".
            product_name (str): The name of the product.
        Returns:
            product_object (Product)
        """
        self.products_page.click_categories_button(category_button=category_button)
        self.products_page.click_product_link(product_name=product_name)
        product_object = self.product_page.create_product()
        self.product_page.click_add_to_cart_button()
        self.product_page.get_alert_text()
        self.product_page.accept_alert()

        return product_object

    def add_product_to_cart(self, category_button, product_name):
        """
        Adds a product to cart.

        Args:
            category_button (str): Product category. Accepted values: "phones",
                "laptops", "monitors".
            product_name (str): The name of the product.
        Returns:
            None
        """
        self.products_page.click_categories_button(category_button=category_button)
        self.products_page.click_product_link(product_name=product_name)
        self.product_page.click_add_to_cart_button()
        self.product_page.get_alert_text()
        self.product_page.accept_alert()
