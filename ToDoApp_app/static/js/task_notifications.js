document.addEventListener('DOMContentLoaded', function () {
    const checkboxes = document.querySelectorAll('.complete-checkbox');
    const modal = document.getElementById('congratsModal');
    const closeBtn = document.getElementById('closeCongratsBtn');
    const clapSound = document.getElementById('clapSound');

    // Handle checkbox toggle
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            const taskDiv = this.closest('.task');
            const taskId = taskDiv.getAttribute('data-task-id');
            const completed = this.checked;

            // Send update to backend
            fetch('/update-task-completion/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ task_id: taskId, completed: completed })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // If marked as completed, show modal and play sound
                    if (completed) {
                        modal.style.display = 'block';
                        clapSound.currentTime = 0;
                        clapSound.play();
                    }
                } else {
                    alert('Update failed: ' + data.message);
                    this.checked = !completed;  // Revert checkbox
                }
            })
            .catch(() => {
                alert('Network error');
                this.checked = !completed;
            });
        });
    });

    // Close modal on close button click
    closeBtn.addEventListener('click', function () {
        modal.style.display = 'none';
        clapSound.pause();
        clapSound.currentTime = 0;
    });

    // Close modal when clicking outside of it
    window.addEventListener('click', function (e) {
        if (e.target === modal) {
            modal.style.display = 'none';
            clapSound.pause();
            clapSound.currentTime = 0;
        }
    });

    // Function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

