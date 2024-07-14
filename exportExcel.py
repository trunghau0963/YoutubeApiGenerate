import requests
import pandas as pd


def fetch_youtube_data(api_key, query, max_results):
    api_url = "https://youtube.googleapis.com/youtube/v3/search"
    all_results = []
    params = {
        "key": api_key,
        "part": "snippet",
        "q": query,
        "maxResults": 50,  # Số lượng kết quả tối đa cho mỗi yêu cầu
    }

    try:
        while len(all_results) < max_results:
            response = requests.get(api_url, params=params)
            response.raise_for_status()  # Nếu mã trạng thái không phải 200, sẽ raise một HTTPError
            data = response.json()

            all_results.extend(data.get("items", []))

            # Kiểm tra nếu có nextPageToken để tiếp tục lấy dữ liệu
            if "nextPageToken" in data and len(all_results) < max_results:
                params["pageToken"] = data["nextPageToken"]
            else:
                break

        # Cắt bớt danh sách kết quả nếu nó vượt quá số lượng mong muốn
        if len(all_results) > max_results:
            all_results = all_results[:max_results]

        return all_results
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")


def extract_video_details(items):
    video_details = []
    for item in items:
        if item["id"]["kind"] == "youtube#video":
            video_id = item["id"]["videoId"]
            video_link = f"https://www.youtube.com/watch?v={video_id}"
            video_detail = {
                "channelTitle": item["snippet"]["channelTitle"],
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
                "video_link": video_link,
            }
            video_details.append(video_detail)
    return video_details


def save_to_excel(data, filename):
    try:
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"Data has been successfully saved to {filename}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")


# Sử dụng hàm với API key và từ khóa tìm kiếm cụ thể
api_key = "AIzaSyCCZgrB3dDDtvZMsyYwGikbCT2QyikEkQs"
query = "instrument course"
max_results = 100000
filename = f"{query}.xlsx"

data = fetch_youtube_data(api_key, query, max_results)

if data:
    video_details = extract_video_details(data)
    save_to_excel(video_details, filename)
