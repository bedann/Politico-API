from app.v1.utils.validator import generate_id, exists, validate_ints


class BaseModel():
    """ model that defines all models """

    def __init__(self, object_name, table):
        self.table = table
        self.object_name = object_name
        self.error_message = ""
        self.error_code = 200
        self.id = generate_id(table)

    def as_json(self):
        pass

    def save(self):
        """ save the object to table """
        self.table.append(self.as_json())

    def delete(self):
        """ Remove item from list and return instance """
        for i in range(len(self.table)):
            if self.table[i]['id'] == self.id:
                return self.table.pop(i)

    def validate_object(self):
        """This function validates an object and rejects or accepts it"""

        return True

    def find_by_id(self, id):
        """ Find object from list and return instance """
        self.id = id

        for i in range(len(self.table)):
            if self.table[i]['id'] == id:
                return self.table[i]
        return None

    def from_json(self, json):
        return self
