import datetime

from geometry.alignment import BVEAlignment
from structures.structure import StructureCollection, Bridge, Tunnel, StructureFactory
from utils.Vector3 import Vector3
from utils.logger import logger
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import pandas as pd
import chardet


class BaseFileHandler:
    """파일 처리를 위한 기본 클래스 (공통 기능 포함)"""

    def __init__(self):
        self.filepath: str = ''
        self.filename: str = ''
        self.file_data: list[str] = []

    def select_file(self, title: str, file_types: list[tuple[str, str]]):
        """공통 파일 선택 메서드"""
        logger.debug(f"{title} 파일 선택 창을 엽니다.")
        root = tk.Tk()
        root.withdraw()  # Tkinter 창 숨기기
        file_path = filedialog.askopenfilename(title=title, filetypes=file_types)

        if file_path:
            self.filepath = file_path
            self.filename = os.path.basename(file_path)  # 파일명 추출
            logger.info(f"파일이 선택되었습니다: {self.filename}")
        else:
            logger.warning("파일을 선택하지 않았습니다.")

    def get_filepath(self):
        """파일 경로 반환"""
        return self.filepath

    def set_filepath(self, filepath):
        self.filepath = filepath

    def get_filename(self):
        """파일 이름 반환"""
        return self.filename

    def get_file_extension(self):
        """파일 확장자 반환"""
        if not self.filepath:
            logger.warning("파일 경로가 설정되지 않았습니다.")
            return None
        return os.path.splitext(self.filepath)[-1].lower()

    def get_file_size(self):
        """파일 크기 반환 (바이트 단위)"""
        if not self.filepath:
            logger.warning("파일 경로가 설정되지 않았습니다.")
            return None
        return os.path.getsize(self.filepath)

    def get_creation_time(self):
        """파일의 생성 날짜 반환"""
        if not self.filepath:
            logger.warning("파일 경로가 설정되지 않았습니다.")
            return None
        creation_time = os.path.getctime(self.filepath)
        return datetime.fromtimestamp(creation_time)

    def get_modification_time(self):
        """파일의 마지막 수정 날짜 반환"""
        if not self.filepath:
            logger.warning("파일 경로가 설정되지 않았습니다.")
            return None
        modification_time = os.path.getmtime(self.filepath)
        return datetime.fromtimestamp(modification_time)

    def read_file_content(self, encoding='utf-8'):
        """파일 내용 읽기"""
        if not self.filepath:
            logger.warning("파일 경로가 설정되지 않았습니다.")
            return None
        try:
            with open(self.filepath, 'r', encoding=encoding) as file:
                self.file_data = file.read()  # 파일 내용 읽기
            logger.info(f"파일 {self.filepath} 읽기 완료.")
        except Exception as e:
            logger.error(f"파일 읽기 중 오류 발생: {e}", exc_info=True)
            return None

    def get_data(self):
        #  파일 내용 반환
        return self.file_data

    def save_file_dialog(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("텍스트 파일", "*.txt"), ("모든 파일", "*.*")]
        )
        if file_path:
            self.filepath = file_path
        else:
            messagebox.showerror('에러!', '파일 경로가 설정되지 않았습니다.')
            logger.warning("파일 경로가 설정되지 않았습니다.")

    def write_to_file(self, data):
        """파일에 데이터 쓰기"""
        if not self.filepath:
            logger.warning("파일 경로가 설정되지 않았습니다.")
            return False
        try:
            with open(self.filepath, 'w', encoding='utf-8') as file:
                if isinstance(data, list):  # 리스트인지 확인
                    file.write(''.join(data))  # 리스트를 문자열로 변환 후 저장
                else:
                    file.write(data)  # 문자열이면 그대로 저장
            logger.info(f"파일에 데이터가 성공적으로 저장되었습니다.")
            return True
        except Exception as e:
            logger.error(f"파일 쓰기 중 오류 발생: {e}", exc_info=True)
            return False

    def file_exists(self):
        """파일 존재 여부 확인"""
        if not self.filepath:
            logger.warning("파일 경로가 설정되지 않았습니다.")
            return False
        return os.path.exists(self.filepath)

    def delete_file(self):
        """파일 삭제"""
        if not self.filepath:
            logger.warning("파일 경로가 설정되지 않았습니다.")
            return False
        try:
            os.remove(self.filepath)
            logger.info(f"파일이 성공적으로 삭제되었습니다: {self.filepath}")
            return True
        except Exception as e:
            logger.error(f"파일 삭제 중 오류 발생: {e}", exc_info=True)
            return False


