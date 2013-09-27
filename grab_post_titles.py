from utils import *

"""
python grab_post_titles.py

OR

posts = get_all_posts(verbose=True)
print posts[0].content

(Pdb) dir(post)
[... 'comment_status', 'content', 'custom_fields', 'date', 'date_modified', 'definition', 'excerpt', 'guid', 'id', 'link', 'menu_order', 'mime_type', 'parent_id', 'password', 'ping_status', 'post_format', 'post_status', 'post_type', 'slug', 'sticky', 'struct', 'terms', 'thumbnail', 'title', 'user']
"""

wp = login()

def get_all_posts(verbose=False, post_status=None, increment=50):
    posts = []
    offset = 0
    while True:
        print '%i-%i' % (offset, offset+increment)
        latest = get_some_posts(post_status=post_status, offset=offset, increment=increment)
        if len(latest):
            posts += latest
        else:
            break  # no more posts returned
        offset = offset + increment
    print
    return posts

def get_some_posts(offset=0, increment=20, post_status='publish'):
    d = {'number': increment,
         'offset': offset}
    if post_status is not None:
        d['post_status'] = post_status
    return wp.call(GetPosts(d))


if __name__ == "__main__":
    posts = get_all_posts(verbose=True)
    # posts = get_some_posts()
    
    print '\n'.join(['%s %s' % (post.id, post.title[:20])
                     for post in posts])
    

