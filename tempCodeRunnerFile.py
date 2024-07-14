import requests

def fetch_youtube_data(api_key, query):
    # Cấu trúc URL của API với query được cung cấp
    api_url = f"https://youtube.googleapis.com/youtube/v3/search?key={api_key}&part=snippet&q={query}"
    
    try:
        # Gửi yêu cầu GET tới API
        response = requests.get(api_url)
        
        # Kiểm tra mã trạng thái của phản hồi
        response.raise_for_status()  # Nếu mã trạng thái không phải 200, sẽ raise một HTTPError
        
        # Chuyển phản hồi JSON thành từ điển Python
        data = response.json()
        
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

# Sử dụng hàm với API key và từ khóa tìm kiếm cụ thể
api_key = "AIzaSyBktsN_5uWqGzOEhb3G63bd-RR3ASudAJY"
query = "youtube api"
data = fetch_youtube_data(api_key, query)

# In dữ liệu nhận được từ API
if data:
    print(data)
