"""
Exercise 3.3: Abstract Payment Methods

ABSTRACT BASE CLASSES (ABC)

Abstract classes define a contract that all subclasses must implement.
They are blueprints that cannot be instantiated directly.

Key concepts:
1. Use ABC as a base class
2. Mark methods with @abstractmethod decorator
3. Subclasses MUST implement all abstract methods
4. Python enforces this at instantiation time

Why use abstract classes?
- Enforce a consistent interface across related classes
- Catch missing implementations early (at instantiation, not runtime)
- Enable safe polymorphism (guaranteed methods exist)
- Self-documenting code (the abstract class shows the contract)

EXAMPLE:

    from abc import ABC, abstractmethod

    class DataStore(ABC):
        @abstractmethod
        def save(self, key: str, value: str) -> None:
            pass

        @abstractmethod
        def load(self, key: str) -> str:
            pass

    class FileStore(DataStore):
        def save(self, key: str, value: str) -> None:
            # Write to file
            pass

        def load(self, key: str) -> str:
            # Read from file
            pass

    class DatabaseStore(DataStore):
        def save(self, key: str, value: str) -> None:
            # Write to database
            pass

        def load(self, key: str) -> str:
            # Read from database
            pass

    # Polymorphism: same function works with any DataStore
    def backup_data(store: DataStore, data: dict) -> None:
        for key, value in data.items():
            store.save(key, value)

    backup_data(FileStore(), {"user": "alice"})      # Works
    backup_data(DatabaseStore(), {"user": "bob"})    # Works

===================================
EXERCISE: Payment Processing System
===================================

Build a payment processing system with multiple payment methods.
All payment methods share a common interface but have different implementations.

TASK 1: Abstract Base Class

Class: PaymentMethod (inherits from ABC)

Abstract methods:
- process_payment(amount: float) -> bool
    Returns True if payment succeeds, False otherwise

- get_transaction_fee(amount: float) -> float
    Returns the fee charged for processing this amount

These define the CONTRACT. All payment methods must implement them.

---

TASK 2: Concrete Payment Methods

Class: CreditCard
- Attribute: card_number (str) - last 4 digits only
- process_payment(amount):
  * Print "Processing ${amount} via Credit Card ****{card_number}"
  * Return True
- get_transaction_fee(amount):
  * Fee is 2.9% of amount
  * Return amount * 0.029

Class: PayPal
- Attribute: email (str)
- process_payment(amount):
  * Print "Processing ${amount} via PayPal ({email})"
  * Return True
- get_transaction_fee(amount):
  * Fee is 3.5% of amount
  * Return amount * 0.035

Class: BankTransfer
- Attribute: account_number (str) - last 4 digits only
- process_payment(amount):
  * If amount > 10000: print "Large transfer requires manual approval" and return False
  * Otherwise: print "Processing ${amount} via Bank Transfer ****{account_number}" and return True
- get_transaction_fee(amount):
  * Flat $5 fee
  * Return 5.0

---

TASK 3: Polymorphic Function

Function: checkout(payment_method: PaymentMethod, amount: float) -> None

This function:
1. Calculates the fee using get_transaction_fee()
2. Calculates total = amount + fee
3. Prints "Total with fees: ${total:.2f}"
4. Calls process_payment(total)
5. If successful, prints "✓ Payment successful"
6. If failed, prints "✗ Payment failed"

This demonstrates polymorphism - one function works with ANY PaymentMethod.

---

LEARNING OBJECTIVES:

1. Understand abstract classes enforce implementation
2. See how different classes can share the same interface
3. Practice polymorphism with real-world example
4. Learn that you cannot instantiate abstract classes

"""


from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def process_payment(amount: float) -> bool:
        pass

    @abstractmethod
    def get_transaction_fee(amount: float) -> float:
        pass

class CreditCard(PaymentMethod):
    def __init__(self, card_number: str):
        if len(card_number) != 4:
            raise ValueError("last four digits")
        self.card_number = card_number

    def process_payment(self, amount:float):
        print(f"Processing ${amount} via Credit Card ****{self.card_number}")
        return True

    def get_transaction_fee(self, amount):
        fee = 0.029 * amount
        return fee
    
