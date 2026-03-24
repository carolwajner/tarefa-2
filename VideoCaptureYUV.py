import numpy as np

class VideoCaptureYUV(object):
    def __init__(self, filename, resolution, bitdepth):
        self.file = open(filename, 'rb')
        self.width, self.height = resolution
        self.uv_width = self.width // 2
        self.uv_height = self.height // 2
        self.bitdepth = bitdepth

    def read_frame(self):
        Y = self.read_channel(self.height, self.width)
        U = self.read_channel(self.uv_height, self.uv_width)
        V = self.read_channel(self.uv_height, self.uv_width)

        return Y, U, V

    def read_channel(self, height, width):
        channel_len = height * width
        shape = (height, width)

        if self.bitdepth == 8:
            raw = self.file.read(channel_len)
            channel_8bits = np.frombuffer(raw, dtype=np.uint8)
            # Convert 8bits to 10 bits
            # channel = np.array(channel_8bits, dtype=np.uint16) << 2
            channel = np.array(channel_8bits, dtype=np.uint16)

        elif self.bitdepth == 10:
            # Read 2 bytes for every pixel
            raw = self.file.read(2 * channel_len)
            channel = np.frombuffer(raw, dtype=np.uint16)

        channel = channel.reshape(shape)

        return channel

    def close(self):
        self.file.close()