class TxTFileHandler(BaseFileHandler):
    """
    TxTFileHandler 클래스는 BaseFileHandler클래스를 상속받아 텍스트 파일을 처리하는 기능을 제공합니다.
    이 클래스는 파일을 선택하고, 인코딩을 자동으로 감지한 후 파일을 읽거나,
    특정 구간 데이터를 찾아 반환하는 메소드를 포함합니다.
    """

    def __init__(self):
        """TxTFileHandler 객체를 초기화합니다."""
        super().__init__()
        self.file_data: list[str] = []  # 텍스트 리스트

        logger.debug("TxTFileHandler 객체가 초기화되었습니다.")

    def process_file(self):
        """파일을 선택하고 읽고 인코딩을 감지하여 데이터를 반환하는 통합 프로세스"""
        logger.info("파일 선택을 시작합니다.")
        super().select_file("TXT 파일 선택", [("Text files", "*.txt"), ("All files", "*.*")])  # 파일 선택후 filepath저장

        if not self.filepath:
            logger.warning("파일을 선택하지 않았습니다.")
            return []  # 파일을 선택하지 않은 경우
        try:
            encoding = self.detect_encoding(self.filepath)
            logger.info(f"인코딩 감지: {encoding}")

            self.read_file_content(encoding)  # 파일 읽기
            super().get_data()
        except Exception as e:
            logger.error(f"파일 처리 중 오류 발생: {e}", exc_info=True)
            return []

    def process_info(self, bvealignment: BVEAlignment, columns: list[str] = None,
                     delimiter: str = ',', mode: str = 'curve') -> BVEAlignment:
        if not self.filepath:
            logger.warning("파일 경로가 설정되지 않았습니다.")
            return bvealignment

        if mode == 'curve':
            return self._process_curve_info(bvealignment, columns, delimiter)
        elif mode == 'pitch':
            return self._process_pitch_info(bvealignment, columns, delimiter)
        else:
            logger.warning(f"지원하지 않는 모드: {mode}")
            return bvealignment

    def _process_curve_info(self, bvealignment: BVEAlignment, columns: list[str], delimiter: str) -> BVEAlignment:
        if columns is None:
            columns = ['sta', 'radius', 'cant']

        try:
            df = pd.read_csv(self.filepath, sep=delimiter, header=None, names=columns)
        except Exception as e:
            logger.error(f"곡선 파일 읽기 오류: {e}", exc_info=True)
            return bvealignment

        from geometry.alignment import Curve
        for _, row in df.iterrows():
            curve = Curve()
            curve.startsta = float(row['sta'])
            curve.radius = float(row['radius'])
            curve.cant = float(row['cant'])
            bvealignment.curves.append(curve)

        logger.info(f"곡선 데이터 {len(bvealignment.curves)}개 로드 완료")
        return bvealignment

    def _process_pitch_info(self, bvealignment: BVEAlignment, columns: list[str], delimiter: str) -> BVEAlignment:
        if columns is None:
            columns = ['sta', 'pitch']

        try:
            df = pd.read_csv(self.filepath, sep=delimiter, header=None, names=columns)
        except Exception as e:
            logger.error(f"종단기울기 파일 읽기 오류: {e}", exc_info=True)
            return bvealignment

        from geometry.alignment import Pitch
        for _, row in df.iterrows():
            pitch = Pitch()
            pitch.startsta = float(row['sta'])
            pitch.pitch = float(row['pitch'])
            bvealignment.pitchs.append(pitch)

        logger.info(f"기울기 데이터 {len(bvealignment.pitchs)}개 로드 완료")
        return bvealignment

    def read_file_content(self, encoding='utf-8'):
        """파일을 실제로 읽고 데이터를 처리하는 메소드(부모 메소드오버라이딩"""
        super().read_file_content()

        if self.file_data is not None:
            self.file_data = self.file_data.splitlines()  # 줄 단위로 리스트 생성

            logger.info(f"파일 {self.filepath} 읽기 완료.")
        else:
            logger.warning("파일을 읽을 수 없습니다.")
            return []

    @staticmethod
    def detect_encoding(file_path):
        """파일의 인코딩을 자동 감지하는 함수"""
        logger.debug(f"파일 {file_path}의 인코딩을 감지합니다.")
        try:
            with open(file_path, "rb") as f:
                raw_data = f.read()
                detected = chardet.detect(raw_data)
                encoding = detected["encoding"]
                if encoding is None:
                    logger.error("파일 인코딩을 감지할 수 없습니다.")
                    return None
                logger.info(f"감지된 인코딩: {encoding}")
                return encoding
        except Exception as e:
            logger.error(f"인코딩 감지 중 오류 발생: {e}")
            return None

    @staticmethod
    def get_column_count(lst):
        """파일에서 최대 열 갯수를 추출하는 함수"""
        max_columns = 0
        for line in lst:
            try:
                parts = line.split(',')
                max_columns = max(max_columns, len(parts))
            except Exception as e:
                logger.error(f"오류 발생: {e}")
        logger.info(f"최대 열 갯수: {max_columns}")
        return max_columns


