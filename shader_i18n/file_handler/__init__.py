# 完成整个文件处理流程
import tempfile
import zipfile
import os
import shutil

from shader_i18n.errors.shader_pack_file import ShaderPackFileError


class ShaderPackHandler:
    """
    文件处理流程
    """

    def __init__(self, file_path: str, in_place: bool = True,output_file_path: str = None):
        """
        初始化文件处理流程
        
        params:
            file_path: 原 shader pack 文件路径
            in_place: 是否原地处理
            output_file_path: 输出文件路径，只在 in_place 为 False 时有效
        return:
            None
        """
        self.file_path = file_path
        self.in_place = in_place
        self.output_file_path = output_file_path

        if not zipfile.is_zipfile(self.file_path):
            raise ShaderPackFileError('文件不是 zip 格式')
        if not self.is_shader_pack():
            raise ShaderPackFileError('文件不是 shader pack 文件')
    
    def is_shader_pack(self):
        r"""
        检测文件是否为shader pack文件，通过 shaders\shaders.properties 文件判断
        
        return:
            bool: 是否为shader pack文件
        """
        # 检查是否包含shaders.properties文件
        with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
            if 'shaders/shaders.properties' not in zip_ref.namelist():
                return False
        return True

    def __enter__(self):
        """
        进入上下文管理器
        """
        if not self.in_place:
            # 复制zip文件到临时目录，不做解压
            self.temp_dir = tempfile.TemporaryDirectory()
            shutil.copy(self.file_path, os.path.join(self.temp_dir.name, os.path.basename(self.file_path)))
            

        return self

    @property
    def lang_list(self):
        """
        语言列表
        """
        # 语言文件在zip文件的 shaders/lang目录下如 shaders/lang/en_us.lang 返回 en_us
        with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
            lang_list = []
            for name in zip_ref.namelist():
                if name.startswith('shaders/lang/'):
                    if os.path.basename(name).split('.')[0] == '':
                        continue
                    lang_list.append(os.path.basename(name).split('.')[0])
        
        return lang_list

    def get_lang_file(self, lang: str):
        """
        获取指定语言文件的内容
        
        params:
            lang: 语言代码
        return:
            str: 语言文件内容
        """
        # 语言文件在zip文件的 shaders/lang目录下如 shaders/lang/en_us.lang 返回 en_us.lang
        try:
            with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
                with zip_ref.open(f'shaders/lang/{lang}.lang', 'r') as lang_file:
                    lang_content = lang_file.read().decode('utf-8')
            return lang_content
        except KeyError:
            raise ShaderPackFileError(f'语言文件 shaders/lang/{lang}.lang 不存在')

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        退出上下文管理器
        """
        if not self.in_place:
            # 复制临时目录的zip文件到输出文件路径
            shutil.copy(os.path.join(self.temp_dir.name, os.path.basename(self.file_path)), self.output_file_path)
            # 关闭临时目录
            self.temp_dir.cleanup()
