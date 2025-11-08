from django.utils.text import slugify

def make_slug(name):
    return slugify(name)
        

        