class PolylineHandler(TxTFileHandler):
    """
    폴리라인 좌표 생성 클래스 TxTFileHandler 상속
    """

    def __init__(self):
        super().__init__()

    def load_polyline(self):
        super().select_file("bve좌표 파일 선택", [("txt files", "*.txt"), ("All files", "*.*")])

    def convert_txt_to_polyline(self, bvealignment: BVEAlignment) -> BVEAlignment:
        """3D 좌표를 읽어와 BVEAlignment 객체에 추가합니다."""
        super().read_file_content()

        for line in self.file_data:
            parts = line.strip().split(',')
            if len(parts) != 3:
                logger.warning(f"좌표가 3개가 아닙니다: {line.strip()}")
                continue
            try:
                x, y, z = map(float, parts)
                bvealignment.coords.append(Vector3(x, y, z))
            except ValueError:
                logger.warning(f"잘못된 형식의 데이터가 발견되었습니다: {line.strip()}")
        logger.info(f"좌표 데이터 {len(bvealignment.coords)}개 로드 완료")
        return bvealignment


class ExcelFileHandler(BaseFileHandler):
    """
    ExcelFileHandler 클래스는 BaseFileHandler 클래스를 상속받아 엑셀 파일을 처리하는 기능을 제공합니다.
    이 클래스는 파일을 선택하고, 파일을 읽거나, 특정 구간 데이터를 찾아 반환하는 메소드를 포함합니다.
    """

    def __init__(self):
        super().__init__()
        self.excel_BRIDGE_Data = None
        self.excel_TUNNEL_Data = None
        logger.debug("ExcelFileHandler 객체가 초기화되었습니다.")

    def load_excel(self):
        """엑셀 파일을 선택하는 메소드"""
        super().select_file("엑셀 파일 선택", [("EXCEL files", "*.xlsx"), ("All files", "*.*")])

    def read_excel(self):
        """엑셀 파일을 읽는 메소드"""
        if not self.filepath:
            logger.warning("엑셀 파일 경로가 설정되지 않았습니다.")
            return None

        try:
            # 첫 번째 열만 str 형식으로, 나머지는 자동 형식
            dtype_dict = {0: str}  # 첫 번째 열만 str로 설정 (0번째 인덱스 열)
            # xlsx 파일 읽기
            self.excel_BRIDGE_Data = pd.read_excel(self.filepath, sheet_name='교량', header=None,
                                                   dtype=dtype_dict)  # 첫 번째 행을 헤더로 사용
            self.excel_TUNNEL_Data = pd.read_excel(self.filepath, sheet_name='터널', header=None, dtype=dtype_dict)
            logger.info("엑셀 파일이 성공적으로 읽혔습니다.")
        except FileNotFoundError:
            logger.error(f"엑셀 파일을 찾을 수 없습니다: {self.filepath}")
            return None
        except ValueError as e:
            logger.error(f"엑셀 파일 처리 중 오류가 발생했습니다: {e}")
            return None
        except Exception as e:
            logger.error(f"알 수 없는 오류 발생: {e}", exc_info=True)
            return None

    def process_structure_data(self, structures: StructureCollection) -> StructureCollection:
        """교량과 터널 구간 정보를 처리하는 메소드"""
        self.read_excel()

        if self.excel_BRIDGE_Data is None or self.excel_TUNNEL_Data is None:
            logger.warning("엑셀 데이터가 로드되지 않았습니다.")
            return structures

        # 첫 번째 행을 열 제목으로 설정
        self.excel_BRIDGE_Data.columns = ['br_NAME', 'br_START_STA', 'br_END_STA', 'br_LENGTH']
        self.excel_TUNNEL_Data.columns = ['tn_NAME', 'tn_START_STA', 'tn_END_STA', 'tn_LENGTH']

        try:
            for _, row in self.excel_BRIDGE_Data.iterrows():
                s = StructureFactory.create_structure(
                    structuretype='교량',
                    name=row['br_NAME'],
                    startsta=row['br_START_STA'],
                    endsta=row['br_END_STA']
                )
                structures.append(s)

            for _, row in self.excel_TUNNEL_Data.iterrows():
                s = StructureFactory.create_structure(
                    structuretype='터널',
                    name=row['tn_NAME'],
                    startsta=row['tn_START_STA'],
                    endsta=row['tn_END_STA']
                )
                structures.append(s)
        except Exception as e:
            logger.error(f"구조 데이터 처리 중 오류 발생: {e}", exc_info=True)
            return structures

        return structures


