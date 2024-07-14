import pandas as pd
import random
import string

def truncate_or_pad_string(text, max_length, min_length=None):
    if min_length and len(text) < min_length:
        # Thêm ký tự ngẫu nhiên nếu chuỗi ngắn hơn min_length
        text += ''.join(random.choices(string.ascii_letters + string.digits, k=min_length - len(text)))
    if len(text) > max_length:
        return text[:max_length]
    return text

def add_row_number(text, row_number):
    return f"{row_number}{text}"

def process_excel_file(input_filename, output_filename):
    # Đọc file Excel
    df = pd.read_excel(input_filename)
    
    # Truncate 'title' column to 120 characters
    df['Title'] = df['Title'].apply(lambda x: truncate_or_pad_string(x, 120) if pd.notnull(x) else x)
    
    # Ensure 'description' column is at least 256 characters
    df['description'] = df['description'].apply(lambda x: truncate_or_pad_string(x, float('inf'), 256) if pd.notnull(x) else x)
    
    # Add row number to 'Title' column
    df['Title'] = df.apply(lambda x: add_row_number(x['Title'], x.name + 1) if pd.notnull(x['Title']) else x['Title'], axis=1)
    
    # Lưu lại file Excel đã được xử lý
    df.to_excel(output_filename, index=False)
    print(f"Data has been successfully processed and saved to {output_filename}")

# Sử dụng hàm với file Excel đầu vào và đầu ra
input_filename = "trunc.xlsx"
output_filename = "trunc2.xlsx"

process_excel_file(input_filename, output_filename)
