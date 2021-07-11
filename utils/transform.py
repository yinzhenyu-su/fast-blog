from copy import Error
from pathlib import Path
from os import makedirs
from time import time
import ffmpy



class FTransform():
    """
        使用ffmpeg进行视频加工转换的类
    """
    def __init__(self, outputDir=".") -> None:
        self.outputDir = Path(outputDir).absolute()
        # print(self.outputDir.joinpath('test.aac'))
        if (not self.outputDir.exists()):
            makedirs(self.outputDir)

    def mp42mp3(self, filename: str,) -> str:
        # if(isinstance(filename, str)):
        extIdx = filename.rfind('.')
        if (extIdx > -1):
            ext = filename[extIdx:]
            name = filename.split(ext)[0]
        else:
            name = filename
        try:
            outfilename = '{name}_{t}.mp3'.format(name=name,t=time())
            f = ffmpy.FFmpeg(inputs={filename: None},outputs={outfilename: None})
            f.run()
            return (self.outputDir.joinpath(outfilename), outfilename)
        except BaseException as err:
            print('err', err)
            return None