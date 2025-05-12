from .fileloader import *


class BVECSV:
    def __init__(self, poledata=None, wiredata=None):
        self.poledata = poledata  # ✅ PoleDATAManager.poledata 인스턴스를 가져옴
        self.wiredata = wiredata
        self.lines = []

    def create_pole_csv(self):
        self.lines.append(',;전주구문\n')
        data = self.poledata
        for i in range(len(data.poles) - 1):
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
            pitch = 0 if direction == 'L' else 180

            # 구문 작성
            self.lines.append(f',;{post_number}\n')
            self.lines.append(f',;-----{current_airjoint}({current_structure})({current_curve})-----\n')
            self.lines.append(f'{pos},.freeobj 0;{mastindex};{gauge},;{mastname}\n')
            self.lines.append(f'{pos},.freeobj 0;{bracketindex};0;0;{pitch};,;{bracketname}\n\n')
            self.lines.append(f'{pos},.freeobj 0;{feederindex};{gauge};0;{pitch};,;{feedername}\n\n')

    def create_wire_csv(self):
        self.lines = []  # 코드 실행전 초기화
        self.lines.append(',;전차선구문\n')
        data = self.poledata
        wiredata = self.wiredata
        for i in range(len(data.poles) - 1):
            pos = data.poles[i].pos
            post_number = data.poles[i].post_number
            current_airjoint = data.poles[i].current_airjoint
            current_structure = data.poles[i].current_structure
            current_curve = data.poles[i].current_curve
            contact_index = wiredata.wires[i].contactwire.index
            af_index = wiredata.wires[i].afwire.index
            af_x = wiredata.wires[i].afwire.positionx
            af_y = wiredata.wires[i].afwire.positiony
            af_yaw = wiredata.wires[i].afwire.xyangle
            af_pitch = wiredata.wires[i].afwire.yzangle
            af_name = wiredata.wires[i].afwire.name.upper()

            fpw_index = wiredata.wires[i].fpwwire.index
            fpw_x = wiredata.wires[i].fpwwire.positionx
            fpw_y = wiredata.wires[i].fpwwire.positiony
            fpw_yaw = wiredata.wires[i].fpwwire.xyangle
            fpw_pitch = wiredata.wires[i].fpwwire.yzangle
            fpw_name = wiredata.wires[i].fpwwire.name.upper()

            stagger = wiredata.wires[i].contactwire.stagger
            pitch = wiredata.wires[i].contactwire.xyangle
            name = wiredata.wires[i].contactwire.name
            roll = wiredata.wires[i].contactwire.yzangle

            # 구문 작성
            self.lines.append(f',;{post_number}\n')
            self.lines.append(f',;-----{current_airjoint}({current_structure})({current_curve})-----\n')
            self.lines.append(f'{pos},.freeobj 0;{contact_index};{stagger};0;{pitch};{roll};,;{name}\n\n')
            self.lines.append(f'{pos},.freeobj 0;{af_index};{af_x};{af_y};{af_yaw};{af_pitch};,;{af_name}\n\n')
            self.lines.append(f'{pos},.freeobj 0;{fpw_index};{fpw_x};{fpw_y};{fpw_yaw};{fpw_pitch};,;{fpw_name}\n\n')

    def create_csvtotxt(self):
        txthandler = TxTFileHandler()
        txthandler.save_file_dialog()  # 파일 저장 대화상자 열기
        txthandler.write_to_file(self.lines)
