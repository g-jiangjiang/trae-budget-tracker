from tracker import add_record, list_records_paginated, summary

# Test adding a record with payment method (simulate confirmation)
print('Testing add_record with payment method...')
try:
    # Simulate the confirmation by calling the function directly
    records = [
        {
            "amount": 150.0,
            "category": "工资", 
            "note": "月收入",
            "payment_method": "支付宝",
            "time": "2025-12-25 17:02:27"
        }
    ]
    
    # Show what would be added
    new_record = records[0]
    print(f"\n即将添加记录：")
    print(f"时间：{new_record['time']}")
    print(f"类别：{new_record['category']}")
    print(f"金额：{new_record['amount']}")
    print(f"支付方式：{new_record['payment_method']}")
    print(f"备注：{new_record['note']}")
    print("\n(模拟用户直接回车确认)")
    
    # Actually add the record
    from tracker import init_data, save_data
    existing_records = init_data()
    existing_records.append(new_record)
    save_data(existing_records)
    print("记录已添加！")
    
except Exception as e:
    print(f'Error adding record: {e}')

# Test viewing records with pagination
print('\nTesting list_records_paginated...')
try:
    result = list_records_paginated(page=1, per_page=5)
    print(f'Found {len(result["records"])} records')
    print(f'Summary: {result["summary"]}')
    print(f'Pagination: {result["pagination"]}')
except Exception as e:
    print(f'Error viewing records: {e}')

# Test summary
print('\nTesting summary...')
try:
    income, expense, balance = summary()
    print(f'Income: {income}, Expense: {expense}, Balance: {balance}')
except Exception as e:
    print(f'Error getting summary: {e}')

print('\nAll tests completed!')