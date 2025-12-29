from mast_material import MastMaterial

HBEAM_MASTS: dict[int, MastMaterial] = {
    619: MastMaterial(
        code=619,
        name="H형주 토공용",
        type="hbeam",
        length=9.0,
        width= 208,
        height= 202
    ),
    620: MastMaterial(
        code=620,
        name="H형주 토공용",
        type="hbeam",
        length= 9.0,
        width= 250,
        height= 255
    ),
    621: MastMaterial(
            code=621,
            name="터널하수강",
            type="tunnel",
            length= 9.0,
            width= 250,
            height= 255
    ),
}