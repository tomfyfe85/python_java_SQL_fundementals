"""
Exercise 5: Complete Money Transfer System (40-Minute Test Simulation)

===================================
FINAL INTEGRATION EXERCISE
===================================

This exercise simulates what you might see in your Gr4vy coding test.

TIME LIMIT: Try to complete this in 40 minutes!

SCENARIO:

You're building a simple money transfer system for a fintech company.
The system must:
- Manage multiple accounts
- Support deposits and withdrawals
- Transfer money between accounts
- Use Decimal for all currency operations
- Handle errors gracefully

REQUIREMENTS:

You have already built the components in exercises 1-4:
1. Decimal basics
2. Custom exceptions
3. Account class
4. TransferService class

Now put it all together and add a simple command-line interface!

YOUR TASK:

Implement a simple CLI that allows users to:
1. Create accounts
2. Deposit money
3. Withdraw money
4. Transfer money between accounts
5. Check account balance
6. List all accounts

BONUS CHALLENGES (if you have time):

1. Add transaction history to Account class
2. Add a transaction ID to each transfer
3. Add a method to get account statement
4. Add interest calculation
5. Add different account types (Savings vs Checking)

===================================
STARTER CODE
===================================

Below is a minimal CLI to get you started.
You can expand it or rewrite it completely!
"""

from decimal import Decimal
from account_class import Account
from transfer_service import TransferService
from custom_exceptions import (
    TransferError,
    InsufficientFundsError,
    InvalidAmountError,
    AccountNotFoundError,
    SameAccountError
)

def display_menu() -> None:
    """Display the main menu"""
    print("\n" + "="*50)
    print("MONEY TRANSFER SYSTEM")
    print("="*50)
    print("1. Create Account")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Transfer Money")
    print("5. Check Balance")
    print("6. List All Accounts")
    print("7. Exit")
    print("="*50)

def create_account_interactive(service: TransferService) -> None:
    """Interactive account creation"""
    print("\n--- Create New Account ---")
    # TODO: Implement this
    # Get account_id, owner_name, initial_balance from user
    # Call service.create_account()
    # Handle exceptions
    pass

def deposit_interactive(service: TransferService) -> None:
    """Interactive deposit"""
    print("\n--- Deposit Money ---")
    # TODO: Implement this
    pass

def withdraw_interactive(service: TransferService) -> None:
    """Interactive withdrawal"""
    print("\n--- Withdraw Money ---")
    # TODO: Implement this
    pass

def transfer_interactive(service: TransferService) -> None:
    """Interactive transfer"""
    print("\n--- Transfer Money ---")
    # TODO: Implement this
    pass

def check_balance_interactive(service: TransferService) -> None:
    """Interactive balance check"""
    print("\n--- Check Balance ---")
    # TODO: Implement this
    pass

def list_accounts_interactive(service: TransferService) -> None:
    """List all accounts"""
    print("\n--- All Accounts ---")
    # TODO: Implement this
    pass

def main() -> None:
    """Main program loop"""
    service = TransferService()

    # Pre-populate with some test accounts
    service.create_account('ACC001', 'Alice', Decimal('1000.00'))
    service.create_account('ACC002', 'Bob', Decimal('500.00'))
    service.create_account('ACC003', 'Charlie', Decimal('250.00'))

    print("Welcome to the Money Transfer System!")
    print("Test accounts created:")
    print("  ACC001 (Alice): $1000.00")
    print("  ACC002 (Bob): $500.00")
    print("  ACC003 (Charlie): $250.00")

    while True:
        display_menu()
        choice = input("\nEnter your choice (1-7): ").strip()

        try:
            if choice == '1':
                create_account_interactive(service)
            elif choice == '2':
                deposit_interactive(service)
            elif choice == '3':
                withdraw_interactive(service)
            elif choice == '4':
                transfer_interactive(service)
            elif choice == '5':
                check_balance_interactive(service)
            elif choice == '6':
                list_accounts_interactive(service)
            elif choice == '7':
                print("\nThank you for using Money Transfer System!")
                break
            else:
                print("Invalid choice. Please enter 1-7.")

        except TransferError as e:
            print(f"\n❌ Error: {e}")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()


