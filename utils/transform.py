from pathlib import Path
from os import makedirs, path
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

    def video2mp3(
        self,
        filename: str,
    ) -> str:
        # if(isinstance(filename, str)):
        extIdx = filename.rfind('.')
        ext = filename[extIdx:]
        name = filename.split(ext)[0]
        outfilename = '{name}_{t}.mp3'.format(name=name, t=time())
        f = ffmpy.FFmpeg(inputs={filename: None}, outputs={outfilename: None})
        [out, err] = f.run()
        if err:
            return None
        return path.basename(outfilename)
