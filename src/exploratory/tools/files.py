import os
import re


def get_files(rootdir : str, extension : str):

    # Initialize list to return
    filepaths = list()
    
    # Recursively search the rootpath directory
    for dirpath, _, fpaths in os.walk(rootdir):
        
        # Iterate over each filename
        for fpath in fpaths:
            
            # Continue if file extension is not desired
            curr_ext = os.path.splitext(fpath)[1]
            if re.search("\.{}$".format(extension), curr_ext) is None: continue
            
            # Add the complete filepath to the list to return
            filepath = os.path.join(dirpath, fpath)
            filepaths.append(str(filepath))

    return filepaths


def get_sources(src_rootdir : str):

    # Initialize list to return
    filepaths = list()
    
    # Recursively search the rootpath directory
    for dirpath, _, fpaths in os.walk(src_rootdir):
        
        # Iterate over each filename
        for fpath in fpaths:
            
            # Continue if file extension is not fortran
            extension = os.path.splitext(fpath)[1]
            if re.search("\.[fF][0-9]*$", extension) is None: continue
            
            # Add the complete filepath to the list to return
            filepath = os.path.join(dirpath, fpath)
            filepaths.append(str(filepath))

    return filepaths