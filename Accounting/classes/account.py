from Accounting.classes.account_movement import AccountMovement


class Account:
    """
        Represents an account with account movements.

        Attributes:
        -----------
        account id : int
            The unique identifier for the account instance.
        name : str
            The name of the account.
        credits : list[AccountMovement]
            All credit's AccountMovements associated with the account.
        debits : list[AccountMovement]
            All debit's AccountMovements associated with the account.

        Methods:
        --------
        __init__(account_id: int, name: str):
            Initializes a new Account instance with the given parameters.
        __str__() -> str:
            Returns a string representation of the account instance.
        account_id() -> int:
            Returns the account id attribute.
        name() -> str:
            Returns the name attribute.
        credits() -> AccountMovement:
            Returns the credits attribute
        credits(credit: AccountMovement) -> None:
            Sets the credit attribute if none have been set.
            Raises exception if credit balance and debit balance don't match or credit and debit accounts are the same.
        debits() -> AccountMovement:
            Returns the debits attribute.
        debits(debit: AccountMovement) -> None:
            Sets the debit attribute if none have been set.
            Raises exception if credit balance and debit balance don't match or credit and debit accounts are the same.
    """

    def __init__(self, account_id: int, name: str, nature: str):
        self._account_id = account_id
        self._name = name
        self._nature = nature.upper()
        self._credits: list[AccountMovement] = []
        self._debits: list[AccountMovement] = []

    def __str__(self) -> str:
        bal = self.balance()

        res = "=" * 27 + "ACCOUNT" + "=" * 27 + "\n"
        res += f"  Name: {self._name}\n"
        res += f"  ID: {self._account_id}\n"
        res += f"  Balance: {'-' if bal.d_c != self._nature else ''}${bal.quantity}\n"
        res += f"  Credits:\n" if len(self._credits) > 0 else ""

        for credit in self._credits:
            res += f"    {credit}\n"

        res += f"  Debits:\n" if len(self._debits) > 0 else ""

        for debit in self._debits:
            res += f"    {debit}\n"

        res += "=" * 62

        return res

    @property
    def account_id(self) -> int:
        return self._account_id

    @account_id.setter
    def account_id(self, account_id: int) -> None:
        pass

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        pass

    @property
    def credits(self) -> [AccountMovement]:
        return self._credits.copy()

    @credits.setter
    def credits(self, account_movement: AccountMovement) -> None:
        if account_movement.account_id == self._account_id:
            self._credits.append(account_movement)
        else:
            raise Exception("ERROR: AccountMovement's account id doesn't match self account id.")

    @property
    def debits(self) -> [AccountMovement]:
        return self._debits.copy()

    @debits.setter
    def debits(self, account_movement: AccountMovement) -> None:
        if account_movement.account_id == self._account_id:
            self._debits.append(account_movement)
        else:
            raise Exception("ERROR: AccountMovement's account id doesn't match self account id.")

    def balance(self) -> AccountMovement:
        credit_balance = 0
        debit_balance = 0

        for credit in self._credits:
            credit_balance += credit.quantity

        for debit in self._debits:
            debit_balance += debit.quantity

        if credit_balance > debit_balance:
            return AccountMovement(000000, credit_balance - debit_balance, "C")
        elif debit_balance > credit_balance:
            return AccountMovement(000000, debit_balance - credit_balance, "D")
        else:
            return AccountMovement(000000, debit_balance - credit_balance, self._nature)
