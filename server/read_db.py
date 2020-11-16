class Read_DB:
    def read_txt(self, filename):
        with open(filename) as f:
            data = []
            item = f.read().replace('\n', '<br>')
            data.append(item)
        return data
