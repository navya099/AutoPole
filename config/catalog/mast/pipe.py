from mast_material import MastMaterial

PIPE_MASTS: dict[int, MastMaterial] = {
    1370: MastMaterial(
        code=1370,
        name="강관주 토공용",
        type="pipe",
        length=9.0,
        diameter=267.5
    ),
    1376: MastMaterial(
        code=1376,
        name="강관주 교량용",
        type="pipe",
        length=8.5,
        diameter=313.0
    ),
    1400: MastMaterial(
        code=1400,
        name="터널 하수강",
        type="pipe",
        length=0.0,
        diameter=0.0
    ),
}