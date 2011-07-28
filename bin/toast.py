#!/usr/bin/env python

import os
import toaster.site


if __name__ == '__main__':
    
    # initialize the site
    site = toaster.site.Site()
    
    print 'Building site: %s -> %s' % (site.settings['source'], site.settings['destination'])
    
    # operate on the working directory
    site.process()
    site.render()