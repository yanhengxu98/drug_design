import numpy as np
import matplotlib.pyplot as plt
import os

class FTIR_PL_Spectrum:
    '''
    专门负责PL IR光谱的读取和作图，基本idea就是排列最新文件，读文件，
    然后根据文件作图，保存之后再show到UI上。
    '''
    def get_newest_file(self, path):
        '''
        返回path下最新生成的txt路径。
        :param path:
        :return:
        '''
        files = os.listdir(path)
        files.sort(key=lambda fn: os.path.getmtime(os.path.join(path, fn)) if fn.endswith('.txt') else 0)
        return os.path.join(path, files[-1])

    def read_PL_data(self, PL_raw_file):
        with open(PL_raw_file) as f:
            all_data = f.read().split('\n')[17:-2]  # 以行分割，读文件，只取数据部分

        all_data = np.transpose(np.array([list(map(float, d.split('\t'))) for d in all_data]))
        x = all_data[0]
        y = all_data[1]
        return x, y

    def get_image(self, file, num_peak, dpi=100):
        return 0
