class ShaderPackFileError(Exception):
    """
    shader pack 文件错误
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
    
    def __str__(self):
        return self.message
    