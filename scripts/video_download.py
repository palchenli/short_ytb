import pytube
from pytube import YouTube


def download_youtube(url, output):
    """Download YouTube videos.

    Args:
        url (str): YouTube video url.
        output (str): Download directory.

    Returns:
        bool: Return True if the video was downloaded and False if get an exception.

    """
    try:
        YouTube(url).streams.first().download(output)
        return True
    except Exception:
        return False


if __name__ == "__main__":
    download_youtube("https://www.youtube.com/shorts/_7tQmQn_qO0", "test.mp4")