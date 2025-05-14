import traceback

import ezdxf

from core.pole import PoleDATAManager
from core.wire import WireDataManager
from utils.util import *
from fileio.fileloader import DxfFileHandler


class DxfManager:
    """도면 작성을 위한 클래스
    Attributes:
        v_scale (int): 종단면도 V 축척
        h_scale (int): 평면도, 종단면도 H 축척
        wiredata (WireDataManager): WireData
        poledata (PoleDATAManager): 측점 정보가 포함된 폴리선
        msp(msp): ezdxf msp객체
        doc(msp): ezdxf doc 객체
        filename(str): 저장할 파일명
    """

    def __init__(self, poledata=None, wiredata=None):
        self.v_scale: int = 0
        self.h_scale: int = 0
        self.poledata: PoleDATAManager = poledata  # ✅ PoleDATAManager.poledata 인스턴스를 가져옴
        self.wiredata: WireDataManager = wiredata
        self.msp = None
        self.doc = None
        self.filename: str = ''

    logger.debug(f'DxfManager 초기화가 완료됐습니다.')

    def run(self):
        self.create_new_dxf()
        self.initialize_default_values()
        self.create_plan_drawing()
        self.save_to_dxf()

    def initialize_default_values(self):
        """초기 축척 변수 설정 메서드"""
        self.h_scale = 1
        self.v_scale = 0.25

    def create_plan_drawing(self):
        """평면도를 생성하는 메서드
        """
        data = self.poledata
        wiredata = self.wiredata
        self.create_alignmnet()  # 선형 작성
        char_height = self.h_scale * 3

        for i in range(len(data.poles) - 1):
            try:
                pos_coord = data.poles[i].coord  # 3차원좌표
                next_pos_coord = data.poles[i + 1].coord  # 다음 전주 좌표
                vector_pos = data.poles[i].vector
                next_vector = data.poles[i + 1].vector
                gauge = data.poles[i].gauge
                pos_coord_with_offset = calculate_offset_point(vector_pos, pos_coord, gauge)

                self.create_mast(data, i, pos_coord, pos_coord_with_offset)  # 전주 생성
                self.create_bracket(data, i, pos_coord, pos_coord_with_offset, char_height)  # 브래킷 생성
                self.create_wire(data, wiredata, i, pos_coord, next_pos_coord, vector_pos, next_vector)  # 전선 생성
            except Exception as ex:
                error_message = (
                    f"예외 발생 in create_plan_drawing!\n"
                    f"인덱스: {i}\n"
                    f"예외 종류: {type(ex).__name__}\n"
                    f"예외 메시지: {ex}\n"
                    f"전체 트레이스백:\n{traceback.format_exc()}"
                )
                logger.error(error_message)
                continue

    def crate_pegging_plan_mast_and_bracket(self):
        pass

    def create_bracket(
            self, data: PoleDATAManager, i, pos_coord: Vector3, pos_coord_with_offset: Vector3, char_height: float):
        """평면도 브래킷을 생성하는 메서드
            Args:
                data (PoleDATAManager): PoleDATAManager 객체
                i (int): 인덱스
                pos_coord (Vector3): 전주 좌표
                pos_coord_with_offset (Vector3): 오프셋이 포함된 전주 좌표
                char_height(float) : 문자높이
        """
        pos_coord = pos_coord.x, pos_coord.y
        pos_coord_with_offset = pos_coord_with_offset.x, pos_coord_with_offset.y
        # 브래킷
        self.msp.add_line(pos_coord, pos_coord_with_offset, dxfattribs={'layer': '브래킷', 'color': 6})
        # 브래킷텍스트
        self.msp.add_mtext(
            f"{data.poles[i].post_number}\n"
            f"{data.poles[i].pos}\n{data.poles[i].Brackets[0].name}\n{data.poles[i].mast.name}",
            dxfattribs={'insert': pos_coord_with_offset, 'char_height': char_height, 'layer': '브래킷',
                        'color': 6})

    def create_mast(self, data: PoleDATAManager, i, pos_coord: Vector3, pos_coord_with_offset: Vector3):
        """평면도 전주를 생성하는 메서드
        Args:
            data (PoleDATAManager): PoleDATAManager 객체
            i (int): 인덱스
            pos_coord (Vector3): 전주 좌표
            pos_coord_with_offset (Vector3): 오프셋이 포함된 전주 좌표
        """
        pos_coord_with_offset = pos_coord_with_offset.x, pos_coord_with_offset.y
        self.msp.add_circle(pos_coord_with_offset, radius=1.5 * self.h_scale, dxfattribs={'layer': '전주', 'color': 4})

    def create_wire(
            self, data: PoleDATAManager, wiredata: WireDataManager, i, pos_coord: Vector3, next_coord: Vector3,
            vector_pos: float, next_vector: float):
        """평면도 전선를 생성하는 메서드
        Args:
            data (PoleDATAManager): PoleDATAManager 객체
            wiredata (WireDataManager): WireDataManager 객체
            i (int): 인덱스
            pos_coord (Vector3): 전주 좌표
            next_coord (Vector3): 다음전주 좌표
            vector_pos (float): 전주 각도
            next_vector (float): 다음 전주 각도
        """
        start_coord = calculate_offset_point(vector_pos, pos_coord, wiredata.wires[i].contactwire.stagger)
        end_coord = calculate_offset_point(next_vector, next_coord, wiredata.wires[i + 1].contactwire.stagger)
        start_coord_tuple = start_coord.x, start_coord.y
        end_coord_tuple = end_coord.x, end_coord.y
        self.msp.add_line(start_coord_tuple, end_coord_tuple, dxfattribs={'layer': '전차선', 'color': 3})
        self.create_af(data, wiredata, i, pos_coord, next_coord, vector_pos, next_vector)
        self.create_fpw(data, wiredata, i, pos_coord, next_coord, vector_pos, next_vector)

    def create_af(
            self, data: PoleDATAManager, wiredata: WireDataManager, i,
            pos_coord: Vector3, next_coord: Vector3, vector_pos: float, next_vector: float):
        """평면도 급전선를 생성하는 메서드
                Args:
                    data (PoleDATAManager): PoleDATAManager 객체
                    wiredata (WireDataManager): WireDataManager 객체
                    i (int): 인덱스
                    pos_coord (Vector3): 전주 좌표
                    next_coord (Vector3): 다음전주 좌표
                    vector_pos (float): 전주 각도
                    next_vector (float): 다음 전주 각도
        """
        start_coord = calculate_offset_point(vector_pos, pos_coord, data.poles[i].gauge +
                                             wiredata.wires[i].afwire.positionx)
        end_coord = calculate_offset_point(next_vector, next_coord, data.poles[i + 1].gauge +
                                           wiredata.wires[i + 1].afwire.positionx)
        start_coord = start_coord.x, start_coord.y
        end_coord = end_coord.x, end_coord.y
        self.msp.add_line(start_coord, end_coord, dxfattribs={'layer': '급전선', 'color': 3})

    def create_fpw(self, data: PoleDATAManager, wiredata: WireDataManager, i,
                   pos_coord: Vector3, next_coord: Vector3, vector_pos: float, next_vector: float):
        """평면도 보호선를 생성하는 메서드
        Args:
            data (PoleDATAManager): PoleDATAManager 객체
            wiredata (WireDataManager): WireDataManager 객체
            i (int): 인덱스
            pos_coord (Vector3): 전주 좌표
            next_coord (Vector3): 다음전주 좌표
            vector_pos (float): 전주 각도
            next_vector (float): 다음 전주 각도
        """
        start_coord = calculate_offset_point(vector_pos, pos_coord, data.poles[i].gauge +
                                             wiredata.wires[i].fpwwire.positionx)
        end_coord = calculate_offset_point(next_vector, next_coord, data.poles[i + 1].gauge +
                                           wiredata.wires[i + 1].fpwwire.positionx)
        start_coord = start_coord.x, start_coord.y
        end_coord = end_coord.x, end_coord.y
        self.msp.add_line(start_coord, end_coord, dxfattribs={'layer': '보호선', 'color': 3})

    def create_alignmnet(self):
        """평면도 평면선형를 생성하는 메서드
        """

        polyline_points = [(pole.coord.x, pole.coord.y) for pole in self.poledata.poles]
        self.msp.add_lwpolyline(polyline_points, close=False, dxfattribs={'layer': '선형', 'color': 1})

    def create_new_dxf(self):
        """
        dxf파일 생성함수
        """
        doc = ezdxf.new()
        msp = doc.modelspace()

        self.doc = doc
        self.msp = msp

    def save_to_dxf(self):
        """
        dxf파일 저장함수
        :return: None 저장기능 수행
        """

        dxfhandler = DxfFileHandler()
        dxfhandler.save_file_dialog()  # 파일 저장 대화상자 열기
        filename = dxfhandler.get_filepath()
        if filename:
            self.doc.saveas(filename)

    def draw_msp_rectangle(self, origin: Vector3, width: float, height: float, layer_name: str = '0', color: int = 0):
        """중심 좌표(origin)를 기준으로 폭과 높이를 가진 사각형을 그립니다.

        Args:
            origin (Vector3): 사각형 중심 좌표
            width (float): 사각형 폭
            height (float): 사각형 높이
            layer_name (str): 도면 레이어 이름
            color (int): ACI 색상 인덱스
        """
        half_w = width / 2
        half_h = height / 2

        top_right = (origin.x + half_w, origin.y + half_h)
        top_left = (origin.x - half_w, origin.y + half_h)
        bottom_left = (origin.x - half_w, origin.y - half_h)
        bottom_right = (origin.x + half_w, origin.y - half_h)

        self.msp.add_lwpolyline(
            [top_right, top_left, bottom_left, bottom_right],
            close=True,
            dxfattribs={'layer': layer_name, 'color': color}
        )

