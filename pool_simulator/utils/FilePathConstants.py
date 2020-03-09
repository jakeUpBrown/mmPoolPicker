class FilePathConstants:
    @staticmethod
    def get_data_dir():
        return "C:\\Users\\jakeE\\PycharmProjects\\mmPoolPicker\\data\\"

    @staticmethod
    def get_data_file(filename):
        return FilePathConstants.get_data_dir() + filename

    @staticmethod
    def get_output_dir():
        return "C:\\Users\\jakeE\\PycharmProjects\\mmPoolPicker\\output\\"

    @staticmethod
    def get_output_file(filename):
        return FilePathConstants.get_output_dir() + filename
