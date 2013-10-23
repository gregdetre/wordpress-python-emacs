from argparse import ArgumentParser
import os
import pprint
import sys

from grab_post_titles import get_all_posts
from utils import *

"""
Feed in a text file to create/update a Wordpress post.

Wordpress login credentials specified by the .password file read by utils.login().

Uses grab_post_titles.get_all_posts() to check for an
existing post with the same title (case-insensitive,
includes both draft + published). If one exists, it updates
it based on the filename and contents, otherwise it creates
a new post.

e.g.

  python create_update_post '../posts/foo bar.txt' -> 'foo bar'

see http://python-wordpress-xmlrpc.readthedocs.org/en/latest/examples/posts.html
"""


def create_update_post(filen, post_status=None):
    # remove the extension from the filename to get the title,
    # e.g. '/yadda/foo bar.txt' -> 'foo bar'
    title = os.path.basename(os.path.splitext(filen)[0])

    posts = get_all_posts()
    existing_post = check_if_title_exists(posts, title)

    if existing_post:
        post = update_post(existing_post, filen, title=title, post_status=post_status, verbose=True)
    else:
        post = create_post(filen, title, post_status=post_status, verbose=True)
    created = not existing_post
    return post, created
    

def check_if_title_exists(posts, title):
    existing_post = [post for post in posts
                     if post.title.lower() == title.lower()]
    if existing_post:
        assert len(existing_post) == 1
        return existing_post[0]
    

def display_post(post, msg, filen):
    print msg
    print pprint.pformat({'filename': filen,
                          'title': post.title,
                          'content': post.content[:20] + '...',
                          'post_status': post.post_status,
                          })

def create_post(filen, title, post_status=None, verbose=False):
    content = open(filen, 'r').read()
    post = WordPressPost()
    post.title = title
    post.content = content
    post.post_status = post_status or 'draft'
    # post.terms_names = {
    #   'post_tag': ['test', 'firstpost'],
    #   'category': ['Introductions', 'Tests']
    # }
    if verbose: display_post(post, 'Creating', filen)
    wp.call(NewPost(post))
    return post
    

def update_post(post, filen, title=None, post_status=None, verbose=False):
    """
    If POST_STATUS is None, does not alter the POST_STATUS,
    so if it was draft before, it'll still be draft now.
    """
    old_content = post.content
    new_content = open(filen, 'r').read()
    old_title = post.title
    new_title = title or old_title
    post.title = new_title
    post.content = new_content
    if post_status is not None: post.post_status = post_status
    if verbose: display_post(post, 'Updating', filen)
    wp.call(EditPost(post.id, post))
    # raise NotImplementedError
    return post


wp = login()

if __name__ == "__main__":
    
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('-f', '--filename',
                        type=str,
                        required=True,
                        help='The filename to use as the basis of the post'
                        )
    parser.add_argument('--post-status',
                        type=str,
                        default=None,
                        help='If specified, will set POST_STATUS, otherwise will leave as is'
                        )
    args = vars(parser.parse_args())
    
    assert os.path.exists(args['filename'])

    post, created = create_update_post(filen=args['filename'],
                                       post_status=args['post_status'])


