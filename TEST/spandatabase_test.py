from config.spandatabase import SpanDatabase

# 테스트할 속도
speed = 150
db = SpanDatabase(speed)

# JSON에 있는 구조물과 와이어 타입을 미리 하드코딩할 수도 있지만,
# 안전하게 get_offset/Key 확인으로 자동 탐색
structures = ['토공', '교량', '터널']
wire_types = ['contact', 'af', 'fpw']
span_lengths = [45, 50, 55, 60]

print(f"=== SpanDatabase 테스트 (속도 {speed}) ===\n")

for struct in structures:
    print(f"구조물: {struct}")
    for wire in wire_types:
        for span in span_lengths:
            idx = db.get_span_index(structure=struct, wire_type=wire, span_length=span)
            print(f"  와이어: {wire}, 경간: {span}m → 스팬 인덱스: {idx}")
    print()
