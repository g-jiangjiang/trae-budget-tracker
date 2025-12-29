import json
from datetime import datetime

DATA_FILE = "data.json"

# 初始化数据文件
def init_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # 验证数据格式
            if not isinstance(data, list):
                print("数据文件格式错误，重新创建")
                return []
            return data
    except FileNotFoundError:
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)
            return []
        except Exception as e:
            print(f"创建数据文件失败：{e}")
            return []
    except json.JSONDecodeError as e:
        print(f"数据文件损坏：{e}，重新创建")
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)
            return []
        except Exception as e2:
            print(f"重新创建数据文件失败：{e2}")
            return []
    except Exception as e:
        print(f"读取数据文件失败：{e}")
        return []

# 保存数据
def save_data(records):
    try:
        # 验证数据格式
        if not isinstance(records, list):
            raise ValueError("记录必须是列表格式")
        
        # 验证每条记录的格式
        for record in records:
            if not isinstance(record, dict):
                raise ValueError("每条记录必须是字典格式")
            required_fields = ['amount', 'category', 'time']
            for field in required_fields:
                if field not in record:
                    raise ValueError(f"记录缺少必要字段：{field}")
        
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存数据失败：{e}")
        return False

# 添加记录（带支付方式和确认）
def add_record(amount, category, note="", payment_method=""):
    records = init_data()
    new_record = {
        "amount": amount,
        "category": category,
        "note": note,
        "payment_method": payment_method,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 先显示要添加的记录
    print(f"\n即将添加记录：")
    print(f"时间：{new_record['time']}")
    print(f"类别：{new_record['category']}")
    print(f"金额：{new_record['amount']}")
    print(f"支付方式：{new_record['payment_method']}")
    print(f"备注：{new_record['note']}")
    
    # 确认是否添加
    confirm = input("\n确认添加此记录？(回车确认，输入y撤回): ").strip().lower()
    if confirm == 'y':
        print("记录已撤回，未添加。")
        return False
    else:
        records.append(new_record)
        if save_data(records):
            print("记录已添加！")
            return True
        else:
            print("记录添加失败，数据保存出错")
            return False

# 读取记录
def list_records():
    return init_data()

# 统计汇总
def summary():
    try:
        records = init_data()
        if not records:
            return 0.0, 0.0, 0.0
        
        # 验证数据完整性
        income = 0.0
        expense = 0.0
        
        for record in records:
            if not isinstance(record, dict):
                continue
            if 'amount' not in record or not isinstance(record['amount'], (int, float)):
                continue
                
            amount = record['amount']
            if amount > 0:
                income += amount
            elif amount < 0:
                expense += -amount
        
        balance = income - expense
        return income, expense, balance
    
    except Exception as e:
        print(f"计算汇总时出错：{e}")
        return 0.0, 0.0, 0.0

# 带分页和筛选的查看记录
def list_records_paginated(page=1, per_page=10, filters=None):
    records = init_data()
    
    # 应用筛选条件
    if filters:
        filtered_records = []
        for record in records:
            match = True
            for field, condition in filters.items():
                if field in record:
                    if isinstance(condition, dict):
                        # 范围筛选
                        if 'min' in condition and record[field] < condition['min']:
                            match = False
                            break
                        if 'max' in condition and record[field] > condition['max']:
                            match = False
                            break
                    elif isinstance(condition, str) and condition not in str(record[field]):
                        # 字符串包含筛选
                        match = False
                        break
                    elif isinstance(condition, (int, float)) and record[field] != condition:
                        # 精确值筛选
                        match = False
                        break
            if match:
                filtered_records.append(record)
        records = filtered_records
    
    # 计算汇总信息
    income = sum(r["amount"] for r in records if r["amount"] > 0)
    expense = sum(-r["amount"] for r in records if r["amount"] < 0)
    balance = income - expense
    
    # 分页
    total_count = len(records)
    total_pages = (total_count + per_page - 1) // per_page
    
    if page < 1:
        page = 1
    if page > total_pages and total_pages > 0:
        page = total_pages
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_records = records[start_idx:end_idx]
    
    return {
        'records': paginated_records,
        'summary': {'income': income, 'expense': expense, 'balance': balance},
        'pagination': {
            'current_page': page,
            'total_pages': total_pages,
            'total_count': total_count,
            'per_page': per_page
        }
    }
