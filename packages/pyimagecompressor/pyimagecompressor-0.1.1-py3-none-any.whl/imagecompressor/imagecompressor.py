'''
Function:
    ImageCompressor: Image compressors written by pure python
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
if __name__ == '__main__':
    from modules import *
else:
    from .modules import *


'''Image Compressor'''
class ImageCompressor():
    def __init__(self, compressor_type=None, logfilepath='imagecompressor.log', **kwargs):
        self.logger_handle = Logger(logfilepath)
        self.supported_compressors = {
            'svd': SVDCompressor,
            'dct': DCTCompressor,
            'pil': PILCompressor,
            'raisr': RAISRCompressor,
        }
        assert compressor_type in self.supported_compressors
        kwargs['logger_handle'] = self.logger_handle
        self.compressor = self.supported_compressors[compressor_type](**kwargs)
        print(self)
    '''call'''
    def __call__(self, imagepath, **kwargs):
        return self.compressor(imagepath, **kwargs)
    '''str'''
    def __str__(self):
        return 'Welcome to use ImageCompressor!\nYou can visit https://github.com/CharlesPikachu/imagecompressor for more details.'


'''test'''
if __name__ == '__main__':
    compressor = ImageCompressor('svd')
    image, eavl_result = compressor('input.jpg')
    print(eavl_result)