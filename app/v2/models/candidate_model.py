from app.v2.utils.validator import validate_ints
from .base_model import BaseModel
from .office_model import Office
from .party_model import Party
from .user_model import User


class Candidate(BaseModel):
    """ model for political candidate """

    def __init__(self, party=None, office=None, candidate=None, id=None):
        super().__init__('Candidate', 'candidates')

        self.party = party
        self.office = office
        self.candidate = candidate
        self.id = id

    def save(self):
        """save candidate to db """

        data = super().save(
            'party, office, candidate', self.party, self.office,
            self.candidate)

        self.id = data.get('id')
        return data

    def load_all(self):
        """ Inner joins all relevant tables to create candidate objects """

        query = """
        SELECT concat_ws(' ', firstname, lastname) AS candidate,
         offices.name as office,parties.name as party, candidates.id,
         users.passport_url
         FROM candidates
         INNER JOIN users ON users.id = candidates.candidate
         INNER JOIN parties ON parties.id = candidates.party
         INNER JOIN offices ON offices.id = candidates.office
        """
        return self.get_all(query)

    def find_by(self, key, value):
        """ Inner joins all relevant tables to create a candidate object """

        query = """
        SELECT concat_ws(' ', firstname, lastname) AS candidate,
         offices.name as office,parties.name as party, candidates.id,
         users.passport_url
         FROM candidates
         INNER JOIN users ON users.id = candidates.candidate
         INNER JOIN parties ON parties.id = candidates.party
         INNER JOIN offices ON offices.id = candidates.office
         WHERE candidates.{} = '{}'
        """.format(key, value)
        return self.get_one(query)

    def find_all(self, key, value):
        """ Inner joins all relevant tables to create a candidate object """

        query = """
        SELECT concat_ws(' ', firstname, lastname) AS candidate,
         offices.name as office,parties.name as party, candidates.id,
         users.passport_url
         FROM candidates
         INNER JOIN users ON users.id = candidates.candidate
         INNER JOIN parties ON parties.id = candidates.party
         INNER JOIN offices ON offices.id = candidates.office
         WHERE candidates.{} = '{}'
        """.format(key, value)
        return self.get_all(query)

    def as_json(self):
        # get the object as a json
        return {
            "id": self.id,
            "party": self.party,
            "office": self.office,
            "candidate": self.candidate
        }

    def from_json(self, json):
        self.__init__(json['party'], json['office'], json['candidate'])
        self.id = json['id']
        return self

    def validate_object(self):
        """ validates the object """

        ok = True

        validate_ints(self.as_json(), 'party', 'office', 'candidate')

        if self.find_by('candidate', self.candidate):
            self.error_message = "{} already exists".format(self.object_name)
            self.error_code = 409
            ok = False

        elif not Office().find_by('id', self.office):
            self.error_message = 'Selected Office does not exist'
            self.error_code = 404
            ok = False

        elif not Party().find_by('id', self.party):
            self.error_message = 'Selected Party does not exist'
            self.error_code = 404
            ok = False

        elif not User().find_by('id', self.candidate):
            self.error_message = 'Selected User does not exist'
            self.error_code = 404
            ok = False

        return ok
