import os
import json
import glob
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path


def load_seen_jobs(record_file):
    """加载历史去重记录"""
    if os.path.exists(record_file):
        try:
            with open(record_file, 'r', encoding='utf-8') as f:
                # 读取 JSON 的 List 并转回 Set 的元组
                return set(tuple(item) for item in json.load(f))
        except Exception as e:
            print(f"⚠️ 读取历史记录失败，将重新开始: {e}")
    return set()

def save_seen_jobs(record_file, seen_jobs):
    """保存去重记录到本地"""
    with open(record_file, 'w', encoding='utf-8') as f:
        # 将 Set 转成 List 以便保存为 JSON
        json.dump(list(seen_jobs), f, ensure_ascii=False)

def process_new_data(input_dir, output_file, record_file):
    # 1. 加载历史记录
    seen_jobs = load_seen_jobs(record_file)
    print(f"📂 已加载历史去重记录: {len(seen_jobs)} 条")
    
    # 2. 查找新数据文件（这里假设你每次把新文件放到 input_dir 下）
    json_files = glob.glob(os.path.join(input_dir, "*.json"))
    if not json_files:
        print(f"在 {input_dir} 下没有找到新的 .json 文件！")
        return

    new_added_data = []
    total_read_count = 0

    # 3. 处理新文件
    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    data = [data]
                
                for item in data:
                    total_read_count += 1
                    company = str(item.get("company_name", "")).strip()
                    title = str(item.get("job_title", "")).strip()
                    job_key = (company, title)
                    
                    # 如果不在历史集合中，说明是新数据
                    if job_key not in seen_jobs:
                        seen_jobs.add(job_key) # 加入历史集合
                        
                        # 清洗 "None" 字符串
                        for key, value in item.items():
                            if value == "None" or value == "null":
                                item[key] = None
                                
                        new_added_data.append(item)
        except Exception as e:
            print(f"❌ 解析文件出错 {file_path}: {e}")

    # 4. 将新数据追加到总结果文件
    if new_added_data:
        # 如果输出文件已存在，先读取旧数据再合并，或者直接追加（这里选择合并成合法数组）
        existing_data = []
        if os.path.exists(output_file):
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            except:
                pass
                
        all_data = existing_data + new_added_data
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
            
        print(f"✅ 新增了 {len(new_added_data)} 条数据，已合并保存。")
    else:
        print("💡 没有发现新数据（全部重复或被跳过）。")

    # 5. 更新保存去重记录文件
    save_seen_jobs(record_file, seen_jobs)
    print(f"💾 去重记录已更新，当前共记录 {len(seen_jobs)} 个岗位组合。")
    print(f"📁 原始读取数据数: {total_read_count} 条")

if __name__ == "__main__":
    # ⚠️ 路径配置
    INPUT_DIR = Path(os.getenv("SOURCE_DIR") or "./saved")# 存放【新】json文件的文件夹
    OUTPUT_FILE = Path(os.getenv("OUTPUT_DIR") or "./output") / "all_cleaned_jobs.json" # 最终汇总输出的文件
    RECORD_FILE = OUTPUT_FILE.parent / "seen_jobs_record.json" # 专门用来存储去重集合的文件
    
    if not os.path.exists(INPUT_DIR):
        # 如果目录不存在，自动创建
        os.makedirs(INPUT_DIR)
        print(f"已自动创建文件夹: {INPUT_DIR}，请将新的 JSON 文件放入其中。")
    else:
        process_new_data(INPUT_DIR, OUTPUT_FILE, RECORD_FILE)