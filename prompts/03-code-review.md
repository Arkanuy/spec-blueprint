# Prompt 03 — Review Kode Hasil AI

> Dipakai saat kamu ingin memeriksa hasil kode — milikmu sendiri atau dari agen lain. Fokusnya bukan gaya kode, tapi **kesesuaian dengan requirement, penanganan kegagalan, dan keamanan.** Ini yang paling sering lolos saat vibecoding.

---

## Prompt

```
Kamu bertindak sebagai reviewer. Periksa kode berikut terhadap dokumen spec, BUKAN terhadap
selera pribadi.

KONTEKS
- Fitur: [F-xx]
- FR terkait: [FR-xxx]
- Dokumen acuan: AGENTS.md, docs/02-requirements.md, docs/03-architecture.md,
  docs/05-data-model.md, docs/06-ui-ux.md, docs/07-test-plan.md
- Kode yang direview: [tempel kode / sebutkan file dan kamu baca sendiri]

URUTAN PEMERIKSAAN (kerjakan berurutan, jangan lompat)

1. KESESUAIAN FUNCTIONAL
   - Apakah setiap FR yang disebut terpenuhi?
   - Apakah ada perilaku yang menyimpang dari kriteria penerimaan (AC)?
   - Apakah ada fitur tambahan yang tidak diminta? (ini pelanggaran, bukan bonus)

2. ATURAN BISNIS
   - Apakah setiap BR-xxx yang relevan ditegakkan di kode?
   - Di lapisan mana ditegakkan — server atau hanya tampilan? (hanya tampilan = TEMUAN)

3. PENANGANAN KEGAGALAN
   - Status kosong: apakah ada, dan pesannya jelas?
   - Status memuat: apakah ada?
   - Status error: apakah ada, dan apakah pengguna bisa memulihkan?
   - Input tidak valid: apakah ditolak dengan pesan yang menyebut field-nya?
   - Data ganda / bentrok: apakah ditangani?
   - Aksi ganda cepat (klik dua kali): apakah aman?

4. KEAMANAN
   - Hak akses diperiksa di server? (bukan hanya menyembunyikan tombol)
   - Ada kredensial/rahasia di kode? (ini TEMUAN Kritis)
   - Input pengguna dipakai langsung di query/perintah? (risiko injeksi)
   - Data sensitif bocor ke log atau ke respons API?
   - Pesan error membocorkan detail teknis (stack trace, struktur tabel)?

5. KONSISTENSI DATA
   - Apakah perubahan mengikuti model di docs/05-data-model.md?
   - Apakah integritas dijaga (transaksi DB untuk operasi berantai)?
   - Apakah operasi berulang aman (idempoten)?
   - Apakah data transaksi diarsipkan, bukan dihapus mentah?

6. KETERAWATAN
   - Apakah ada duplikasi yang seharusnya disatukan?
   - Apakah ada fungsi yang mengerjakan terlalu banyak hal?
   - Apakah penamaan menunjukkan maksudnya?
   - Apakah ada kode mati / tidak dipakai?
   - Apakah error tertelan diam-diam (catch tanpa tindakan)?

7. KONSISTENSI DOKUMEN
   - Apakah kode berbeda dari dokumen? Jika ya, mana yang benar?
     (dokumen harus diperbarui, atau kode harus diperbaiki — tentukan dan jelaskan)

FORMAT TEMUAN (urutan dari yang paling berat)
[KEPARAHAN] file:baris — [temuan]
  Kenapa ini masalah : [dampak nyata, bukan teori]
  Bukti              : [kutipan kode]
  Perbaikan          : [langkah konkret]

KEPARAHAN
- Kritis  : data salah/hilang, keamanan bocor, alur utama tidak jalan
- Tinggi  : perilaku menyimpang dari FR, kasus gagal tidak ditangani
- Sedang  : masalah keterawatan, duplikasi, error ditelan
- Rendah  : gaya, penamaan, tata letak

ATURAN
1. Jangan mengomentari hal di luar dokumen acuan. Kalau tidak ada di dokumen, bukan temuan —
   tulis sebagai "usulan", di bagian terpisah.
2. Setiap temuan wajib punya bukti berupa kutipan kode. Tanpa bukti, jangan diangkat.
3. Jangan menulis ulang seluruh kode. Cukup tunjukkan perbaikannya.
4. Kalau tidak ada temuan, katakan terus terang. Jangan mencari-cari masalah agar terlihat teliti.
```

---

## Cara memakai hasil review

1. Perbaiki dulu semua temuan **Kritis** dan **Tinggi**. Jangan lanjut ke fitur berikutnya sebelum ini bersih.
2. Temuan **Sedang**: masukkan ke `docs/03-architecture.md` bagian "utang teknis" dengan tanggal.
3. Temuan **Rendah** dan usulan: masukkan ke "ide tunda" kalau layak, kalau tidak — abaikan.
4. Kalau reviewer menemukan kode berbeda dari dokumen, **putuskan mana yang benar** dan perbarui yang salah. Jangan biarkan keduanya berbeda.

---

## Review cepat (kalau waktu terbatas)

Kalau hanya punya beberapa menit, periksa lima hal ini saja — ini yang paling sering menyebabkan masalah nyata:

1. Ada kredensial tertulis di kode?
2. Hak akses diperiksa di server?
3. Operasi tulis dibungkus transaksi database?
4. Status error ditangani, dan pengguna diberi jalan keluar?
5. Ada bukti uji, atau hanya klaim?
