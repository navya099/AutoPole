from core.pole import PoleDATAManager
from core.wire import WireDataManager
from .fileloader import *
from utils.util import Direction


class BVECSV:
    def __init__(self, poledata=None, wiredata=None):
        self.poledata: PoleDATAManager = poledata  # ✅ PoleDATAManager.poledata 인스턴스를 가져옴
        self.wiredata: WireDataManager = wiredata
        self.lines = []

    def create_pole_csv(self):
        self.lines = []  # 코드 실행전 초기화
        self.lines.append(',;전주구문\n')
        data = self.poledata
        for i in range(len(data.poles) - 1):
            try:
                pos = data.poles[i].pos
                post_number = data.poles[i].post_number
                mastindex = data.poles[i].mast.index
                mastname = data.poles[i].mast.name
                bracketindex = data.poles[i].Brackets[0].index
                bracketname = data.poles[i].Brackets[0].name
                feederindex = data.poles[i].feeder.index
                feedername = data.poles[i].feeder.name
                current_airjoint = data.poles[i].current_airjoint
                current_structure = data.poles[i].current_structure
                current_curve = data.poles[i].current_curve
                gauge = data.poles[i].gauge
                direction = data.poles[i].direction

                if direction == Direction.LEFT:
                    pitch = 0
                    gauge *= -1
                else:
                    pitch = 180

                # 구문 작성
                self.lines.append(f',;{post_number}\n')
                self.lines.append(f',;-----{current_airjoint}({current_structure})({current_curve})-----\n')
                self.lines.append(f'{pos},.freeobj 0;{mastindex};{gauge},;{mastname}\n')
                self.lines.append(f'{pos},.freeobj 0;{bracketindex};0;0;{pitch};,;{bracketname}\n\n')
                self.lines.append(f'{pos},.freeobj 0;{feederindex};{gauge};0;{pitch};,;{feedername}\n\n')
            except AttributeError as e:
                logger.warning(f"poledata 데이터 누락: index {i}, 오류: {e}")
            except Exception as e:
                logger.error(f"예상치 못한 오류: index {i}, 오류: {e}")
        logger.info(f'create_pole_csv실행이 완료됐습니다.')

    def create_wire_csv(self):
        self.lines = []  # 코드 실행전 초기화
        self.lines.append(',;전차선구문\n')
        data = self.poledata
        wiredata = self.wiredata
        for i in range(len(data.poles) - 1):
            try:
                pos = data.poles[i].pos
                post_number = data.poles[i].post_number
                current_airjoint = data.poles[i].current_airjoint
                current_structure = data.poles[i].current_structure
                current_curve = data.poles[i].current_curve
                contact_index = wiredata.wires[i].contactwire.index
                af_index = wiredata.wires[i].afwire.index
                af_x = wiredata.wires[i].afwire.positionx
                af_y = wiredata.wires[i].afwire.positiony
                af_yaw = wiredata.wires[i].afwire.yaw
                af_pitch = wiredata.wires[i].afwire.pitch
                af_name = wiredata.wires[i].afwire.name.upper()

                fpw_index = wiredata.wires[i].fpwwire.index
                fpw_x = wiredata.wires[i].fpwwire.positionx
                fpw_y = wiredata.wires[i].fpwwire.positiony
                fpw_yaw = wiredata.wires[i].fpwwire.yaw
                fpw_pitch = wiredata.wires[i].fpwwire.pitch
                fpw_name = wiredata.wires[i].fpwwire.name.upper()

                stagger = wiredata.wires[i].contactwire.stagger
                contact_yaw = wiredata.wires[i].contactwire.yaw
                contact_name = wiredata.wires[i].contactwire.name
                contact_pitch = wiredata.wires[i].contactwire.pitch

                # 구문 작성
                self.lines.append(f',;{post_number}\n')
                self.lines.append(f',;-----{current_airjoint}({current_structure})({current_curve})-----\n')
                self.lines.append(f'{pos},.freeobj 0;{contact_index};{stagger};0;{contact_yaw};{contact_pitch};,;{contact_name}\n\n')
                self.lines.append(f'{pos},.freeobj 0;{af_index};{af_x};{af_y};{af_yaw};{af_pitch};,;{af_name}\n\n')
                self.lines.append(f'{pos},.freeobj 0;{fpw_index};{fpw_x};{fpw_y};{fpw_yaw};{fpw_pitch};,;{fpw_name}\n\n')
            except AttributeError as e:
                logger.warning(f"Wire 데이터 누락: index {i}, 오류: {e}")
            except Exception as e:
                logger.error(f"예상치 못한 오류: index {i}, 오류: {e}")

        logger.info(f'create_wire_csv실행이 완료됐습니다.')

    def create_csvtotxt(self):
        txthandler = TxTFileHandler()
        txthandler.save_file_dialog()  # 파일 저장 대화상자 열기
        txthandler.write_to_file(self.lines)
