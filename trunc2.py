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

def process_excel_file(input_filename, output_filename):
    # Đọc file Excel
    df = pd.read_excel(input_filename)
    
    # Truncate 'title' column to 120 characters
    df['Subtitle'] = df['Subtitle'].apply(lambda x: truncate_or_pad_string(x, 120) if pd.notnull(x) else x)
    
    # Ensure 'description' column is at least 256 characters
    df['description'] = df['description'].apply(lambda x: truncate_or_pad_string(x, float('inf'), 256) if pd.notnull(x) else x)
    
    # Lưu lại file Excel đã được xử lý
    df.to_excel(output_filename, index=False)
    print(f"Data has been successfully processed and saved to {output_filename}")

# Sử dụng hàm với file Excel đầu vào và đầu ra
input_filename = "trunc.xlsx"
output_filename = "processed_youtube_video_details.xlsx"

process_excel_file(input_filename, output_filename)
