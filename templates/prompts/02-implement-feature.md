# Prompt 02 — Implementasi Satu Fitur

> Prompt inti untuk fase vibecoding. Kuncinya: **satu fitur per sesi**, lingkup dikunci, bukti uji diminta di akhir. Ini yang mencegah AI melebar dan membuat kode yang tidak bisa dilacak.

---

## Cara pakai

1. Pastikan fitur yang mau dikerjakan sudah punya `FR-xxx` di `docs/02-requirements.md`. Kalau belum, buat requirement-nya dulu — jangan lanjut.
2. Salin prompt ini, ganti `[F-xx]` dengan fitur yang dimaksud.
3. Jangan menambahkan permintaan lain di sesi yang sama.

---

## Prompt

```
Baca dulu file-file ini sebelum menulis kode apa pun:
- AGENTS.md (aturan kerja wajib)
- docs/02-requirements.md (FR, NFR, BR yang mengikat)
- docs/03-architecture.md (susunan komponen, struktur folder, otorisasi)
- docs/05-data-model.md (entitas, field, aturan integritas)
- docs/06-ui-ux.md (layar, elemen, semua status)
- docs/07-test-plan.md (kasus uji terkait)

TUGAS
Implementasikan fitur [F-xx] sesuai dokumen di atas.

LINGKUP
- FR yang harus dipenuhi: [FR-xxx, FR-xxx]
- Kriteria penerimaan: [AC-xxx]
- Aturan bisnis yang harus ditegakkan: [BR-xxx]
- Layar terkait: [S-xx]
- Kasus uji yang harus lulus: [TC-xxx]

ATURAN KERJA
1. Kerjakan HANYA fitur ini. Jangan memperbaiki, menata ulang, atau menambah hal lain
   walaupun menurutmu perlu. Catat temuanmu di bagian akhir laporan, bukan di kode.
2. Jangan membuat file baru kalau file yang ada bisa dipakai.
3. Jangan mengubah skema database tanpa membuat migrasi.
4. Jangan menambah library/paket baru. Kalau memang tidak bisa dihindari, STOP dan tanyakan
   dulu dengan menyebutkan: nama paket, alasan, ukuran, dan alternatif tanpa paket.
5. Tegakkan aturan bisnis (BR) di lapisan server/logika, bukan hanya di tampilan.
6. Tangani ketiga status wajib: kosong (belum ada data), memuat, dan gagal (error).
   Sertakan pesan error yang bisa dimengerti pengguna, bukan pesan teknis mentah.
7. Validasi input di batas sistem dengan pesan yang menyebut field bermasalah.
8. Pemeriksaan hak akses diletakkan di server.
9. Jangan menuliskan kredensial/kunci API ke dalam kode. Gunakan variabel lingkungan.
10. Ikuti konvensi penamaan dan struktur folder yang sudah ada di repo.

LANGKAH KERJA
1. BACA — baca file di atas, lalu ringkas dalam ≤5 baris: apa yang harus dicapai fitur ini.
2. RENCANA — sebutkan file yang akan kamu sentuh dan perubahan apa di masing-masing.
   Tunggu konfirmasi saya sebelum menulis kode.
   (Kalau saya sudah bilang "lanjut", lewati langkah ini.)
3. KERJAKAN — implementasi sesuai rencana.
4. UJI — jalankan [TC-xxx]. Tunjukkan keluaran perintahnya yang nyata.
5. LAPOR — pakai format laporan di bawah.

FORMAT LAPORAN (wajib, jangan diringkas jadi paragraf bebas)
Tugas      : [fitur yang dikerjakan]
FR terkait : [daftar]
File       : [daftar file yang diubah/dibuat]
Uji        : [TC-xxx] lulus/gagal + bukti (keluaran perintah atau log)
Status     : kosong / memuat / error sudah ditangani? [ya/tidak, jelaskan singkat]
Hak akses  : [di mana diperiksa]
Belum      : [yang sengaja tidak dikerjakan]
Temuan     : [hal lain yang kamu lihat tapi tidak kamu ubah]
Risiko     : [yang perlu saya perhatikan]
Dokumen    : [dokumen yang perlu diperbarui karena perubahan ini]

PENTING
- Jangan menulis "seharusnya jalan" atau "mestinya berfungsi". Kalau belum dijalankan,
  tulis "BELUM DIUJI".
- Kalau ada informasi yang kurang, berhenti dan tanya. Jangan menebak aturan bisnis.
- Kalau menemukan bahwa requirement-nya bertentangan, berhenti dan tunjukkan pertentangannya.
```

---

## Setelah AI menjawab

Periksa hal-hal ini sebelum menerima hasilnya:

- [ ] File yang disentuh sesuai rencana, tidak lebih
- [ ] Tidak ada fitur tambahan yang tidak diminta
- [ ] Ada bukti uji nyata (keluaran perintah, bukan klaim)
- [ ] Status kosong / memuat / error benar-benar ditangani, bukan hanya disebut
- [ ] Aturan bisnis ditegakkan di server
- [ ] Tidak ada kredensial di kode
- [ ] Laporan menunjukkan hal yang belum dikerjakan secara jujur

Kalau AI menulis "sudah selesai" tanpa bukti uji, minta dia menjalankan uji-nya sekarang dan menunjukkan keluarannya.

---

## Kalau hasilnya melebar

Gejala: AI menyentuh file di luar lingkup, atau menambah fitur sendiri.

Tindakan:

```
Kamu keluar dari lingkup. Batalkan perubahan pada file ini: [daftar file].
Kembalikan hanya ke perubahan yang berkaitan dengan [FR-xxx].
Temuan lain tulis di bagian "Temuan" pada laporan.
```
