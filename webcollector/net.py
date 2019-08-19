# coding=utf-8


class Requester(object):

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_response(self, crawl_datum):
        raise NotImplementedError()

    def create_async_context_manager(self):
        return None


with Requester() as r:
    print(r)