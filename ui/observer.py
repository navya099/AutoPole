class ResultSubject:
    """결과 데이터를 관리하고 관찰자에게 알리는 Subject"""
    def __init__(self):
        self._observers = []
        self._result = None

    def attach(self, observer):
        """관찰자 등록"""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        """관찰자 해제"""
        if observer in self._observers:
            self._observers.remove(observer)

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        """결과 변경 시 자동 알림"""
        self._result = value
        self._notify()

    def _notify(self):
        for obs in self._observers:
            obs.update(self._result)  # Observer 인터페이스 호출
