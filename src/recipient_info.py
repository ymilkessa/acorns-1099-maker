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
