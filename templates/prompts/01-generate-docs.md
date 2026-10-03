# Prompt 01 — Membuat Dokumen dari Ide Mentah

> Pakai prompt ini saat kamu punya ide proyek tapi belum punya dokumen apa pun. Tujuannya: mengubah ide samar menjadi `00-discovery.md` dan `01-prd.md` yang jujur — termasuk mengakui apa yang belum diketahui.

---

## Cara pakai

1. Buka agen AI dengan akses ke folder proyekmu (yang sudah berisi template `docs/`).
2. Salin prompt di bawah, ganti bagian `[ ]` dengan informasi proyekmu. Kalau ada bagian yang belum kamu tahu, tulis "belum tahu" — jangan diisi karangan.
3. Periksa hasilnya. Bagian yang tanda `[butuh konfirmasi]` wajib kamu jawab sebelum lanjut.

---

## Prompt

```
Kamu bertindak sebagai business analyst. Tugasmu: mengubah ide proyek mentah di bawah
menjadi dua dokumen: docs/00-discovery.md dan docs/01-prd.md, mengikuti struktur yang
sudah ada di file template tersebut.

KONTEKS PROYEK
- Ide/masalah awal: [tulis masalahnya, bukan fitur yang diinginkan]
- Siapa yang mengalami masalah ini: [peran/orang nyata]
- Bagaimana prosesnya berjalan sekarang: [alat, cara kerja, langkahnya]
- Perusahaan/organisasi: [nama, bidang, skala]
- Yang saya bayangkan dibangun: [kalau ada]
- Tenggat/waktu tersedia: [kalau ada]
- Kemampuan teknis saya: [rendah/menengah/tinggi]
- Anggaran: [kalau ada]

ATURAN KERJA
1. Jangan mengarang data. Angka yang tidak saya sebutkan harus ditulis "[butuh data]".
2. Pisahkan dengan tegas: FAKTA (yang saya sebutkan), ASUMSI (yang kamu simpulkan,
   tandai jelas), dan PERTANYAAN (yang harus saya jawab).
3. Untuk bagian pohon masalah (5 Whys), turunkan sampai akar yang benar-benar bisa
   diperbaiki. Jangan berhenti di gejala.
4. Di bagian evaluasi alternatif solusi, WAJIB sertakan minimal tiga opsi termasuk
   "perbaikan proses tanpa sistem" dan "spreadsheet terstruktur". Jangan langsung
   menyimpulkan bahwa sistem adalah jawabannya.
5. Untuk setiap fitur di PRD, isi kolom "alasan" dengan masalah nyata yang diselesaikan.
   Kalau alasannya hanya "supaya lengkap", hapus fiturnya.
6. Nyatakan OUT OF SCOPE secara eksplisit, termasuk hal-hal yang biasanya otomatis
   dianggap ada (login, notifikasi, aplikasi mobile, integrasi pembayaran).
7. Setiap pertanyaan yang belum bisa kamu jawab: tulis di PRD bagian "Pertanyaan terbuka"
   dengan nomor Q-xx, dan pindahkan ke docs/09-risks.md.

LANGKAH
1. Tulis docs/00-discovery.md lengkap (semua bagian terisi atau bertanda "[butuh data]").
2. Tulis docs/01-prd.md lengkap.
3. Di akhir jawabanmu, tampilkan daftar:
   - Keputusan yang kamu ambil sendiri (agar saya bisa mengoreksi)
   - Pertanyaan yang harus saya jawab sebelum dokumen ini dianggap sah
   - Bagian yang paling berisiko jika asumsinya salah

Jangan lompat ke dokumen lain (requirements, architecture, dsb). Selesaikan dua dokumen itu
dulu dan tunggu koreksi saya.
```

---

## Yang harus diperiksa setelah AI menjawab

- [ ] AI tidak mengarang angka volume transaksi / jumlah pengguna / pendapatan
- [ ] Akar masalah terasa masuk akal dan benar-benar bisa diperbaiki
- [ ] Ada minimal tiga alternatif solusi, bukan langsung aplikasi
- [ ] Fitur di PRD punya alasan yang bisa dilacak ke masalah
- [ ] Out of scope ditulis eksplisit
- [ ] Ada daftar pertanyaan terbuka, bukan pura-pura semua sudah jelas

Kalau AI menjawab dengan terlalu yakin padahal informasi kurang, minta dia menyebut ulang mana yang fakta dan mana yang asumsi.
