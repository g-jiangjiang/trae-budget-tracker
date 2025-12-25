from tracker import add_record, list_records, summary, list_records_paginated

def menu():
    print("\n====== 简单记账工具 ======")
    print("1. 添加记录")
    print("2. 查看记录")
    print("3. 查看汇总")
    print("4. 退出")

while True:
    try:
        menu()
        choice = input("请输入选项：").strip()

        if choice == "1":
            try:
                amount_input = input("金额（收入正数，支出负数）：").strip()
                if not amount_input:
                    print("金额不能为空！")
                    continue
                amount = float(amount_input)
                
                category = input("类别（如：餐饮/工资/购物）：").strip()
                if not category:
                    print("类别不能为空！")
                    continue
                    
                payment_method = input("支付方式（如：支付宝/微信/现金，可直接回车）：").strip()
                note = input("备注：").strip()
                
                add_record(amount, category, note, payment_method)
                
            except ValueError as e:
                print(f"输入格式错误：请输入有效的数字金额。错误：{e}")
            except KeyboardInterrupt:
                print("\n操作已取消")
                break
            except Exception as e:
                print(f"添加记录时出错：{e}")

        elif choice == "2":
            try:
                # 获取分页参数
                per_page_input = input("每页数量（默认10，直接回车）：").strip()
                per_page = int(per_page_input) if per_page_input else 10
                if per_page <= 0:
                    print("每页数量必须大于0，已设置为10")
                    per_page = 10
                    
                page_input = input("页码（默认1，直接回车）：").strip()
                page = int(page_input) if page_input else 1
                if page <= 0:
                    print("页码必须大于0，已设置为1")
                    page = 1
                
                # 获取筛选条件
                print("\n=== 筛选条件（直接回车跳过）===")
                filters = {}
                
                amount_min = input("金额最小值：").strip()
                if amount_min:
                    try:
                        filters['amount'] = filters.get('amount', {})
                        filters['amount']['min'] = float(amount_min)
                    except ValueError:
                        print("金额最小值格式错误，已跳过此筛选条件")
                        
                amount_max = input("金额最大值：").strip()
                if amount_max:
                    try:
                        filters['amount'] = filters.get('amount', {})
                        filters['amount']['max'] = float(amount_max)
                    except ValueError:
                        print("金额最大值格式错误，已跳过此筛选条件")
                        
                category = input("类别（包含）：").strip()
                if category:
                    filters['category'] = category
                    
                note = input("备注（包含）：").strip()
                if note:
                    filters['note'] = note
                    
                time_filter = input("时间（包含，如2025-12）：").strip()
                if time_filter:
                    filters['time'] = time_filter
                
                # 获取数据
                result = list_records_paginated(page, per_page, filters if filters else None)
                
                # 显示表头
                print(f"\n{'='*80}")
                print(f"{'时间':<20} {'类别':<12} {'金额':<10} {'支付方式':<10} {'备注':<20}")
                print(f"{'='*80}")
                
                # 显示汇总信息
                summary_data = result['summary']
                print(f"{'[汇总]':<20} {'收入':<12} {summary_data['income']:<10.2f} {'':<10} {'总支出':<10} {summary_data['expense']:<10.2f}")
                print(f"{'':<20} {'余额':<12} {summary_data['balance']:<10.2f} {'':<10} {'':<10}")
                print(f"{'='*80}")
                
                # 显示记录
                records = result['records']
                if not records:
                    print("没有找到符合条件的记录")
                else:
                    for r in records:
                        payment_method = r.get('payment_method', '无')
                        print(f"{r['time']:<20} {r['category']:<12} {r['amount']:<10.2f} {payment_method:<10} {r['note']:<20}")
                
                # 显示分页信息
                pagination = result['pagination']
                print(f"\n当前页：{pagination['current_page']}/{pagination['total_pages']}，总数：{pagination['total_count']}")
                
            except ValueError as e:
                print(f"输入格式错误：{e}")
            except KeyboardInterrupt:
                print("\n操作已取消")
                break
            except Exception as e:
                print(f"查看记录时出错：{e}")

        elif choice == "3":
            try:
                income, expense, balance = summary()
                print("\n===== 汇总 =====")
                print(f"总收入：{income:.2f}")
                print(f"总支出：{expense:.2f}")
                print(f"结余：{balance:.2f}")
            except Exception as e:
                print(f"计算汇总时出错：{e}")

        elif choice == "4":
            print("再见！")
            break

        else:
            print("无效选项，请重试！")
            
    except KeyboardInterrupt:
        print("\n程序已退出")
        break
    except Exception as e:
        print(f"程序运行出错：{e}")
        print("请重试或联系技术支持")
