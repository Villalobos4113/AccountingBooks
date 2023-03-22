class AccountMovement:

    """
        Represents a single movement of funds in an account, either a debit or a credit.

        Attributes:
        -----------
        account_id : int
            The unique identifier of the account the movement is associated with.
        quantity : float
            The amount of money involved in the movement, expressed in dollars.
        d_c : str
            A string representing the type of movement. Must be either 'D' (for debit) or 'C' (for credit).

        Methods:
        --------
        __init__(account_id: int, quantity: float, d_c: str):
            Initializes a new AccountMovement instance with the given parameters.
        __str__() -> str:
            Returns a string representation of the AccountMovement instance.
        account_id() -> int:
            Returns the account_id attribute.
        quantity() -> float:
            Returns the quantity attribute.
        d_c() -> str:
            Returns the d_c attribute.

    """

    def __init__(self, account_id: int, quantity: float, d_c: str):
        self._account_id = account_id
        self._quantity = quantity
        self._d_c = d_c.upper()

    def __str__(self) -> str:
        return f"Account: {self._account_id}, Quantity: ${self.quantity}, Type: {'Debit' if self._d_c == 'D' else 'Credit'}"

    @property
    def account_id(self) -> int:
        return self._account_id

    @account_id.setter
    def account_id(self, account_id: int) -> None:
        pass

    @property
    def quantity(self) -> float:
        return self._quantity

    @quantity.setter
    def quantity(self, quantity: float) -> None:
        pass

    @property
    def d_c(self) -> str:
        return self._d_c

    @d_c.setter
    def d_c(self, d_c: str) -> None:
        pass
