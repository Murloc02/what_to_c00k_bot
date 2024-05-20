from min_dalle import MinDalle
from pickle import dump, load

model_file = 'light_model.pkl'


def create_model(file_name=model_file):
    model = MinDalle(
        models_root='./pretrained',
        is_mega=False,
        is_reusable=True
    )

    with open(file_name, 'wb') as file:
        dump(model, file)


def load_model(file_name=model_file):

    try:
        file = open(file_name, 'rb')
    except FileNotFoundError:
        create_model(file_name)
        file = open(file_name, 'rb')
    except BaseException:
        raise 'Неизвестная ошибка при чтении файла'

    model = load(file)
    file.close()

    return model


if __name__ == '__main__':
    create_model()
