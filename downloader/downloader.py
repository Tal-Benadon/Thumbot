import yt_dlp
import requests
import os
from exceptions import  MissingContentLengthError, FileTooLargeError, InitialLinkFormatError, InstagramError, FacebookError, RedditError
from typing import Any, Dict
from .providers_formats_processors.dispatch_table import dispatch_table

video_dir = './video_temp_dir'

# Extracts the initial metadata without downloading the video
def extract_metadata_info(url: str) -> Dict[str, Any]:
    yt_opt = {}
    try:
        with yt_dlp.YoutubeDL(yt_opt) as ydl:
            video_info_dict = ydl.extract_info(url, download=False)
            if video_info_dict is None and "instagram" in url:
                raise InstagramError("Instagram didnt provide us with information (rate limit might have reached)")
            else:
                return video_info_dict
        
    
    
    except yt_dlp.utils.DownloadError as e:
        return {"Error": {"yt_dlp":e}}



# Checks for the different formats and sizes existing in the given metadata
def metadata_formats_info(info_dict):
        formats_info = {}
        if 'formats' in info_dict:
            for format in info_dict['formats']:
                
                format_id = format.get('format_id')
                if not format_id:
                    continue
                
                format_ext = format.get('ext', 'Unknown extension')
                format_note = format.get('format_note', 'Unknown note')
                format_url = format.get('url', None)
                vcodec = format.get('vcodec', '')
                filesize = format.get('filesize', None)
                filesize_approx = format.get('filesize_approx', None) 
                resolution = format.get('resolution', '')
                
                
                # size readablity
                if filesize is not None:
                    filesize = round(int(filesize) / (1024 * 1024),2)
                if filesize_approx is not None:
                    filesize_approx = round(int(filesize_approx) / (1024 * 1024),2)
                    
                formats_info[format_id] = {
                    'format_ext': format_ext,
                    'format_note':format_note,
                    'format_url':format_url,
                    'vcodec': vcodec,
                    'filesize': filesize,
                    'filesize_approx':filesize_approx,
                    'resolution': resolution
                }
        return formats_info
   

# TODO : Discord supports only around 8MB of file uploads for bots. Could be enhanced up to 50MB if a server is boosted to level 2            
def check_video_size(video_url: str, max_size=8_388_608)-> int:
    
    # Head request to determine actual video size **** Heads Up **** -> some providers' links does not provide real number within content-length
    response = requests.head(video_url, allow_redirects=True)
    content_length = response.headers.get('content-length')
    
    # Checks if size exists or exceeds the max size limits
    if not content_length:
        raise MissingContentLengthError("Content length not found in response headers.")
    
    content_length = int(content_length)
    
    if content_length >= max_size:
        raise FileTooLargeError(f"File size [{content_length} bytes] ({round(content_length / (1024 * 1024),2)}MB) exceeds the limit of [{max_size}] bytes ({max_size / (1024 * 1024)}MB)")
    
    return content_length
    

def download_video(url: str, format_id: str) -> str:
    video_path_template = os.path.join(video_dir,'%(title)s.%(ext)s')
    
    ydl_opts: Dict[str, Any] = {
         'format': format_id,
        'outtmpl': video_path_template,
        
        }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info_dict)

    except Exception as e:
        print(f"Download Error{e}")


def choose_provider(initial_link, format_info):
    try:
        for key, func in dispatch_table.items():
            if key in initial_link:
                return func(format_info)
        
        raise InitialLinkFormatError(f"Error: Unsupported link provider in URL [{initial_link}]")
    except InitialLinkFormatError as e:
        return {"Error": {"providerLinkError": e}}
                

def proccess_video_request(url: str):
    try:
        info_dict = extract_metadata_info(url)
        formats_info = metadata_formats_info(info_dict)
        print(formats_info)
        chosen_format = choose_provider(url, formats_info)
        
        format_url = chosen_format.get('format_url')
        format_id = chosen_format.get('format_id')
        
        video_size = check_video_size(format_url) 
        
        if video_size >= 8_388_608: # TODO: should be an env variable
            return None
            
        return download_video(url, format_id)
     
        

    except FacebookError as e:
        return{"Error": f"Facebook Error -> {e}"}
    
    except InstagramError as e:
        return{"Error": f"Instagram Error -> {e}"}
    
    except RedditError as e:
        return{"Error": f"Reddit Error -> {e}"}
    
    except Exception as e:
        return {"Error" : f"Unexpected error occured -> {e}"}