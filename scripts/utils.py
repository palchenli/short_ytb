import pytube
from pytube import YouTube
from urllib import request


def get_video(url, output):
    try:
        YouTube(url).streams.first().download(output)
        return True
    except Exception:
        return False


def get_metadata(video_id, api_key):
    url = "https://www.googleapis.com/youtube/v3/videos?id={}&key={}&part=snippet,contentDetails,statistics,status".format(video_id, api_key)
    res = request.urlopen(url=url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko)"}  # 请求的User-Agent
    req = request.Request(url=url, headers=headers)  # 包装请求对象
    res = request.urlopen(req)  # 发请求
    html = res.read().decode()  # 获取响应内容
    print(html)
    return 0


if __name__ == "__main__":
    # get_video("https://www.youtube.com/shorts/_7tQmQn_qO0", "test.mp4")
    get_metadata("_7tQmQn_qO0", "AIzaSyCFh7zoDAWE26chAQbl3xrB_NkGzqnHUwM")