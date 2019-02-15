from app.v2.utils.validator import validate_ints
from app.v2.utils.validator import validate_strings
from .base_model import BaseModel


class Office(BaseModel):
    """ model for political office """

    def __init__(self, name=None, type=None, id=None):
        super().__init__('Office', 'offices')

        self.name = name
        self.type = type
        self.id = id

    def save(self):
        """save office to db """

        data = super().save('name, type', self.name, self.type)

        self.id = data.get('id')
        return data

    def as_json(self):
        # get the object as a json
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type
        }

    def from_json(self, json):
        self.__init__(json['name'], json['type'])
        self.id = json['id']
        return self

    def validate_object(self):
        """ validates the object """

        if not validate_strings(self.name, self.type):
            self.error_message = (
                "Invalid or empty string")
            self.error_code = 422
            return False

        if len(self.name) < 3:
            self.error_message = "The {} name provided is too short".format(
                self.object_name)
            self.error_code = 422
            return False

        if self.find_by('name', self.name):
            self.error_message = "{} already exists".format(self.object_name)
            self.error_code = 409
            return False

        return super().validate_object()
