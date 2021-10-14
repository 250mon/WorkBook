
class HandleIds():
    def __init__(self, filename):
       self.filename = filename

    def get_idpw(self, site, filename=None):
        if filename is None:
            filename = self.filename
        with open(filename, 'r') as f:
            list_ids = f.readlines()
        list_id_strs =  [str.split(';') for str in list_ids]
        dict_ids = {site: {'id': id, 'pw': pw} for site, id, pw in list_id_strs}
        return dict_ids.get(site)['id'], dict_ids.get(site)['pw']


if __name__ == '__main__':
    ids = HandleIds('ids.txt')
    print(ids.get_idpw('Seoul'))
