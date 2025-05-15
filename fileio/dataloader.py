from dataclasses import dataclass
from .fileloader import TxTFileHandler, ExcelFileHandler, PolylineHandler
from utils.util import *


@dataclass
class DataBundle:
    """
    파라미터 보관을 위한 데이터 클래스
    Attributes:
        designspeed : 설계속도
        linecount: 선로 갯수
        lineoffset: 선로중심간격
        poledirection: 전주 설치방향(-1/1)
        mode: 설치모드(0=기존/1=신규)
        curve_path: curve_info 경로
        pitch_path: pitch_info 경로
        coord_path: coord_info 경로
        structure_path: structure_info 경로
    """
    designspeed: int = 0
    linecount: int = 0
    lineoffset: float = 0.0
    poledirection: int = -1
    mode: int = 1
    curve_path: str = ''
    pitch_path: str = ''
    coord_path: str = ''
    structure_path: str = ''


class DataLoader:
    def __init__(self, databudle: DataBundle):
        self.databudle = databudle
        self.last_block: int = 0

        # ✅ 파일 로드 (빈 문자열 예외 처리 추가)
        # 인스턴스 추가
        self.txtprocessor = TxTFileHandler()
        self.excelprocessor = ExcelFileHandler()
        self.polylineprocessor = PolylineHandler()

        if self.databudle.curve_path:
            self.txtprocessor.set_filepath(self.databudle.curve_path)  # self속성에 경로 추가
            self.txtprocessor.read_file_content()  # 파일 읽기 splitlines
            self.data = self.txtprocessor.get_data()  # get
            self.curve_list = self.txtprocessor.process_info(mode='curve')
        else:
            logger.error("curve_info 파일 경로가 설정되지 않았습니다.")
            self.data = ''
            self.curve_list = []

        if self.databudle.pitch_path:
            self.txtprocessor.set_filepath(self.databudle.pitch_path)
            self.txtprocessor.read_file_content()
            self.pitch_list = self.txtprocessor.process_info(mode='pitch')
        else:
            logger.error("pitch_info 파일 경로가 설정되지 않았습니다.")
            self.pitch_list = []

        if self.databudle.coord_path:
            self.polylineprocessor.set_filepath(self.databudle.coord_path)
            self.polylineprocessor.convert_txt_to_polyline()
            self.coord_list = self.polylineprocessor.get_polyline()
        else:
            logger.error("coord_info 파일 경로가 설정되지 않았습니다.")
            self.coord_list = []

        if self.databudle.structure_path:
            self.excelprocessor.set_filepath(self.databudle.structure_path)
            self.struct_dic = self.excelprocessor.process_structure_data()

        else:
            logger.error("structures 파일 경로가 설정되지 않았습니다.")
            self.struct_dic = {}
        try:
            self.last_block = find_last_block(self.data) if self.data else 0
            logger.info(f" last_block {self.last_block}")
        except Exception as e:
            logger.error(f"last_block 계산 오류: {e}")
            self.last_block = 0

        self.start_km: float = 0.0
        self.end_km: float = (self.last_block / 1000) if self.last_block else 600  # 마지막측점 예외시 600
        logger.info(f""" start_km : {self.start_km}
                    end_km {self.end_km}""")





