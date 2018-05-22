from pure_pagination import Paginator,EmptyPage,PageNotAnInteger

def paging(all_blogs,request,nums = 6):
    try:
        page = request.GET.get('page',1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(all_blogs,nums,request = request)
    blogs = p.page(page)

    return blogs