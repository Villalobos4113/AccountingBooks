from Accounting.classes.account_movement import AccountMovement
from Accounting.classes.account import Account


class Statement:

    """
        Represents an accounting statement with accounts.

        Attributes:
        -----------
        name : str
            The name of the account.
        nature : str
            Statement's nature, "D" if debtor or "C" if creditor.
        accounts : dict[int: Accounts]
            All the statement's accounts with the account's ids as keys.

        Methods:
        --------
        __init__(name: str, nature: str):
            Initializes a new Statement instance with the given parameters.
        __str__() -> str:
            Returns a string representation of the statement instance.
        name() -> str:
            Returns the name attribute.
        nature() -> str:
            Returns the nature attribute.
        accounts() -> dict[int: Accounts]:
            Returns the accounts attribute
        accounts(account: Account) -> None:
            Adds account.
            Raises exception if account id already exists in the accounts.
        account_movement(account_movement: AccountMovement) -> None:
            Record the account movement in the corresponding account.
            Raises exception if the AccountMovement's account id doesn't exist.
            Raises exception if the AccountMovement's d_c isn't a valid option.
    """

    def __init__(self, name: str, nature: str):
        self._name = name
        self._nature = nature.upper()
        self._accounts: dict[int, Account] = {}

    def __str__(self) -> str:
        keys = sorted(self._accounts.keys())
        bal = self.balance()

        res = "=" * 27 + "STATEMENT" + "=" * 27 + "\n"
        res += f"  Name: {self._name}\n"
        res += f"  Nature: {'Debtor' if self._nature == 'D' else 'Creditor'}\n"
        res += f"  Balance: {'-' if bal < 0 else ''}${abs(bal)}\n"
        res += f"  Accounts:\n" if len(keys) > 0 else ""

        for key in keys:
            res += f"{self._accounts[key]}\n"

        res += "=" * 64

        return res

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: int) -> None:
        pass

    @property
    def nature(self) -> str:
        return self._nature

    @nature.setter
    def nature(self, nature: str) -> None:
        pass

    @property
    def accounts(self) -> dict[int: Account]:
        return self._accounts.copy()

    def add_account(self, account_id: int, name: str) -> None:
        if account_id in self._accounts:
            raise Exception("ERROR: Account ID already exists.")

        self._accounts[account_id] = Account(account_id, name, self._nature)

    def account_movement(self, account_movement: AccountMovement) -> None:
        if account_movement.account_id not in self._accounts:
            raise Exception("ERROR: Account '" + str(account_movement.account_id) + "' doesn't exist.")

        if account_movement.d_c == "D":
            self._accounts[account_movement.account_id].debits = account_movement

        elif account_movement.d_c == "C":
            self._accounts[account_movement.account_id].credits = account_movement

        else:
            raise Exception("ERROR: Account Movement d_c's '" + account_movement.d_c + "' isn't a valid type.")

    def balance(self) -> int:
        res = 0

        for account in self._accounts.values():
            account_balance = account.balance()

            if account_balance.d_c == self._nature:
                res += account_balance.quantity
            else:
                res -= account_balance.quantity

        return res
