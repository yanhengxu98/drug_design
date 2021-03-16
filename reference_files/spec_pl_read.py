# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler, FileCreatedEvent
import time
# from spectrum_analyzer import SpectrumAnalyzer as sa
import numpy as np
import matplotlib.pyplot as plt
import cv2
# from IPython import display
from copy import deepcopy
from scipy.optimize import leastsq
from scipy.optimize import curve_fit
from PIL import Image
import os
import glob
import zerorpc
import clr
clr.AddReference('IdeaOptics')
from IdeaOptics import Wrapper
wrapper = Wrapper()
wrapper.OpenAllSpectrometers()
wrapper.getName(0)
wrapper.getSerialNumber(0)
wrapper.getNumberOfPixels(0)
wrapper.setBoxcarWidth(0, 1)
wrapper.setIntegrationTime(0, 1000)
wrapper.setScansToAverage(0, 1)


def plot_raman():
    wavelength = list(wrapper.getWavelengths(0))
    spec = list(wrapper.getSpectrum(0))
    plt.plot(1e7 / 531.5 - 1e7 / np.array(wavelength), spec)
    plt.show()


def read_txt(file):
    with open(file) as f:
        return f.read().split('\n')


def read_data(file):
    data = read_txt(file)
    data = data[17:-2]
    data = np.transpose(np.array([list(map(float, d.split('\t'))) for d in data]))
    x = data[0]
    y = data[1]
    return x, y

def get_init_p(centers):
    p = []
    for c in centers:
        p.extend([1.,c,1.])
    return p

def get_init_p_num(n):
    return get_init_p(np.linspace(400,800,n+2)[1:-1])

def gaussian_wave(x,p):
    a, b, c= p[0],p[1],p[2]
    return a*np.exp(-(x-b)**2/(2*c**2))

def func(x,*p):
    res = 0
    for i in range(len(p)//3):
        res += gaussian_wave(x,p[i*3:i*3+3])
    return res

def split_curve(x,params):
    return [gaussian_wave(x,params[3*i:3*i+3]) for i in range(len(params)//3)]

def void_noise(y_input):
    y_blur = cv2.GaussianBlur(y_input, (1, 11), 20)
    for i in range(10):
        y_blur = cv2.GaussianBlur(y_blur, (1, 5), 5)
    for i in range(3):
        y_blur = cv2.blur(y_blur, (1, 11))
    temp = deepcopy(y_blur)
    for i in range(2, inplen(y_blur) - 2):
        temp[i + 2] = np.median(y_blur[i:i + 5])

    return y_blur


def getImage(file, num_peak, dpi=100):
    x, y = read_data(file)
    print(x, y)
    p0 = get_init_p_num(num_peak)
    plsq = curve_fit(func, x, y, p0=p0)[0]
    y2 = func(x, *plsq)
    ys = split_curve(x, plsq)
    fig = plt.figure(dpi=dpi)
    plt.xlim(400, 800)
    plt.ylim(0, 3 * max(y))  # 65000 before
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('PL Intensity')
    #plt.title('$CdSe_x$ X = %.3f'%title,{'size':25},y=1.25)
    ax = plt.gca()
    ax.spines['top'].set_visible(False) #去掉上边框
    ax.spines['right'].set_visible(False) #去掉右边框
    plt.plot(x, y)
    texts = []
    for i, sub_curve in enumerate(ys):
        plt.plot(x,sub_curve,'--')
        x_center, peak, LFWHM = plsq[1+3*i], plsq[3*i], abs(plsq[3*i+2])*2.355
        #texts.append(plt.text(plsq[1+3*i], peak,'Center: %.2f'%x_center+'\nIntensity: %.2f'%peak+'\nLFWHM: %.2f'%(LFWHM)))
        plt.annotate('Center: %.2f'%x_center+'\nIntensity: %.2f'%peak+'\nLFWHM: %.2f'%(LFWHM), xy=(x_center, peak),
                     xytext=(plsq[1+3*i], peak+peak*0.5+1000 if peak+peak*0.5+3000 < 65000 else 65000),
                     arrowprops=dict(arrowstyle='->', color='red',lw=1.5))
    #adjust_text(texts,arrowprops=dict(arrowstyle='->', color='red',lw=.5))
    plt.tight_layout()
    canvas = fig.canvas
    buf, size = canvas.print_to_buffer()
    image = np.array(Image.frombuffer('RGBA', size, buf, 'raw', 'RGBA', 0, 1))
    return image


def on_call_newest_data():
    x, y = read_data(newest_result_file)
    p0 = get_init_p_num(3)
    plsq = curve_fit(func, x, y, p0=p0)[0]
    y2 = func(x, *plsq)
    ys = split_curve(x, plsq)
    return x, y, plsq

'''class MyDirEventHandler(FileSystemEventHandler):
    def on_moved(self, event):
        print(event)

    def on_created(self, event):
        print(event)
        time.sleep(0.1)
        display.clear_output(wait=True)
        # image = spectrum1.get_image(event.src_path, 3)
        # cv2.imshow('img', image)
        # cv2.waitKey(1)
        global newest_result_file
        newest_result_file = event.src_path
        aaa, bbb, plsq = on_call_newest_data()
        print(aaa, bbb)
        print(plsq)
        print("succ")

    def on_deleted(self, event):
        print(event)

    def on_modified(self, event):
        print("modified:", event)'''


def get_newest_file(path):
    files = os.listdir(path)
    files.sort(key=lambda fn: os.path.getmtime(os.path.join(path,fn)) if fn.endswith('.txt') else 0)
    return os.path.join(path, files[-1])


class Controller:
    def get_img(self):
        file_path = get_newest_file('txtdata')
        image = getImage(file_path, 3)
        # cv2.imwrite('aaa.jpg', image)
        return cv2.imencode('.jpg', image)[1].tostring()

    def get_img_data(self):
        file_path = get_newest_file('txtdata')
        x, y = read_data(file_path)
        return x, y

    def get_raman_results(self):
        print("show raman")

        import threading
        a = list(wrapper.getWavelengths(0))
        b = list(wrapper.getSpectrum(0))
        fig = plt.figure()
        plt.plot(1e7 / 531.5 - 1e7 / np.array(a), b)
        canvas = fig.canvas
        buf, size = canvas.print_to_buffer()
        image = np.array(Image.frombuffer('RGBA', size, buf, 'raw', 'RGBA', 0, 1))
        # cv2.imwrite('bbb.jpg', image)
        plt.close('all')
        return cv2.imencode('.jpg', image)[1].tostring()

    def get_raman_data(self):
        a = list(wrapper.getWavelengths(0))
        b = list(wrapper.getSpectrum(0))
        return a, b




"""
使用watchdog 监控文件的变化
"""
if __name__ == '__main__':
    # 创建观察者对象
    #plt.ion()
    '''observer = Observer()
    # 创建事件处理对象
    fileHandler = MyDirEventHandler()

    # 为观察者设置观察对象与处理事件对象
    observer.schedule(fileHandler, "../txtdata/", True)
    observer.start()
    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()'''
    print("spectrum ok...")
    controller_image = Controller()
    s = zerorpc.Server(controller_image)

    s.bind("tcp://0.0.0.0:4244")

    try:
        s.run()
        print("Running ...")
    except KeyboardInterrupt:
        s.close()
        print("Exiting ...")
        exit()
