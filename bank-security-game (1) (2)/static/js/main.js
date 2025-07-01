// Khởi tạo particles.js khi trang tải xong
document.addEventListener('DOMContentLoaded', function() {
    // Khởi tạo particles.js nếu có trên trang
    if (typeof particlesJS !== 'undefined' && document.getElementById('particles-js')) {
        particlesJS('particles-js', {
            particles: {
                number: { value: 80, density: { enable: true, value_area: 800 } },
                color: { value: "#ffffff" },
                shape: { type: "circle" },
                opacity: { value: 0.5, random: true },
                size: { value: 3, random: true },
                line_linked: { enable: true, distance: 150, color: "#ffffff", opacity: 0.4, width: 1 },
                move: { enable: true, speed: 2, direction: "none", random: true, straight: false, out_mode: "out" }
            },
            interactivity: {
                detect_on: "canvas",
                events: {
                    onhover: { enable: true, mode: "repulse" },
                    onclick: { enable: true, mode: "push" }
                }
            }
        });
    }
    
    // Thêm hiệu ứng cho các card level
    const levelCards = document.querySelectorAll('.level-card');
    levelCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.classList.add('animate__animated', 'animate__pulse');
        });
        card.addEventListener('mouseleave', () => {
            card.classList.remove('animate__animated', 'animate__pulse');
        });
    });
    
    // Cập nhật progress bar nếu có trên trang
    const progressBar = document.getElementById('progress-bar');
    if (progressBar) {
        // Tính toán % tiến trình dựa trên số giao dịch đã hoàn thành
        const txTotal = parseInt('{{ transaction_count }}');
        const txCompleted = 0; // Thay bằng giá trị thực từ server
        const progressPercent = (txCompleted / txTotal) * 100;
        progressBar.style.width = `${progressPercent}%`;
    }
});

// Hiển thị toast thông báo
function showToast(message, isSuccess = true) {
    const toast = document.getElementById('feedback-toast');
    const icon = document.getElementById('toast-icon');
    const msg = document.getElementById('toast-message');
    
    toast.classList.remove('hidden');
    toast.classList.remove('bg-red-100', 'text-red-800');
    toast.classList.remove('bg-green-100', 'text-green-800');
    
    if (isSuccess) {
        toast.classList.add('bg-green-100', 'text-green-800');
        icon.className = 'fas fa-check-circle text-green-500 mr-3';
    } else {
        toast.classList.add('bg-red-100', 'text-red-800');
        icon.className = 'fas fa-times-circle text-red-500 mr-3';
    }
    
    msg.textContent = message;
    
    // Ẩn toast sau 3 giây
    setTimeout(() => {
        toast.classList.add('hidden');
    }, 3000);
}