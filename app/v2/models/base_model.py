from app.v1.utils.validator import generate_id, exists, validate_ints
from app.v2.db.database_config import Database


class BaseModel(Database):
    """ model that defines all models """

    def __init__(self, object_name, table_name):
        self.table_name = table_name
        self.object_name = object_name
        self.error_message = ""
        self.error_code = 200

    def as_json(self):
        pass

    def params_to_values(self, params):
        f = ["'{}'".format(i) for i in params]
        return ", ".join(f)

    def save(self, fields, *values):
        """ save the object to table """

        query = "INSERT INTO {} ({}) \
        VALUES ({}) RETURNING *".format(
            self.table_name, fields, self.params_to_values(values)
        )
        print(query)
        return super().insert(query)

    def delete(self, id):
        """ Remove item from table """

        query = "DELETE FROM {} WHERE id = {}".format(self.table_name, id)

        self.execute(query)

    def validate_object(self):
        """This function validates an object and rejects or accepts it"""

        return True

    def find_by(self, key, value):
        """ Find object from table and return """

        query = "SELECT * FROM {} WHERE {} = '{}'".format(
            self.table_name, key, value)

        return self.get_one(query)

    def from_json(self, json):
        return self
