#!/usr/bin/env python

import os, toaster


if __name__ == '__main__':
    
    # initialize the toaster instance
    toast = toaster.Toaster()
    
    # load the config file values
    toast.load_config(os.path.relpath('_config.yml'))
    
    # operate on the input directory
    toast.toast_directory(toast.settings['source'])