def buffered_write(filename, lines):
    """파일 쓰기 버퍼 함수"""
    filename = "C:/TEMP/" + filename
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(lines)


class ObjectSaver:
    def __init__(self, obj):
        """객체를 받아 속성을 저장할 준비를 함"""
        self.obj = obj

    def save_to_txt(self, filename):
        """객체의 속성을 텍스트 파일로 저장"""
        with open(filename, 'w', encoding='utf-8') as file:
            for attr, value in self.obj.__dict__.items():
                file.write(f'{attr}: {value}\n')

    def save_to_json(self, filename):
        """객체의 속성을 JSON 파일로 저장"""
        import json
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.obj.__dict__, file, indent=4, ensure_ascii=False)

    def save_to_pickle(self, filename):
        """객체를 pickle 파일로 저장"""
        import pickle
        with open(filename, 'wb') as file:
            pickle.dump(self.obj, file)


class DxfFileHandler(BaseFileHandler):
    """DXF 파일 저장을 위한 핸들러"""

    def save_file_dialog(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".dxf",
            filetypes=[("DXF 파일", "*.dxf"), ("모든 파일", "*.*")]
        )
        if file_path:
            self.filepath = file_path
        else:
            messagebox.showerror('에러!', '파일 경로가 설정되지 않았습니다.')
            logger.warning("파일 경로가 설정되지 않았습니다.")
