import glob


def get_test_ids(path):
    ids = []
    filepaths = glob.glob(path + "/*.jpg")
    filepaths.sort()
    ids = [filepath.split("/")[-1][:-4] for filepath in filepaths]
    return ids, filepaths
