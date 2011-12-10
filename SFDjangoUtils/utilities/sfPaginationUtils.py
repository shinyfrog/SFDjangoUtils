'''
    Shiny frog pagination utilities
'''

try:
    from settings import PAGELINKS_LEFT, PAGELINKS_RIGHT
except:
    PAGELINKS_LEFT = 5
    PAGELINKS_RIGHT = 5

def getPaginationData(paginator, page, request, links_left=PAGELINKS_LEFT, links_right=PAGELINKS_RIGHT):

    rangeleft  = 0
    rangeright = 0
    totlinks   = links_left + links_right + 1

    if page - links_left < 1:
        rangeleft = 1
    else:
        rangeleft = page - links_left

    rangeright = rangeleft + (totlinks)

    if rangeright > paginator.num_pages:
       rangeright = paginator.num_pages + 1

    linkrange  = range(rangeleft, rangeright)

    get_string = request.get_full_path().split('?')
    get_string = '?' + get_string[1] if len(get_string) > 1 else ''

    return  {
             'paginator'     : paginator,
             'page'          : page,
             'nextpage'      : page + 1,
             'prevpage'      : page - 1,
             'hasnext'       : paginator.page(page).has_next(),
             'hasprev'       : paginator.page(page).has_previous(),
             'pages'         : linkrange,
             'pagedata'      : paginator.page(page).object_list,
             'paginatorPath' : getPaginatorPath(request.path),
             'lastpage'      : paginator.num_pages,
             'isfirstshown'  : 1 > page - links_left - 1,
             'islastshown'   : rangeright - 1 == paginator.num_pages,
             'getString'     : get_string,
            }

def getPaginatorPath(path):
    '''
        Function for having always a correct base paginator path like: baseurl/page/
    '''
    paginatorPath = ''
    pathComps = path.split('/')
    
    if pathComps[-2] == 'page':
        paginatorPath = path
    elif pathComps[-3] == 'page':
        paginatorPath = ('/').join(pathComps[:-2])
    else:
        paginatorPath = path + 'page'

    if not paginatorPath.endswith('/'):
        paginatorPath = paginatorPath + '/'
    return paginatorPath
