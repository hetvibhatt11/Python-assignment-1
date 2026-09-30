# Custom Exceptions
class InsufficientBalanceError(Exception):
    pass


class AccountNotFoundError(Exception):
    pass


class InvalidAmountError(Exception):
    pass


# Account Class
class Account:

    def __init__(self, account_id, balance):
        self.account_id = account_id
        self._balance = balance
        self.history = []

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")

        self._balance += amount
        self.history.append("DEPOSIT " + str(amount))

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")

        if amount > self._balance:
            raise InsufficientBalanceError("Insufficient balance")

        self._balance -= amount
        self.history.append("WITHDRAW " + str(amount))


# Transaction Class
class Transaction:

    def __init__(self, transaction_type, from_account=None,
                 to_account=None, amount=0):

        self.transaction_type = transaction_type
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount


# Bank Class
class Bank:

    def __init__(self):
        self.accounts = {}
        self.history = []

    def add_account(self, account):
        self.accounts[account.account_id] = account

    def get_account(self, account_id):
        if account_id not in self.accounts:
            raise AccountNotFoundError("Account not found")

        return self.accounts[account_id]

    def deposit(self, account_id, amount):

        account = self.get_account(account_id)

        account.deposit(amount)

        self.history.append(
            Transaction("DEPOSIT", to_account=account_id, amount=amount)
        )

    def withdraw(self, account_id, amount):

        account = self.get_account(account_id)

        account.withdraw(amount)

        self.history.append(
            Transaction("WITHDRAW", from_account=account_id, amount=amount)
        )

    def transfer(self, from_id, to_id, amount):

        sender = self.get_account(from_id)
        receiver = self.get_account(to_id)

        # First check withdrawal
        sender.withdraw(amount)

        # Then deposit
        receiver.deposit(amount)

        self.history.append(
            Transaction(
                "TRANSFER",
                from_account=from_id,
                to_account=to_id,
                amount=amount
            )
        )


# Main Program
def main():

    bank = Bank()

    # Number of accounts
    n = int(input("Enter number of accounts: "))

    print("Enter account ID and initial balance:")

    for _ in range(n):

        account_id, balance = input().split()

        balance = int(balance)

        bank.add_account(
            Account(account_id, balance)
        )

    # Number of operations
    q = int(input("Enter number of operations: "))

    batch_number = 0
    in_batch = False
    batch_failed = False
    batch_start_balances = {}
    failed_batch = None

    print("Enter operations:")

    for _ in range(q):

        command = input().split()

        operation = command[0]

        # Start batch
        if operation == "BATCH_BEGIN":

            batch_number += 1
            in_batch = True
            batch_failed = False

            # Save balances before batch
            batch_start_balances = {
                account_id: account.balance
                for account_id, account in bank.accounts.items()
            }

        # End batch
        elif operation == "BATCH_END":

            if in_batch:

                if batch_failed:
                    # Rollback all balances
                    for account_id, balance in batch_start_balances.items():
                        bank.accounts[account_id]._balance = balance

                    failed_batch = batch_number

                in_batch = False

        # Deposit
        elif operation == "DEPOSIT":

            account_id = command[1]
            amount = int(command[2])

            try:
                bank.deposit(account_id, amount)

            except Exception:
                if in_batch:
                    batch_failed = True

        # Withdraw
        elif operation == "WITHDRAW":

            account_id = command[1]
            amount = int(command[2])

            try:
                bank.withdraw(account_id, amount)

            except Exception:
                if in_batch:
                    batch_failed = True

        # Transfer
        elif operation == "TRANSFER":

            from_id = command[1]
            to_id = command[2]
            amount = int(command[3])

            try:
                bank.transfer(from_id, to_id, amount)

            except Exception:
                if in_batch:
                    batch_failed = True

    # Print failed batch
    if failed_batch is not None:
        print("FAILED", failed_batch)

    # Print final balances
    for account_id in sorted(bank.accounts):
        print(account_id, bank.accounts[account_id].balance)


if __name__ == "__main__":
    main()
