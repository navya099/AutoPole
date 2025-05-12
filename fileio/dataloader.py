from .fileloader import TxTFileHandler, ExcelFileHandler, PolylineHandler
from utils.util import *


class DataLoader:
    def __init__(self, design_params: dict[str, int | float], file_paths: dict[str, str]):
        self.design_params = design_params
        self.file_paths = file_paths
        self.last_block: int = 0

        # ✅ StringVar를 사용하여 안전하게 값 가져오기
        try:
            self.designspeed: int = design_params['designspeed']  # 설계 속도
            self.linecount: int = design_params['linecount']  # 선로 개수
            self.lineoffset: float = design_params['lineoffset']  # 선로 간격
            self.poledirection: int = design_params['poledirection']  # 전주 방향
        except (KeyError, TypeError, ValueError) as e:
            logger.error(f"입력값 오류: {e}")
            self.designspeed = 250
            self.linecount = 1
            self.lineoffset = 0.0
            self.poledirection = -1

        # ✅ 파일 경로 설정 (None 체크 포함)
        self.curve_path = file_paths['curve_path']
        self.pitch_path = file_paths['pitch_path']
        self.coord_path = file_paths['coord_path']
        self.structure_path = file_paths['structure_path']

        # ✅ 디버깅 로그 추가 (logger 오류 수정)
        logger.info(f"""DataLoader - 파일 경로 목록:
        curve_list: {self.curve_path}
        pitch_path: {self.pitch_path}
        coord_path: {self.coord_path}
        structure_path: {self.structure_path}""")

        # ✅ 파일 로드 (빈 문자열 예외 처리 추가)
        # 인스턴스 추가
        self.txtprocessor = TxTFileHandler()
        self.excelprocessor = ExcelFileHandler()
        self.polylineprocessor = PolylineHandler()

        if self.curve_path:
            self.txtprocessor.set_filepath(self.curve_path)  # self속성에 경로 추가
            self.txtprocessor.read_file_content()  # 파일 읽기 splitlines
            self.data = self.txtprocessor.get_data()  # get
            self.curve_list = self.txtprocessor.process_info(mode='curve')
        else:
            logger.error("curve_info 파일 경로가 설정되지 않았습니다.")
            self.data = ''
            self.curve_list = []

        if self.pitch_path:
            self.txtprocessor.set_filepath(self.pitch_path)
            self.txtprocessor.read_file_content()
            self.pitch_list = self.txtprocessor.process_info(mode='pitch')
        else:
            logger.error("pitch_info 파일 경로가 설정되지 않았습니다.")
            self.pitch_list = []

        if self.coord_path:
            self.polylineprocessor.set_filepath(self.coord_path)
            self.polylineprocessor.convert_txt_to_polyline()
            self.coord_list = self.polylineprocessor.get_polyline()
        else:
            logger.error("coord_info 파일 경로가 설정되지 않았습니다.")
            self.coord_list = []

        if self.structure_path:
            self.excelprocessor.set_filepath(self.structure_path)
            self.struct_dic = self.excelprocessor.process_structure_data()

        else:
            logger.error("structure 파일 경로가 설정되지 않았습니다.")
            self.struct_dic = {}
        try:
            self.last_block = find_last_block(self.data) if self.data else 0
            logger.info(f" last_block {self.last_block}")
        except Exception as e:
            logger.error(f"last_block 계산 오류: {e}")
            self.last_block = 0

        self.start_km = 0
        self.end_km = (self.last_block // 1000) if self.last_block else 600  # 마지막측점 예외시 600
        logger.info(f""" start_km : {self.start_km}
                    end_km {self.end_km}""")
        list_params = self.curve_list, self.pitch_list, self.coord_list, self.struct_dic, self.end_km
        self.params = [design_params, list_params]
