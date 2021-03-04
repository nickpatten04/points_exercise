import datetime

from module.table import TableRow, Table
from module.constants.users import USERS_TABLE
from typing import List


class Transaction(TableRow):
    def __init__(self, user_id: int, payer: str, points: int, timestamp: str, _id: int = None):
        self.user_id = user_id
        self.payer = payer
        self.points = points
        self.timestamp = datetime.datetime.fromisoformat(str(timestamp))
        self._id = _id
        super().__init__(self._id)


class Transactions(Table):
    def __init__(self):
        super().__init__()

    @classmethod
    def from_list(cls, transaction_list: List[Transaction]):
        transactions = Transactions()
        [transactions.add(transaction, update_user_balance=False) for transaction in transaction_list]
        return transactions

    def add(self, transaction: Transaction, update_user_balance=True):
        if update_user_balance:
            user = USERS_TABLE.find_row(transaction.user_id)
            if not user:
                return
            validated_transaction = super().add(transaction)
            user._update_balance_and_details(validated_transaction)
            return validated_transaction
        return super().add(transaction)

    def sort_by_field(self, sort_field, ascending=True, in_place=False):
        list_to_sort = [(getattr(trs, "_id"), getattr(trs, sort_field)) for trs in self]
        sorted_list = sorted(list_to_sort, key=lambda x: x[1])
        sorted_transactions = []
        if ascending:
            idx = 0
            while idx < len(sorted_list):
                transaction = next(filter(lambda row: row._id == sorted_list[idx][0], self), None)
                if transaction:
                    sorted_transactions.append(transaction)
                idx += 1
        else:
            idx = len(sorted_list) - 1
            while idx >= 0:
                transaction = next(filter(lambda row: row._id == sorted_list[idx][0], self), None)
                if transaction:
                    sorted_transactions.append(transaction)
                idx -= 1
        if in_place:
            self.rows = sorted_transactions
            return
        else:
            return Transactions.from_list(sorted_transactions)



