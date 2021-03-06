from argparse import ArgumentParser
import codecs
import os

from get_posts import get_all_posts
from utils import *

wp = login()


"""
e.g.

  python ~/dev/wordpress/download_posts.py -d ~/Desktop/writing/publish --post-status publish
  python ~/dev/wordpress/download_posts.py -d ~/Desktop/writing/draft --post-status draft

"""


def download_all_posts(directory, post_status=None, post_type=None):
    directory = os.path.abspath( os.path.expanduser(directory) )

    if not os.path.exists(directory):
        print 'Creating directory: %s' % directory
        os.makedirs(directory)

    posts = get_all_posts(post_status=post_status, post_type=post_type, verbose=False)
    for post in posts:
        if not post.title:
            # actually, Wordpress allows posts without
            # titles. so add a pdb and look at the content
            # to figure out what it is
            raise UnknownError("This post does not have a title")
        title = post.title[:-1] if post.title[-1] == '.' else post.title # remove trailing '.'
        filen = os.path.join(directory, title + '.txt')
        # print 'Writing %s' % filen
        try:
            codecs.open(filen, 'w', 'utf-8').write(post.content)
        except:
            print 'Error: %s' % title


if __name__ == "__main__":
    
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('-d', '--directory',
                        type=str,
                        default='posts',
                        help='The directory to fill with text files of your posts - defaults to "./posts"'
                        )
    parser.add_argument('--post-status',
                        type=str,
                        default=None,
                        help='If specified, will filter to POST_STATUS, otherwise doesn\'t filter by POST_STATUS'
                        )
    parser.add_argument('--post-type',
                        type=str,
                        default='post',
                        help='By default, grabs Posts. Set to "page" for Pages'
                        )
    args = vars(parser.parse_args())
    
    download_all_posts(directory=args['directory'],
                       post_status=args['post_status'],
                       post_type=args['post_type'])


