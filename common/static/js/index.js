const logo = document.querySelector('.logo');
const instructionBox = document.getElementById('instructionBox');
        
function toggleInstructions() {
    if (instructionBox.style.display === "none" || instructionBox.style.display === "") {
        instructionBox.style.display = "block";
        logo.classList.add('paused');
    } 
    else {
        closeInstructions();
    }
}

function closeInstructions() {
    instructionBox.style.display = "none";
    logo.classList.remove('paused');
}

function setMode(mode, sendRequest = true) {
    document.querySelectorAll('#mode-selection button').forEach(btn => {
        btn.classList.remove('active');
    });
    document.getElementById(mode.toLowerCase() + '-btn').classList.add('active');
    if (sendRequest) {
        sendChatMessage('mode: ' + mode.toLowerCase());
    }
    else{
        sendChatMessage('reset mode');
    }
}

function addMessage(sender, message) {
    $('#chat-container').append('<div class="message ' + sender + '">' + message + '</div>');
    $('#chat-container').scrollTop($('#chat-container')[0].scrollHeight);
}

function sendMessage() {
    var message = $('#user-input').val();
    if (message.trim() === '') return;

    addMessage('user', message);
    $('#user-input').val('');
    sendChatMessage(message);
}

function sendChatMessage(message) {
    $.ajax({
        url: 'http://127.0.0.1:5000/chat',
        method: 'POST',
        data: { message: message },
        success: function(data) {
            if (data.response.trim() !== ''){
                addMessage('bot', data.response.replace(/\n/g, '<br>'));
            }
        },
        error: function() {
            addMessage('bot', 'Rất tiếc, đã xảy ra lỗi khi xử lý yêu cầu của bạn.');
        }
    });
}

// Đặt ChatGPT làm chế độ mặc định khi trang web được tải, nhưng không gửi yêu cầu
window.onload = function() {
    setMode('ChatGPT', false);
};

$('#user-input').keypress(function(e) {
    if (e.which == 13) {
        sendMessage();
        return false;
    }
});

addMessage('bot', "Xin chào! Tôi có thể hỗ trợ bạn tìm câu hỏi trắc nghiệm cho môn học 'Quản lý dự án'. Nhập <code>`chương hỗ trợ`</code> để xem các chương mà tôi đang hỗ trợ sinh câu hỏi.<br><br>Bạn cũng có thể chọn chế độ sinh câu hỏi bằng cách nhấp vào các nút chế độ phía trên.");