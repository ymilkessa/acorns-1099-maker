class RecipientInfo:
    name = None
    tin = None
    street_address = None
    city = None
    state = None
    zip_code = None

    def __init__(self, name, tin, street_address, city, state, zip_code):
        self.name = name
        self.tin = tin
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def get_city_state_zip(self):
        return f"{self.city}, {self.state} {self.zip_code}"

    @staticmethod
    def get_user_info_from_console():
        print("Enter the following information:")
        tin = input("TIN: \n>")
        name = input("Name: \n>")
        street_address = input("Street Address: \n>")
        city = input("City: \n>")
        state = input("State: \n>")
        zip_code = input("Zip Code: \n>")
        return RecipientInfo(tin, name, street_address, city, state, zip_code)
