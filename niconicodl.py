import os
import re
import signal
import platform
from yt_dlp import YoutubeDL
from datetime import datetime
import subprocess

class KeyboardInterruptError(Exception):
    pass

def handle_keyboard_interrupt(signum, frame):
    raise KeyboardInterruptError()

def is_valid_niconico_url(url):
    pattern = r'https?://(?:www\.|)nicovideo\.jp/watch/(?:sm|nm|so|)(?:\d+)'
    return re.match(pattern, url) is not None

def set_file_times(filepath):
    current_time = datetime.now().timestamp()
    os.utime(filepath, (current_time, current_time))
    
    if platform.system() == "Windows":
        import ctypes
        from ctypes import wintypes
        kernel32 = ctypes.windll.kernel32
        SetFileTime = kernel32.SetFileTime
        SetFileTime.argtypes = [wintypes.HANDLE, wintypes.LPFILETIME, wintypes.LPFILETIME, wintypes.LPFILETIME]
        SetFileTime.restype = wintypes.BOOL
        file_handle = ctypes.windll.kernel32.CreateFileW(filepath, 0x100000, 0, None, 3, 0x80, None)
        if file_handle != -1:
            file_time = int(current_time * 10000000 + 116444736000000000)
            creation_time = wintypes.FILETIME(file_time & 0xFFFFFFFF, file_time >> 32)
            SetFileTime(file_handle, ctypes.byref(creation_time), None, None)
            ctypes.windll.kernel32.CloseHandle(file_handle)

def download_best_quality_video(url, output_dir):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s')
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)
            print(f"Successfully downloaded best quality video from {url}")
            set_file_times(file_name)
            return file_name
        except Exception as e:
            print(f"An error occurred while downloading the content: {str(e)}")
            return None

def reencode_video(input_file, resolution):
    output_file = f"{os.path.splitext(input_file)[0]}_{resolution}.mp4"
    ffmpeg_command = ['ffmpeg', '-i', input_file, '-vf', f'scale=-2:{resolution}', '-c:a', 'copy', output_file]
    try:
        print(f"Re-encoding to {resolution}p...")
        subprocess.run(ffmpeg_command, check=True)
        print(f"Successfully re-encoded the video to {resolution}p.")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during re-encoding: {e}")
        return None

def get_default_download_folder():
    if platform.system() == "Windows":
        return os.path.join(os.path.expanduser("~"), "Downloads")
    else:
        return os.getcwd()

def main():
    try:
        print("Welcome to the Niconico Downloader!")
        print("Made by https://github.com/theoneandonlyprincesstrunks")
        print("This script will automatically download the highest quality available for your chosen option.")
        print("Press Ctrl+X at any time to cancel the current operation and return to the main menu.")
        
        signal.signal(signal.SIGINT, handle_keyboard_interrupt)
        
        main.output_dir = get_default_download_folder()
        print(f"Default output directory: {main.output_dir}")
        
        while True:
            print("\nPlease choose an option:")
            print("1. Download content")
            print("2. Set output directory")
            print("3. Exit")
            
            choice = input("Enter your choice (1-3): ")
            
            if choice == '1':
                url = input("Enter the Niconico video URL: ")
                if not is_valid_niconico_url(url):
                    print("Invalid Niconico URL. Please provide a valid URL.")
                    continue
                
                downloaded_file = download_best_quality_video(url, main.output_dir)
                if downloaded_file:
                    print("\nChoose a resolution to re-encode the video:")
                    print("1. 1080p")
                    print("2. 720p")
                    print("3. 480p")
                    
                    resolution_choice = input("Enter the resolution (1-3): ").strip()
                    resolution_map = {'1': '1080', '2': '720', '3': '480'}
                    
                    if resolution_choice in resolution_map:
                        selected_resolution = resolution_map[resolution_choice]
                        reencode_video(downloaded_file, selected_resolution)
                    else:
                        print("Invalid resolution choice.")
            
            elif choice == '2':
                new_dir = input("Enter the new output directory path: ")
                if os.path.isdir(new_dir):
                    main.output_dir = new_dir
                    print(f"Output directory set to: {new_dir}")
                else:
                    print("Invalid directory path. Please try again.")
            
            elif choice == '3':
                print("Thank you for using Niconico Downloader. Goodbye!")
                break
            
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
