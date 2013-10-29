from argparse import ArgumentParser

from utils import *

"""
Gets Posts (default) or Pages as python objects.
"""

# python get_posts.py
#
# OR
#
# posts = get_all_posts(verbose=True)
# print posts[0].content
#
# (Pdb) dir(posts[0])
# [... 'comment_status', 'content', 'custom_fields', 'date', 'date_modified', 'definition', 'excerpt', 'guid', 'id', 'link', 'menu_order', 'mime_type', 'parent_id', 'password', 'ping_status', 'post_format', 'post_status', 'post_type', 'slug', 'sticky', 'struct', 'terms', 'thumbnail', 'title', 'user']


wp = login()

def get_all_posts(verbose=False, increment=50, post_status=None, post_type=None):
    posts = []
    offset = 0
    while True:
        print '%i-%i' % (offset, offset+increment)
        latest = get_some_posts(offset=offset, increment=increment,
                                post_status=post_status, post_type=post_type)
        if len(latest):
            posts += latest
        else:
            break  # no more posts returned
        offset = offset + increment
    print
    return posts


def get_some_posts(offset=0, increment=20,
                   post_status='publish',
                   post_type='post'):
    if post_type is None:
        post_type = 'post'
    d = {'number': increment,
         'offset': offset,
         'post_type': post_type,}
    if post_status is not None:
        d['post_status'] = post_status
    if post_type == 'post':
        results_class = WordPressPost
    elif post_type == 'page':
        results_class = WordPressPage
    else:
        raise Exception('Unknown POST_TYPE %s' % post_type)
    items = wp.call(GetPosts(d, results_class=results_class))
    for item in items:
        if not item.title:
            item.title = '(no title)'
    # if you want the parent category Page's id, see
    # item.parent_id - though you would then have to look
    # up the title for that id
    return items


if __name__ == "__main__":

    parser = ArgumentParser(description=__doc__)
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

    items = get_all_posts(verbose=True,
                          post_status=args['post_status'],
                          post_type=args['post_type']
                          )
    
    print '\n'.join(['%s %s' % (item.id, item.title[:20])
                     for item in items])
    

