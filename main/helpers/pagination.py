class MakePaginate():
    def __init__(self):
        self.response = {
            'data': [],
            'total': None,
            'pages': None,
            'current_page': None,
            'next_page': None,
            'prev_page': None
        }

    def paginate(self, models):
        response = dict()
        response['data'] = [item.to_json() for item in models.items]
        response['total'] = models.total
        response['pages'] = models.pages
        response['current_page'] = models.page
        response['next_page'] = models.next_num if models.has_next is True else None
        response['prev_page'] = models.prev_num if models.has_prev is True else None
        self.response = response
