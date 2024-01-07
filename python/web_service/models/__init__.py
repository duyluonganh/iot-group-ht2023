from .dnn import CNN1D

'''
setup(): Create a model

Input:
    config(Class)
    n_feats(int): Number of features (neural network input tensor size)
'''
def setup(config, n_feats):
    model = CNN1D(
        input_shape = n_feats,
        num_classes = len(config.class_labels),
        lr = config.lr,
        n_kernels = config.n_kernels,
        kernel_sizes = config.kernel_sizes,
        hidden_size = config.hidden_size,
        dropout = config.dropout
    )

    return model
