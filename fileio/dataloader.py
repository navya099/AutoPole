from dataclasses import dataclass
from utils.logger import logger
from geometry.alignment import BVEAlignment
from structures.structure import StructureCollection
from .fileloader import TxTFileHandler, ExcelFileHandler, PolylineHandler


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
        start_sta: 시작 측점
        end_sta: 끝 측점
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
    start_sta: float = 0.0
    end_sta: float = 0.0
    offset: float = 0.0

class DataLoader:
    def __init__(self, databudle: DataBundle):
        self.databudle = databudle
        self.bvealignment: BVEAlignment = BVEAlignment()
        self.structures: StructureCollection = StructureCollection()
        # ✅ 파일 로드 (빈 문자열 예외 처리 추가)
        # 인스턴스 추가
        self.txtprocessor = TxTFileHandler()
        self.excelprocessor = ExcelFileHandler()
        self.polylineprocessor = PolylineHandler()

        # 초기화 메서드 실행
        self.load_alignment_data()

    def load_alignment_data(self):
        if self.databudle.curve_path:
            self.txtprocessor.set_filepath(self.databudle.curve_path)  # self속성에 경로 추가
            self.txtprocessor.read_file_content()  # 파일 읽기 splitlines
            self.txtprocessor.process_info(self.bvealignment, mode='curve')
        else:

            logger.error("curve_info 파일 경로(databundle.curve_path)가 설정되지 않았습니다.")

        if self.databudle.pitch_path:
            self.txtprocessor.set_filepath(self.databudle.pitch_path)
            self.txtprocessor.read_file_content()
            self.txtprocessor.process_info(self.bvealignment, mode='pitch')
        else:
            logger.error("pitch_info 파일 경로(databundle.pitch_path)가 설정되지 않았습니다.")

        if self.databudle.coord_path:
            self.polylineprocessor.set_filepath(self.databudle.coord_path)
            self.polylineprocessor.convert_txt_to_polyline(self.bvealignment)
        else:
            logger.error("coord_info 파일 경로(databundle.coord_path)가 설정되지 않았습니다.")

        if self.databudle.structure_path:
            self.excelprocessor.set_filepath(self.databudle.structure_path)
            self.excelprocessor.process_structure_data(self.structures)
            self.structures.apply_offset(self.databudle.offset)

        else:
            logger.error("structures 파일 경로(databundle.structure_path)가 설정되지 않았습니다.")