class PayPal(PaymentMethod):
    def __init__(self, email:str):
        self.email = email

    def process_payment(self, amount:float):
        print("Processing ${amount} via PayPal ({email})")
        return True
    
    def get_transaction_fee(self, amount:float):
        return amount * 0.035
    

class BankTransfer(PaymentMethod):
    def __init__(self, account_number:str):
        self.account_number = account_number

    def process_payment(self, amount:float):
        if amount > 10000: 
            print("Large transfer requires manual approval")
            return False
        print("Processing ${amount} via Bank Transfer ****{self.account_number}")
        return True      

    def get_transaction_fee(self, amount:str):
        return 5.0
    
def checkout(payment_method: PaymentMethod, amount: float) -> None:


# ==========================================
# TESTS
# ==========================================

if __name__ == "__main__":
    print("=== Test 1: Cannot instantiate abstract class ===")
    try:
        payment = PaymentMethod()
        print("❌ FAIL: Should not be able to instantiate PaymentMethod")
    except TypeError as e:
        print(f"✓ PASS: {e}")

    print("\n=== Test 2: CreditCard ===")
    cc = CreditCard("1234")
    print(f"Fee for $100: ${cc.get_transaction_fee(100.0):.2f}")  # $2.90
    cc.process_payment(100.0)  # Processing $100.0 via Credit Card ****1234

    print("\n=== Test 3: PayPal ===")
    paypal = PayPal("user@example.com")
    print(f"Fee for $100: ${paypal.get_transaction_fee(100.0):.2f}")  # $3.50
    paypal.process_payment(100.0)  # Processing $100.0 via PayPal (user@example.com)

    print("\n=== Test 4: BankTransfer ===")
    bank = BankTransfer("5678")
    print(f"Fee for $100: ${bank.get_transaction_fee(100.0):.2f}")  # $5.00
    bank.process_payment(100.0)  # Processing $100.0 via Bank Transfer ****5678

    print("\n=== Test 5: BankTransfer - Large amount ===")
    result = bank.process_payment(15000.0)  # Large transfer requires manual approval
    print(f"Success: {result}")  # False

    print("\n=== Test 6: Polymorphism - checkout function ===")

    # Test 6a: CreditCard checkout
    cc_test = CreditCard("1234")
    fee = cc_test.get_transaction_fee(100.0)
    assert fee == 2.90, f"CreditCard fee should be $2.90, got ${fee}"
    print("✓ CreditCard fee calculation correct: $2.90")

    # Test 6b: PayPal checkout
    pp_test = PayPal("user@example.com")
    fee = pp_test.get_transaction_fee(100.0)
    assert fee == 3.50, f"PayPal fee should be $3.50, got ${fee}"
    print("✓ PayPal fee calculation correct: $3.50")

    # Test 6c: BankTransfer checkout (success)
    bt_test = BankTransfer("5678")
    fee = bt_test.get_transaction_fee(100.0)
    assert fee == 5.0, f"BankTransfer fee should be $5.00, got ${fee}"
    print("✓ BankTransfer fee calculation correct: $5.00")

    # Test 6d: BankTransfer large amount (should fail)
    result = bt_test.process_payment(15000.0)
    assert result == False, "BankTransfer should reject large amounts"
    print("✓ BankTransfer correctly rejects large amounts")

    print("\n✓ All fee calculations and validations passed!")

    # print("\n=== Test 7: Type checking ===")
    # payments = [
    #     CreditCard("1111"),
    #     PayPal("test@test.com"),
    #     BankTransfer("2222")
    # ]
    # for p in payments:
    #     print(f"{p.__class__.__name__} is a PaymentMethod: {isinstance(p, PaymentMethod)}")

    # print("\n=== Test 8: Incomplete implementation ===")
    # class IncompletePayment(PaymentMethod):
    #     def process_payment(self, amount: float) -> bool:
    #         return True
    #     # Missing get_transaction_fee()

    # try:
    #     incomplete = IncompletePayment()
    #     print("❌ FAIL: Should not instantiate without all methods")
    # except TypeError as e:
    #     print(f"✓ PASS: {e}")

    # print("\n✓ All tests passed")