import pickle
import tags as t

_file = open(t.FILE_NAME, "rb")
unique_id_dic = pickle.load(_file)
unique_id_dic = {k.translate({32: None}): v for k, v in unique_id_dic.items()}
_file.close()


_id = unique_id_dic.get('TSLA')
print(_id)