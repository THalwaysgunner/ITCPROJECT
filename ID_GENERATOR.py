import uuid
import pickle
import config_logger as cfl
import tags as t
import os


def get_id(data):
    """
    the function will generate a unique stock id- the unique id will used to Differentiate themselves
    from other stocks and used as foreign key in DB
    the keys value (symbol : uuid) are saved in a pkl file
    every time we have to generate a new id before we populate our table we will read the file - if the symbol already
    exists in the file we will return the appropriate unique id else we generate a new id and save the new key into
    the file before we return the new key
    :param data: list of symbol
    :return: data with keys
    """

    id_col = []

    file_p = os.path.abspath(t.FILE_NAME)
    try:
        _file = open(t.FILE_NAME, "rb")
        unique_id_dic = pickle.load(_file)
        unique_id_dic = {k.translate({32: None}): v for k, v in unique_id_dic.items()}  # make sure we have the
        # correct format before working with the pkl file
        cfl.logging.info(f' successfully load symbol - id dictionary file from {file_p}')
        _file.close()

        for i in data['Symbol']:

            sym = i

            if sym in unique_id_dic:

                print("symbol exists")
                _id = unique_id_dic.get(sym)
                id_col.append(_id)

                cfl.logging.info(f' symbol - id dictionary file successfully closed\n')
                cfl.logging.info(f' successfully retrieve uuid for {i}')

            else:

                print(f"generate unique id for {i}\n")
                _id = str(uuid.uuid4().fields[-1])[:5]
                size = len(i)
                unique_id = f'{_id}-{size}'
                boolean = unique_id in unique_id_dic.values()
                print(boolean)
                cfl.logging.info(f'unique id for {i} is {unique_id}\n')

                # checking that we didn't generate an id that already exist in the data
                # data.loc[(data['Symbol'] == i), 'ID'] = unique_id
                id_col.append(_id)
                unique_id_dic[i] = unique_id
                _file = open(t.FILE_NAME, 'wb')
                pickle.dump(unique_id_dic, _file)
                _file.close()

                cfl.logging.info(f' symbol - id dictionary file successfully closed\n')
                cfl.logging.info(f' successfully generate new uuid for {i}')

        _file.close()
        return id_col

    except ValueError as e:
        cfl.logging.error(f'{e}')
        print(e)
