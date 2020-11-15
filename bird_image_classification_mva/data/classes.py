def retrieve_class_names(filepaths):
    class_names = {filepath.split("/")[-2] for filepath in filepaths}
    num_classes = len(class_names)
    class_encoding = {class_name: class_index for class_index, class_name in enumerate(class_names)}
    print("Number of classes detected: {}".format(num_classes))
    return class_names, num_classes, class_encoding
