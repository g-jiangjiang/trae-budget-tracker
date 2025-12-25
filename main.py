from tracker import add_record, list_records, summary, save_data

def menu():
    print("\n====== 简单记账工具 ======")
    print("1. 添加记录")
    print("2. 查看记录")
    print("3. 查看汇总")
    print("4. 退出")

while True:
    try:
        menu()
        choice = input("请输入选项：")

        if choice == "1":
            try:
                amount = float(input("金额（收入正数，支出负数）："))
                category = input("类别（如：餐饮/工资/购物）：")
                payment_method = input("支付方式（如：支付宝/微信/现金）：")
                note = input("备注：")
                add_record(amount, category, payment_method, note)
            
                # 二次确认
                records = list_records()
                new_record = records[-1]
                print("\n===== 新添加的记录 =====")
                print(f"时间：{new_record['time']}")
                print(f"类别：{new_record['category']}")
                print(f"支付方式：{new_record['payment_method']}")
                print(f"金额：{new_record['amount']}")
                print(f"备注：{new_record['note']}")
                
                confirm = input("\n是否撤回操作？(回y撤回，否则保留): ")
                if confirm.lower() == 'y':
                    records.pop()
                    save_data(records)
                    print("操作已撤回！")
                else:
                    print("记录已添加！")
            except ValueError:
                print("错误：金额必须是数字！")

        elif choice == "2":
            try:
                records = list_records()
                
                # 筛选功能
                filtered_records = records.copy()
                
                # 先询问是否筛选
                filter_choice = input("是否需要筛选记录？(是/否)：")
                if filter_choice.lower() in ['是', 'y', 'yes']:
                    # 时间范围筛选
                    start_time = input("开始时间（YYYY-MM-DD，留空跳过）：")
                    end_time = input("结束时间（YYYY-MM-DD，留空跳过）：")
                    
                    if start_time:
                        filtered_records = [r for r in filtered_records if r['time'] >= start_time]
                    if end_time:
                        filtered_records = [r for r in filtered_records if r['time'] <= end_time + " 23:59:59"]
                    
                    # 类别筛选
                    category_filter = input("类别筛选（留空跳过）：")
                    if category_filter:
                        filtered_records = [r for r in filtered_records if category_filter in r['category']]
                    
                    # 支付方式筛选
                    payment_filter = input("支付方式筛选（留空跳过）：")
                    if payment_filter:
                        filtered_records = [r for r in filtered_records if 'payment_method' in r and payment_filter in r['payment_method']]
                    
                    # 金额范围筛选
                    min_amount = input("最小金额（留空跳过）：")
                    max_amount = input("最大金额（留空跳过）：")
                    
                    if min_amount:
                        filtered_records = [r for r in filtered_records if r['amount'] >= float(min_amount)]
                    if max_amount:
                        filtered_records = [r for r in filtered_records if r['amount'] <= float(max_amount)]
                    
                    # 备注筛选
                    note_filter = input("备注筛选（留空跳过）：")
                    if note_filter:
                        filtered_records = [r for r in filtered_records if note_filter in r['note']]
                
                if not filtered_records:
                    print("\n没有找到符合条件的记录！")
                    continue
                
                # 分页功能
                page_size = input("每页数量（默认10）：")
                page_size = int(page_size) if page_size.strip() else 10
                page_num = input("页码（默认1）：")
                page_num = int(page_num) if page_num.strip() else 1
                
                total_records = len(filtered_records)
                total_pages = (total_records + page_size - 1) // page_size
                
                # 分页边界校验
                if page_size <= 0:
                    print("\n错误：每页数量必须大于0！")
                    continue
                if page_num < 1 or page_num > total_pages:
                    print(f"\n错误：页码必须在1到{total_pages}之间！")
                    continue
                
                start_idx = (page_num - 1) * page_size
                end_idx = min(start_idx + page_size, total_records)
                page_records = filtered_records[start_idx:end_idx]
                
                # 汇总信息
                income = sum(r["amount"] for r in filtered_records if r["amount"] > 0)
                expense = sum(-r["amount"] for r in filtered_records if r["amount"] < 0)
                balance = income - expense
                
                print("\n===== 记录汇总 =====")
                print(f"总收入：{income:.2f}")
                print(f"总支出：{expense:.2f}")
                print(f"结余：{balance:.2f}")
                print(f"\n当前页/总页数：{page_num}/{total_pages}，总数：{total_records}")
                
                # 表头
                print(f"{'时间':<20} | {'类别':<10} | {'支付方式':<10} | {'金额':<10} | {'备注':<20}")
                print("-" * 80)
                
                # 数据行
                for r in page_records:
                    payment_method = r.get('payment_method', '未知')
                    amount_str = f"+{r['amount']:.2f}" if r['amount'] > 0 else f"{r['amount']:.2f}"
                    print(f"{r['time']:<20} | {r['category']:<10} | {payment_method:<10} | {amount_str:<10} | {r['note']:<20}")
                    
            except ValueError as e:
                print(f"错误：{e}")

        elif choice == "3":
            income, expense, balance = summary()
            print("\n===== 汇总 =====")
            print("总收入：", income)
            print("总支出：", expense)
            print("结余：", balance)

        elif choice == "4":
            print("再见！")
            break

        else:
            print("无效选项，请重试！")
    except ValueError as e:
        print(f"输入错误：{str(e)}")
    except IndexError as e:
        print(f"索引错误：{str(e)}")
    except Exception as e:
        print(f"发生错误：{str(e)}")
