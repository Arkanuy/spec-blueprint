"""Exception domain aplikasi kasir.

Setiap pelanggaran aturan bisnis (BR-001..BR-010) atau kegagalan requirement
(FR-xxx) dilempar sebagai :class:`KesalahanAturan` dari lapisan ``layanan``.
Lapisan CLI menangkapnya, menulis pesan ke ``stderr``, lalu mengembalikan kode
keluar 1 (lihat kontrak CLI). Memisahkan exception ini dari ``sqlite3.Error``
membuat aturan bisnis bisa diuji tanpa menyentuh CLI.
"""


class KesalahanAturan(Exception):
    """Pelanggaran aturan bisnis yang harus diberitahukan ke kasir.

    Pesan wajib ditulis dalam Bahasa Indonesia dan menyebut **apa yang salah**
    sekaligus **apa yang harus dilakukan** (NFR-003), karena pengguna adalah
    kasir, bukan orang teknis.
    """

    def __init__(self, pesan: str) -> None:
        super().__init__(pesan)
        self.pesan = pesan

    def __str__(self) -> str:  # pragma: no cover - dipakai saat debugging
        return self.pesan