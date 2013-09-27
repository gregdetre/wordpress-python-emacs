from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost, EditPost
from wordpress_xmlrpc.methods.users import GetUserInfo

def login():
    site, username, passwd = open('.password').read().split()
    full_site = 'http://%s/xmlrpc.php' % site
    wp = Client(full_site, username, passwd)
    return wp

