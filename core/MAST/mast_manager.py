from core.base_manager import BaseManager


class MastManager(BaseManager):
    """전주(Mast) 데이터를 설정하는 클래스"""

    def __init__(self, dataloader, poledata):
        super().__init__(dataloader, poledata)

    def run(self):
        self.create_mast()

    def create_mast(self):
        data = self.poledata
        for i in range(len(data.poles)):
            try:
                current_structure = data.poles[i].current_structure
                mast_index, mast_name = get_mast_type(self.loader.databudle.designspeed, current_structure)
                data.poles[i].mast.name = mast_name
                data.poles[i].mast.index = mast_index
                data.poles[i].mast.direction = data.poles[i].Brackets[0].direction

            except Exception as ex:
                error_message = (
                    f"예외 발생 in create_mast!\n"
                    f"인덱스: {i}\n"
                    f"예외 종류: {type(ex).__name__}\n"
                    f"예외 메시지: {ex}\n"
                    f"전체 트레이스백:\n{traceback.format_exc()}"
                )
                logger.error(error_message)
                continue