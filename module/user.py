from module.table import TableRow, Table


class User(TableRow):
    def __init__(self, first_name: str, last_name: str, _id: int = None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0
        self.balance_details = {}
        self._id = _id
        super().__init__(self._id)

    def _recalibrate_balance(self):
        self.balance = sum([points for points in self.balance_details.values()])

    def _update_balance_and_details(self, transaction):
        update_dict = transaction.to_dict()
        payer = update_dict["payer"]
        if self.balance_details.get(payer):
            self.balance_details[payer] += update_dict["points"]
        else:
            self.balance_details[payer] = update_dict["points"]
        self._recalibrate_balance()

    # had to pass the transactions table as an argument to avoid circular import
    # in prod, i'd create a database to log transactions and users
    def spend_points(self, points: int, transactions_table):
        ordered_transactions_table = transactions_table.sort_by_field("timestamp")
        user_transactions = [trs for trs in ordered_transactions_table if trs.user_id == self._id]
        if len(user_transactions) == 0 or points > self.balance:
            return -1
        idx = 0
        while points > 0 and idx < len(user_transactions):
            for transaction in user_transactions:
                if self.balance_details[transaction.payer] == 0:
                    continue
                if points <= self.balance_details[transaction.payer]:
                    self.balance_details[transaction.payer] -= points
                    points = 0
                else:
                    offset = points - self.balance_details[transaction.payer]
                    self.balance_details[transaction.payer] -= offset
                    points -= offset
                idx += 1
        self._recalibrate_balance()
        return points


class Users(Table):
    def __init__(self):
        super().__init__()







