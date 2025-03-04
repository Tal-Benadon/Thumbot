from typing import Dict, Any
from exceptions import NoSupportedFormatAvailable

def choose_facebook_format(formats_info: Dict[str, Any]) -> str: 
    chosen_format = None
    
    # filter the formats dict to have no av01 vcodec (not widely supported)
    filtered_formats_info = {
        f: formats_info[f] for f in formats_info if 'av01' not in formats_info[f].get('vcodec')
    }
    
    # pprint.pprint(filtered_formats_info)
    # TODO: Add flag to flip priority to HD
    # we prioritize sd for less bandwith
    try:
        for priority in ["sd", "hd"]:                                
            if priority in filtered_formats_info:
                chosen_format = {
                    'format_id':priority, 
                    'format_url':filtered_formats_info[priority].get('format_url')
                }
                break # will break if sd is found
        
        

        if not chosen_format:
            raise NoSupportedFormatAvailable("avalible format not found")
        
        return chosen_format
    except NoSupportedFormatAvailable as e:
        return{"Error": {"FacebookError": e}}