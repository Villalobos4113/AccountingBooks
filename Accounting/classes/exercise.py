from Accounting.classes.policy import Policy
from Accounting.classes.statement import Statement
from Accounting.classes.account_movement import AccountMovement

from datetime import datetime
from copy import deepcopy


class Exercise:
    """
        Represents an accounting exercise with statements.

        Attributes:
        -----------
        company name : str
            The name of the company
        name : str
            The name of the exercise.
        exercise : datetime
            The date and time the exercise was created.
        statements : [Statement]
            All the statements involved in the exercise (Assets, Liabilities, Common Stock, Revenue and Expenses).
        policies : [Policy]
            All the policies involved in the exercise.

        Methods:
        --------
        __init__(name: str, nature: str):
            Initializes a new Exercise instance with the given parameters.
        __str__() -> str:
            Returns a string representation of the exercise instance.
        company_name() -> str:
            Returns the company name attribute.
        name() -> str:
            Returns the name attribute.
        exercise() -> datetime:
            Returns the exercise attribute.
        nature() -> str:
            Returns the nature attribute.
        statements() -> [Statement]:
            Returns the statements attribute
        policies() -> [Policy]:
            Returns the policies attribute
        policies(policy: Policy) -> None:
            Record the policy and all the account movements in their corresponding accounts.
            Raises exception if an account id doesn't belong to any statement.
            Raises exception if the AccountMovement's account id doesn't exist.
            Raises exception if the AccountMovement's d_c isn't a valid option.
        add_account(account_id: int, name: str) -> None:
            Adds account to the corresponding statement.
            Raises exception if account id doesn't belong to any statement.
        next_policy_invoice() -> int:
            Returns the next policy invoice.
        get_all_accounts() -> list[str]:
            Returns all account's id in the exercise.
    """

    def __init__(self, company_name: str, name: str):
        self._company_name = company_name
        self._name = name
        self._exercise = datetime.now()
        self._statements = []
        self._policies = []

        self._statements.append(Statement("Assets", "d"))
        self._statements.append((Statement("Liabilities", "c")))
        self._statements.append(Statement("Common Stock", "c"))
        self._statements.append(Statement("Revenue", "c"))
        self._statements.append(Statement("Expenses", "d"))

    def __str__(self) -> str:
        res = "=" * 29 + "EXERCISE" + "=" * 29 + "\n"
        res += f"  Company Name: {self._company_name}\n"
        res += f"  Name: {self._name}\n"
        res += f"  Exercise: {self._exercise.strftime('%Y')}\n"
        res += "  Statements:\n"

        for statement in self._statements:
            res += f"\n{statement}\n"

        res += "  \nPolicies:\n" if len(self._policies) > 0 else ""

        for policy in self._policies:
            res += f"\n{policy}\n"

        res += "=" * 66

        return res

    @property
    def company_name(self) -> str:
        return self._company_name

    @company_name.setter
    def company_name(self, company_name: str) -> None:
        pass

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        pass

    @property
    def exercise(self) -> datetime:
        return deepcopy(self._exercise)

    @exercise.setter
    def exercise(self, exercise: datetime) -> None:
        pass

    @property
    def statements(self) -> list[Statement]:
        return deepcopy(self._statements)

    @statements.setter
    def statements(self, statements: list[Statement]) -> None:
        pass

    @property
    def policies(self) -> list[Policy]:
        return deepcopy(self._policies)

    @policies.setter
    def policies(self, policy: Policy) -> None:
        id_statement_credit = policy.credit.account_id // 100000
        id_statement_debit = policy.debit.account_id // 100000

        if id_statement_credit < 1 or id_statement_credit > 5:
            raise Exception("ERROR: Credit account ID '" + str(policy.credit.account_id) + "' doesn't belong to any any statement")
        if id_statement_debit < 1 or id_statement_debit > 5:
            raise Exception("ERROR: Debit account ID '" + str(policy.credit.account_id) + "' doesn't belong to any any statement")

        self._statements[id_statement_credit - 1].account_movement(policy.credit)
        self._statements[id_statement_debit - 1].account_movement(policy.debit)

        self._policies.append(policy)

    def add_account(self, account_id: int, name: str) -> None:
        id_account = account_id // 100000

        if id_account < 1 or id_account > 5:
            raise Exception("ERROR: Account ID '" + str(account_id) + "' doesn't belong to any any statement")

        self._statements[id_account - 1].add_account(account_id, name)

    def next_policy_invoice(self) -> int:
        return len(self._policies) + 1

    def get_all_accounts(self) -> list[str]:
        lst = []

        for statement in self._statements:
            for account in statement.accounts:
                lst.append(str(account))

        return lst

    def check_accounting_equation(self) -> bool:
        return self._statements[0].balance() == (self._statements[1].balance() + self._statements[2].balance() + self._statements[3].balance() - self._statements[4].balance())

    def balance_sheet(self) -> str:
        bal_assets = self._statements[0].balance()
        bal_liabilities = self._statements[1].balance()
        bal_common_stock = self._statements[2].balance()
        bal_revenue = self._statements[3].balance()
        bal_expenses = self._statements[4].balance()

        res = "=" * 29 + "EXERCISE" + "=" * 29 + "\n"
        res += f"  Company Name: {self._company_name}\n"
        res += f"  Name: {self._name}\n"
        res += f"  Exercise: {self._exercise.strftime('%Y')}\n\n"
        res += f"    Assets                          {'-' if bal_assets < 0 else ''}${abs(bal_assets)}\n"
        res += f"    Expenses                     {'-' if bal_expenses < 0 else ''}${abs(bal_expenses)}\n"
        res += f"      Liabilities                                          {'-' if bal_liabilities < 0 else ''}${abs(bal_liabilities)}\n"
        res += f"      Common Stock                                {'-' if bal_common_stock < 0 else ''}${abs(bal_common_stock)}\n"
        res += f"      Revenue                                            {'-' if bal_revenue < 0 else ''}${abs(bal_revenue)}\n\n"
        res += f"                                         {'-' if bal_assets + bal_expenses < 0 else ''}${abs(bal_assets + bal_expenses)}\n"
        res += f"                                                                {'-' if bal_liabilities + bal_common_stock + bal_revenue < 0 else ''}${abs(bal_liabilities + bal_common_stock + bal_revenue)}\n"
        res += "=" * 66

        return res

    def income_statement(self) -> str:
        bal_revenue = self._statements[3].balance()
        bal_expenses = self._statements[4].balance()
        bal_utilities = bal_revenue - bal_expenses

        res = "=" * 29 + "EXERCISE" + "=" * 29 + "\n"
        res += f"  Company Name: {self._company_name}\n"
        res += f"  Name: {self._name}\n"
        res += f"  Exercise: {self._exercise.strftime('%Y')}\n\n"
        res += f"    Revenue                       {'-' if bal_revenue < 0 else ''}${abs(bal_revenue)}\n"
        res += f"      Expenses                                          {'-' if bal_expenses < 0 else ''}${abs(bal_expenses)}\n\n"
        res += f"    {'  ' if bal_utilities < 0 else ''}Operating Income{'                            ' if bal_utilities < 0 else '       '}${abs(bal_utilities)}\n"
        res += "=" * 66

        return res

    def close_book(self) -> dict[str: int]:
        try:
            self._statements[2].add_account(300100, "Retained Earnings")
        except Exception:
            pass

        revenue_bal = 0
        expenses_bal = 0

        for account in self._statements[3].accounts.values():
            account_balance = account.balance()

            policy = Policy(self.next_policy_invoice(), f"Closing revenue account '{account.name}'.")
            policy.debit = AccountMovement(account.account_id, account_balance.quantity, "d")
            policy.credit = AccountMovement(300100, account_balance.quantity, "c")
            self.policies = policy

            revenue_bal += account_balance.quantity

        for account in self._statements[4].accounts.values():
            account_balance = account.balance()

            policy = Policy(self.next_policy_invoice(), f"Closing expenses account '{account.name}'.")
            policy.debit = AccountMovement(300100, account_balance.quantity, "d")
            policy.credit = AccountMovement(account.account_id, account_balance.quantity, "c")
            self.policies = policy

            expenses_bal += account_balance.quantity

        income_tax = 0.3 * (revenue_bal - expenses_bal)

        if income_tax > 0:
            try:
                self._statements[1].add_account(200100, "Income Tax Payable")
            except Exception:
                pass

            policy = Policy(self.next_policy_invoice(), "Income Tax Payable of Exercise.")
            policy.debit = AccountMovement(300100, income_tax, "d")
            policy.credit = AccountMovement(200100, income_tax, "c")
            self.policies = policy
