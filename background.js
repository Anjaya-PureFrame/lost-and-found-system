console.log("JS slideshow jalan!");

// Daftar 4 gambar tema autumn kamu
const images = [
    "background1.png",
    "background2.png",
    "background3.png",
    "background4.png"
];

let index = 0;
const bg1 = document.querySelector(".bg1");
const bg2 = document.querySelector(".bg2");

// Warna overlay krem transparan
const overlayKrem = "linear-gradient(rgba(246, 241, 234, 0.65), rgba(246, 241, 234, 0.20))";

// Pasang gambar pertama saat halaman awal dimuat
bg1.style.backgroundImage = `${overlayKrem}, url('${images[0]}')`;

setInterval(() => {
    // Geser index berputar 0 -> 1 -> 2 -> 3 -> balik ke 0
    index = (index + 1) % images.length;

    // Pasang gambar target di bg2 lalu munculkan perlahan (fade-in)
    bg2.style.backgroundImage = `${overlayKrem}, url('${images[index]}')`;
    bg2.style.opacity = "1";

    // Setelah durasi transisi selesai (misal 2.5 detik), sinkronkan bg1 dan reset bg2
    setTimeout(() => {
        bg1.style.backgroundImage = bg2.style.backgroundImage;
        bg2.style.opacity = "0";
    }, 2500);

}, 8000); // Berganti gambar setiap 8 detik