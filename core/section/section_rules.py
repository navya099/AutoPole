# core/SECTION/section_rule.py

class SectionRule:
    @staticmethod
    def get_gauge(current_structure: str) -> float:
        if current_structure == '토공':
            return 3.0
        elif current_structure == '교량':
            return 3.5
        elif current_structure == '터널':
            return 2.1
        else:
            return 0.0

    @staticmethod
    def get_install_type(current_structure: str) -> str:
        if current_structure in ('토공', '교량'):
            return 'OpG'
        elif current_structure == '터널':
            return 'Tn'
        return ''
