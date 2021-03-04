import datetime
import json

from module.utility import COLUMN_EXCLUSION


class TableRow(object):
    def __init__(self, _id=None):
        self._id = _id

    @classmethod
    def from_json(cls, _json):
        return cls(**json.loads(_json))

    def to_dict(self, dates_to_string=False):
        data = self.__dict__
        for key, value in data.items():
            if dates_to_string:
                if type(value) == datetime.datetime:
                    data[key] = value.isoformat()
            else:
                if type(value) != datetime.datetime:
                    try:
                        data[key] = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
                    except:
                        data[key] = value
                else:
                    data[key] = value
        return data

    def to_json(self):
        return json.dumps(self.to_dict(dates_to_string=True))


class Table:
    def __init__(self):
        self.idx = 0
        self.rows = []

    def find_row(self, _id):
        return next(filter(lambda row: row._id == _id, self), None)

    def add(self, row: TableRow):
        data = {key: value for key, value in row.__dict__.items() if key not in COLUMN_EXCLUSION}
        if row._id:
            self.rows.append(type(row)(**data))
            return self.find_row(row._id)
        else:
            new_id = max([row._id for row in self]) + 1 if len(self) > 0 else 1
            data["_id"] = new_id
            self.rows.append(type(row)(**data))
            return self.find_row(new_id)

    def delete(self, _id):
        row = self.find_row(_id)
        if not row:
            return
        idx = self.rows.index(row)
        return self.rows.pop(idx)

    def update(self, _id, update_dict):
        row = self.find_row(_id)
        if not row:
            return
        self.delete(row._id)
        data = row.to_dict()
        data.update(update_dict)
        self.add(type(row)(**data))
        return self.find_row(_id)

    def to_json(self):
        return [row.to_json() for row in self]

    def __next__(self):
        self.idx += 1
        try:
            return self.rows[self.idx - 1]
        except IndexError:
            raise StopIteration

    def __iter__(self):
        return iter(self.rows)

    def __len__(self):
        return len(self.rows)
