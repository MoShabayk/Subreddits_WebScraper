import os
import requests
import urllib.parse
import re


def sanitize_filename(filename):
    # Remove invalid characters from the filename
    sanitized_filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    return sanitized_filename


def download_image(url, folder_path, filename):
    response = requests.get(url)
    if response.status_code == 200:
        parsed_url = urllib.parse.urlparse(url)
        path = parsed_url.path
        extension = os.path.splitext(path)[1]
        if extension:
            sanitized_filename = sanitize_filename(filename)
            file_name = f"{sanitized_filename}{extension}"
            os.makedirs(folder_path, exist_ok=True)
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {file_name}")
        else:
            print(f"Failed to determine file extension for: {filename}")
    else:
        print(f"Failed to download: {filename}")


def scrape_subreddit(subreddit_name, download_folder):
    url = f"https://www.reddit.com/r/{subreddit_name}.json"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code == 200:
        data = response.json()
        if "data" in data and "children" in data["data"]:
            posts = data["data"]["children"]

            for post in posts:
                post_data = post["data"]
                post_title = post_data["title"]
                post_date = post_data["created_utc"]
                image_url = post_data["url"]

                # Create a folder with the subreddit name if it doesn't exist
                subreddit_folder = os.path.join(download_folder, subreddit_name)
                os.makedirs(subreddit_folder, exist_ok=True)

                # Format the filename as "title_date.extension"
                extension = image_url.split('.')[-1]
                filename = f"{post_title}_{post_date}.{extension}"

                download_image(image_url, subreddit_folder, filename)
        else:
            print("Failed to retrieve subreddit data.")
    else:
        print("Failed to retrieve subreddit data.")


def main():
    subreddit_name = input("Enter the subreddit name: ")
    download_folder = input("Enter the path to the download folder: ")

    scrape_subreddit(subreddit_name, download_folder)


if __name__ == '__main__':
    main()
