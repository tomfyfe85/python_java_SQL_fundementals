print("\nTesting filter_and_convert_inventory():")
print(f"Changes [1, -2, 3, -4, 5] → {filter_and_convert_inventory([1, -2, 3, -4, 5])}")  # Should be [2, 6, 10]
print(f"Changes [-1, -2, -3] → {filter_and_convert_inventory([-1, -2, -3])}")  # Should be []
print(f"Changes [10, 20, 30] → {filter_and_convert_inventory([10, 20, 30])}")  # Should be [20, 40, 60]