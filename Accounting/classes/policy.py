from Accounting.classes.account_movement import AccountMovement

from datetime import datetime
from copy import deepcopy


class Policy:

    """
        Represents a policy with credit and debit movements.

        Attributes:
        -----------
        invoice : int
            The invoice number associated with the policy.
        description : str
            A short description of the policy.
        date : datetime
            The date and time when the policy was created.
        credit : AccountMovement
            The credit movement associated with the policy.
        debit : AccountMovement
            The debit movement associated with the policy.

        Methods:
        --------
        __init__(invoice: int, description: str):
            Initializes a new Policy instance with the given parameters.
        __str__() -> str:
            Returns a string representation of the policy instance.
        invoice() -> int:
            Returns the invoice attribute.
        description() -> str:
            Returns the description attribute.
        date() -> datetime:
            Returns the date attribute
        credit() -> AccountMovement:
            Returns the credit attribute
        credit(credit: AccountMovement) -> None:
            Sets the credit attribute if none have been set.
            Raises exception if credit balance and debit balance don't match or credit and debit accounts are the same.
        debit() -> AccountMovement:
            Returns the debit attribute.
        debit(debit: AccountMovement) -> None:
            Sets the debit attribute if none have been set.
            Raises exception if credit balance and debit balance don't match or credit and debit accounts are the same.

    """

    def __init__(self, invoice: int, description: str):
        self._invoice = invoice
        self._description = description
        self._date = datetime.now()
        self._credit: AccountMovement = None
        self._debit: AccountMovement = None

    def __str__(self) -> str:
        res = "=" * 27 + "POLICY" + "=" * 27 + "\n"
        res += f"  Invoice:      {self._invoice}\n"
        res += f"  Description: \"{self._description}\"\n"
        res += f"  Date:         {self._date.strftime('%A')} {self._date.strftime('%B')} {self._date.strftime('%d')} {self._date.strftime('%Y')}\n"
        res += f"  Movements:\n"
        res += f"    {self._credit}\n"
        res += f"    {self._debit}\n"
        res += "=" * 60
        return res

    @property
    def invoice(self) -> int:
        return self._invoice

    @invoice.setter
    def invoice(self, invoice: int) -> None:
        pass

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str) -> None:
        pass

    @property
    def date(self) -> datetime:
        return deepcopy(self._date)

    @date.setter
    def date(self, date: str) -> None:
        pass

    @property
    def credit(self) -> AccountMovement:
        return self._credit

    @credit.setter
    def credit(self, credit: AccountMovement) -> None:
        if self._credit is None:
            if self._debit is not None:
                if self._debit.quantity != credit.quantity:
                    raise Exception("ERROR: Credit and debit is not balanced.")
                elif self._debit.account_id == credit.account_id:
                    raise Exception("ERROR: Credit and debit accounts can not be the same.")

            self._credit = credit

    @property
    def debit(self) -> AccountMovement:
        return self._debit

    @debit.setter
    def debit(self, debit: AccountMovement) -> None:
        if self._debit is None:
            if self._credit is not None:
                if self._credit.quantity != debit.quantity:
                    raise Exception("ERROR: Credit and debit is not balanced.")
                elif debit.account_id == self._credit.account_id:
                    raise Exception("ERROR: Credit and debit accounts can not be the same.")

            self._debit = debit
