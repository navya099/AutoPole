import pandas as pd

from core.POLE.polepositionset import PolePositionSet
from fileio.fileloader import TxTFileHandler

class PoleFileSource:
    def load(self) -> PolePositionSet:
        handler = TxTFileHandler()
        handler.select_file(
            "미리 정의된 전주 파일 선택",
            [("txt files", "*.txt"), ("All files", "*.*")]
        )

        df = pd.read_csv(
            handler.get_filepath(),
            sep=",",
            header=0,
            names=['측점', '전주번호', '타입', '에어조인트']
        )

        return PolePositionSet(
            positions=df['측점'].tolist(),
            airjoints=[
                (row['측점'], row['에어조인트'])
                for _, row in df.iterrows()
                if row['에어조인트'] != '일반개소'
            ]
        )
