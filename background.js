console.log("JS slideshow jalan!");

// Aku kasih 3 contoh gambar tema autumn, nanti tinggal ganti pakai nama file kamu (misal: "background1.png")
const images = [
    "background1.png",
    "background2.png"
];

let index = 0;

const bg1 = document.querySelector(".bg1");
const bg2 = document.querySelector(".bg2");

// Simpan kode warna krem transparan biar bisa ditempel di atas gambar
const overlayKrem = "linear-gradient(rgba(246, 241, 234, 0.65), rgba(246, 241, 234, 0.65))";

// Pasang gambar pertama saat web baru dibuka
bg1.style.backgroundImage = `${overlayKrem}, url('${images[0]}')`;

setInterval(() => {
    // Pindah ke gambar selanjutnya
    index = (index + 1) % images.length;

    // Pasang gambar baru di bg2, lalu munculkan perlahan (opacity 1)
    bg2.style.backgroundImage = `${overlayKrem}, url('${images[index]}')`;
    bg2.style.opacity = 1;

    // Setelah 3 detik (transisi selesai), pindahkan gambar ke bg1, dan sembunyikan lagi bg2
    setTimeout(() => {
        bg1.style.backgroundImage = bg2.style.backgroundImage;
        bg2.style.opacity = 0;
    }, 3000);

}, 8000); // Jalan setiap 8 detik