# ==========================================
# ALTERNATIVE: AUTOMATED TEST SUITE
# ==========================================
# If you prefer to skip the CLI and just demonstrate
# the system works, implement these test scenarios:

def run_test_scenarios() -> None:
    """Run automated test scenarios"""
    print("="*60)
    print("RUNNING AUTOMATED TEST SCENARIOS")
    print("="*60)

    service = TransferService()

    print("\n[Scenario 1: Account Creation]")
    alice = service.create_account('ACC001', 'Alice Smith', Decimal('1000.00'))
    bob = service.create_account('ACC002', 'Bob Jones', Decimal('500.00'))
    charlie = service.create_account('ACC003', 'Charlie Brown', Decimal('0.00'))
    print(f"✓ Created 3 accounts")

    print("\n[Scenario 2: Deposit Operations]")
    charlie_account = service.get_account('ACC003')
    charlie_account.deposit(Decimal('100.00'))
    print(f"✓ Charlie deposited $100, balance: ${charlie_account.get_balance()}")

    print("\n[Scenario 3: Simple Transfer]")
    service.transfer('ACC001', 'ACC002', Decimal('200.00'))
    print(f"✓ Transferred $200 from Alice to Bob")
    print(f"  Alice balance: ${service.get_account('ACC001').get_balance()}")
    print(f"  Bob balance: ${service.get_account('ACC002').get_balance()}")

    print("\n[Scenario 4: Multiple Transfers]")
    service.transfer('ACC002', 'ACC003', Decimal('100.00'))
    service.transfer('ACC001', 'ACC003', Decimal('50.00'))
    print(f"✓ Completed 2 more transfers")
    print(f"  Charlie balance: ${service.get_account('ACC003').get_balance()}")

    print("\n[Scenario 5: Error Handling - Insufficient Funds]")
    try:
        service.transfer('ACC003', 'ACC001', Decimal('10000.00'))
        print("❌ Should have raised InsufficientFundsError")
    except InsufficientFundsError as e:
        print(f"✓ Correctly rejected: {e}")

    print("\n[Scenario 6: Error Handling - Invalid Amount]")
    try:
        service.transfer('ACC001', 'ACC002', Decimal('-50.00'))
        print("❌ Should have raised InvalidAmountError")
    except InvalidAmountError as e:
        print(f"✓ Correctly rejected: {e}")

    print("\n[Scenario 7: Error Handling - Same Account]")
    try:
        service.transfer('ACC001', 'ACC001', Decimal('50.00'))
        print("❌ Should have raised SameAccountError")
    except SameAccountError as e:
        print(f"✓ Correctly rejected: {e}")

    print("\n[Scenario 8: Money Conservation Check]")
    total = service.get_total_money()
    print(f"✓ Total money in system: ${total}")
    print(f"✓ Expected: $1600.00")
    assert total == Decimal('1600.00'), "Money was created or destroyed!"

    print("\n[Scenario 9: Decimal Precision]")
    service.create_account('ACC004', 'Dave', Decimal('100.00'))
    for _ in range(10):
        service.get_account('ACC004').deposit(Decimal('0.01'))
    dave_balance = service.get_account('ACC004').get_balance()
    print(f"✓ After 10 deposits of $0.01: ${dave_balance}")
    assert dave_balance == Decimal('100.10'), "Decimal precision error!"

    print("\n" + "="*60)
    print("ALL SCENARIOS PASSED!")
    print("="*60)

    print("\nFinal Account Balances:")
    for account_id in ['ACC001', 'ACC002', 'ACC003', 'ACC004']:
        account = service.get_account(account_id)
        print(f"  {account_id} ({account.owner_name}): ${account.get_balance()}")


# Uncomment to run automated tests instead of CLI:
# if __name__ == "__main__":
#     run_test_scenarios()
