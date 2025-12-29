from tracker import init_data, save_data

# Test the data saving functionality
print("Testing data saving...")

# Get current data
data = init_data()
print(f"Current data: {data}")

# Add a test record
test_record = {
    "amount": 200.0,
    "category": "测试",
    "note": "测试记录",
    "payment_method": "微信",
    "time": "2025-12-25 17:30:00"
}
data.append(test_record)
print(f"After adding test record: {data}")

# Save the data
result = save_data(data)
print(f"Save result: {result}")

# Read the data again to verify
new_data = init_data()
print(f"Data after save: {new_data}")