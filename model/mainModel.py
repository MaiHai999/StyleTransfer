import os
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import PIL.Image

os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'
mpl.rcParams['figure.figsize'] = (12, 12)
mpl.rcParams['axes.grid'] = False


from model.StyleContentModel import StyleContentModel

class TransferStyle:
    def __init__(self):
        self.content_layers = ['block5_conv2']
        self.style_layers = ['block1_conv1',
                             'block2_conv1',
                             'block3_conv1',
                             'block4_conv1',
                              'block5_conv1']

        self.num_content_layers = len(self.content_layers)
        self.num_style_layers = len(self.style_layers)
        self.style_weight = 1e-2
        self.content_weight = 1e4
        self.opt = tf.keras.optimizers.Adam(learning_rate=0.02, beta_1=0.99, epsilon=1e-1)

    def tensor_to_image(self , tensor):
        tensor = tensor * 255
        tensor = np.array(tensor, dtype=np.uint8)
        if np.ndim(tensor) > 3:
            assert tensor.shape[0] == 1
            tensor = tensor[0]
            return PIL.Image.fromarray(tensor)

    def load_img(self, path_to_img):
        max_dim = 512
        img = tf.io.read_file(path_to_img)
        img = tf.image.decode_image(img, channels=3)
        img = tf.image.convert_image_dtype(img, tf.float32)

        shape = tf.cast(tf.shape(img)[:-1], tf.float32)
        long_dim = max(shape)
        scale = max_dim / long_dim

        new_shape = tf.cast(shape * scale, tf.int32)

        img = tf.image.resize(img, new_shape)
        img = img[tf.newaxis, :]
        return img

    def imshow(self, image, title=None):
        if len(image.shape) > 3:
            image = tf.squeeze(image, axis=0)

        plt.imshow(image)
        if title:
            plt.title(title)

    def clip_0_1(self ,image):
        return tf.clip_by_value(image, clip_value_min=0.0, clip_value_max=1.0)

    def style_content_loss(self, outputs):
        style_outputs = outputs['style']
        content_outputs = outputs['content']
        style_loss = tf.add_n([tf.reduce_mean((style_outputs[name] - self.style_targets[name]) ** 2)
                               for name in style_outputs.keys()])
        style_loss *= self.style_weight / self.num_style_layers

        content_loss = tf.add_n([tf.reduce_mean((content_outputs[name] - self.content_targets[name]) ** 2)
                                 for name in content_outputs.keys()])
        content_loss *= self.content_weight / self.num_content_layers
        loss = style_loss + content_loss
        return loss

    @tf.function()
    def train_step(self ,image):
        with tf.GradientTape() as tape:
            outputs = self.extractor(image)
            loss = self.style_content_loss(outputs)

        grad = tape.gradient(loss, image)
        self.opt.apply_gradients([(grad, image)])
        image.assign(self.clip_0_1(image))

    def run(self,content_path,style_path , epochs):
        self.content_path = content_path
        self.style_path = style_path
        content_image = self.load_img(self.content_path)
        style_image = self.load_img(self.style_path)

        self.extractor = StyleContentModel(self.style_layers, self.content_layers)
        self.style_targets = self.extractor(style_image)['style']
        self.content_targets = self.extractor(content_image)['content']

        image = tf.Variable(content_image)

        for _ in range(epochs):
            self.train_step(image)

        tensor_image = self.tensor_to_image(image)
        current_directory = os.path.dirname(__file__)
        current_directory = current_directory.replace("/model", "")
        path = current_directory + "/asset/picture/transferPicture.jpg"
        self.path = path
        tensor_image.save(path)


if __name__ == '__main__':
    a = TransferStyle()
    current_directory = os.path.dirname(__file__)
    current_directory = current_directory.replace("/model" , "")

    image1_path = current_directory + "/asset/picture/landscape.jpg"
    image2_path = current_directory + "/asset/picture/a-starry-sky.jpg"

    a.run(image1_path, image2_path , 3)








