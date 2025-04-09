import ezdxf
from utils.util import *
from fileio.fileloader import DxfFileHandler


class DxfManager:
    def __init__(self, poledata=None, wiredata=None):
        self.v_scale = 0
        self.h_scale = 0
        self.poledata = poledata  # ✅ PoleDATAManager.poledata 인스턴스를 가져옴
        self.wiredata = wiredata
        self.msp = None
        self.doc = None
        self.filename = None

    def run(self):
        self.create_new_dxf()
        self.initialize_default_values()
        self.create_plan_drawing()
        self.save_to_dxf()

    def initialize_default_values(self):
        self.h_scale = 1
        self.v_scale = 0.25

    def create_plan_drawing(self):
        data = self.poledata
        wiredata = self.wiredata
        self.create_alignmnet()  # 선형 작성
        char_height = self.h_scale * 3

        for i in range(len(data.poles) - 1):
            pos_coord = (data.poles[i].coord.x, data.poles[i].coord.y)  # 2차원좌표
            next_pos_coord = (data.poles[i + 1].coord.x, data.poles[i + 1].coord.y)
            vector_pos = data.poles[i].vector
            next_vector = data.poles[i + 1].vector
            gauge = data.poles[i].gauge
            pos_coord_with_offset = calculate_offset_point(vector_pos, pos_coord, gauge)

            self.create_mast(data, i, pos_coord, pos_coord_with_offset)  # 전주 생성
            self.create_bracket(data, i, pos_coord, pos_coord_with_offset, char_height)  # 브래킷 생성
            self.create_wire(wiredata, i, pos_coord, next_pos_coord, vector_pos, next_vector)  # 전선 생성

    def crate_pegging_plan_mast_and_bracket(self):
        pass

    def create_bracket(self, data, i, pos_coord, pos_coord_with_offset, char_height):
        # 브래킷
        self.msp.add_line(pos_coord, pos_coord_with_offset, dxfattribs={'layer': '브래킷', 'color': 6})
        # 브래킷텍스트
        self.msp.add_mtext(
            f"{data.poles[i].post_number}\n{data.poles[i].pos}\n{data.poles[i].Brackets[0].name}\n{data.poles[i].mast.name}",
            dxfattribs={'insert': pos_coord_with_offset, 'char_height': char_height, 'layer': '브래킷',
                        'color': 6})

    def create_mast(self, data, i, pos_coord, pos_coord_with_offset):
        self.msp.add_circle(pos_coord_with_offset, radius=1.5 * self.h_scale, dxfattribs={'layer': '전주', 'color': 4})

    def create_wire(self, wiredata, i, pos_coord, next_coord, vector_pos, next_vector):
        start_coord = calculate_offset_point(vector_pos, pos_coord, wiredata.wires[i].contactwire.stagger)
        end_coord = calculate_offset_point(next_vector, next_coord, wiredata.wires[i + 1].contactwire.stagger)

        self.msp.add_line(start_coord, end_coord, dxfattribs={'layer': '전차선', 'color': 3})

    def create_alignmnet(self):
        # 선형 플롯

        polyline_points = [(pole.coord.x, pole.coord.y) for pole in self.poledata.poles]
        self.msp.add_lwpolyline(polyline_points, close=False, dxfattribs={'layer': '선형', 'color': 1})

    def create_new_dxf(self):
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

    def draw_msp_rectangle(self, origin, width, height, layer_name='0', color=0):
        p1 = (origin[0] + width / 2, origin[1] + height / 2)  # 오른쪽 위
        p2 = (p1[0] - width, p1[1])  # 왼쪽 위
        p3 = (p2[0], p2[1] - height)  # 왼쪽 아래
        p4 = (p1[0], p3[1])  # 오른쪽 아래

        # 사각형 그리기
        self.msp.add_lwpolyline([p1, p2, p3, p4, p1], dxfattribs={'layer': layer_name, 'color': color})
