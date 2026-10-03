# Gate 2 — Pemeriksaan per Fitur Selesai

> Dijalankan **setiap kali satu fitur selesai** dikerjakan AI. Ringan, tapi wajib. Melewatkan langkah ini adalah penyebab utama utang teknis menumpuk di proyek vibecoding.

**Fitur:** [F-xx — nama fitur]
**FR terkait:** [FR-xxx]
**Tanggal:** _______
**Diperiksa oleh:** _______

---

## A. Kesesuaian

- [ ] Perilaku sesuai dengan FR dan kriteria penerimaan
- [ ] Tidak ada fitur tambahan yang tidak diminta
- [ ] Tidak ada file di luar lingkup yang diubah
- [ ] Aturan bisnis (BR) yang relevan sudah ditegakkan
- [ ] Hasilnya benar-benar menyelesaikan tujuan fitur ini, bukan hanya "kodenya jalan"

## B. Status gagal

- [ ] **Kosong** — belum ada data: ada pesan yang jelas, bukan layar putih atau error
- [ ] **Kosong karena filter** — pencarian tanpa hasil: ada pesan berbeda dari "belum ada data"
- [ ] **Memuat** — ada indikator saat data sedang diambil
- [ ] **Gagal validasi** — input salah ditolak dengan pesan yang menyebut kolomnya
- [ ] **Gagal sistem** — server/DB gagal: ada pesan yang bisa dimengerti dan jalan untuk mencoba lagi
- [ ] **Tidak punya akses** — peran yang tidak diizinkan dapat pesan yang jelas
- [ ] **Aksi ganda** — klik dua kali tidak menciptakan data ganda

## C. Keamanan

- [ ] Hak akses diperiksa di server, bukan hanya disembunyikan di tampilan
- [ ] Tidak ada kredensial/kunci API tertulis di kode
- [ ] Input pengguna tidak dipakai langsung di query/perintah
- [ ] Data sensitif tidak muncul di log
- [ ] Pesan error tidak membocorkan detail teknis (stack trace, nama tabel)

## D. Data

- [ ] Perubahan mengikuti model di `05-data-model.md`
- [ ] Operasi berantai dibungkus transaksi database (tidak ada data setengah jadi)
- [ ] Operasi tulis aman kalau dijalankan dua kali (idempoten)
- [ ] Data transaksi diarsipkan, bukan dihapus permanen
- [ ] Kalau ada perubahan skema: migrasi sudah dibuat dan dijalankan

## E. Uji

- [ ] Kasus uji terkait (TC-xxx) dijalankan
- [ ] Bukti uji ada (keluaran perintah, log, tangkapan layar) — bukan klaim
- [ ] Alur normal diuji dari awal sampai akhir
- [ ] Minimal satu alur gagal diuji
- [ ] Tidak ada error baru di log saat alur dijalankan
- [ ] Statusnya ditulis jujur — kalau belum diuji, tulis "belum diuji"

## F. Keterawatan

- [ ] Tidak ada kode duplikat yang seharusnya disatukan
- [ ] Tidak ada fungsi yang mengerjakan terlalu banyak hal
- [ ] Tidak ada kode mati atau tidak terpakai
- [ ] Tidak ada error yang ditelan diam-diam
- [ ] Penamaan menunjukkan maksudnya

## G. Dokumentasi

- [ ] Dokumen yang terpengaruh sudah diperbarui (sebutkan yang mana)
- [ ] Kalau ada keputusan teknis penting: sudah dicatat di `10-decisions.md`
- [ ] Kalau ada hal yang ditunda: sudah masuk `08-roadmap.md` bagian "ditunda"
- [ ] Kalau ada temuan/jebakan baru: sudah masuk `AGENTS.md` bagian jebakan

---

## Hasil

**Kesimpulan:** Selesai / Perlu perbaikan

**Temuan yang harus diperbaiki sebelum lanjut:**

| # | Temuan | Keparahan | Tindakan |
|---|---|---|---|
| 1 | | Kritis/Tinggi | |

Aturan: **temuan Kritis dan Tinggi wajib diperbaiki sebelum mengerjakan fitur berikutnya.** Temuan Sedang dan Rendah boleh masuk daftar utang teknis, tapi harus ada tanggal.

---

## Catatan untuk fitur berikutnya

Berdasarkan apa yang ditemukan saat mengerjakan fitur ini, hal apa yang perlu diperhatikan di fitur selanjutnya?

- [catatan]

Hal ini juga berguna dimasukkan ke `AGENTS.md` bagian "jebakan yang sering terjadi" agar agen berikutnya tidak mengulangi kesalahan yang sama.
