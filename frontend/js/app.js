// --- GLOBAL FUNCTIONS (Butonların her zaman erişebilmesi için) ---
window.toggleAuth = (mode) => {
    const tabLogin = document.getElementById('tabLogin');
    const tabRegister = document.getElementById('tabRegister');
    const regFields = document.getElementById('registerOnlyFields');
    const submitBtn = document.getElementById('authSubmitBtn');

    if (mode === 'login') {
        tabLogin.classList.add('active');
        tabRegister.classList.remove('active');
        regFields.style.display = 'none';
        submitBtn.textContent = 'Giriş Yap';
    } else {
        tabLogin.classList.remove('active');
        tabRegister.classList.add('active');
        regFields.style.display = 'block';
        submitBtn.textContent = 'Kayıt Ol';
    }
    window.authMode = mode;
};

window.closeAllModals = () => {
    document.querySelectorAll('.modal').forEach(m => m.classList.remove('active'));
    if (window.chatInterval) clearInterval(window.chatInterval);
};

window.switchTab = (tab) => {
    const candView = document.getElementById('candidatesView');
    const msgView = document.getElementById('messagesView');
    const menuCand = document.getElementById('menuCandidates');
    const menuMsg = document.getElementById('menuMessages');

    if (tab === 'candidates') {
        candView.style.display = 'block';
        msgView.style.display = 'none';
        menuCand.classList.add('active');
        menuMsg.classList.remove('active');
    } else {
        candView.style.display = 'none';
        msgView.style.display = 'block';
        menuCand.classList.remove('active');
        menuMsg.classList.add('active');
        window.fetchActiveChats(); // Mesajlar sekmesine geçince listeyi yenile
    }
};

window.switchDevTab = (tab) => {
    const quizView = document.getElementById('devQuizView');
    const msgView = document.getElementById('devMessagesView');
    const menuQuiz = document.getElementById('devMenuQuiz');
    const menuMsg = document.getElementById('devMenuMessages');

    if (tab === 'quiz') {
        quizView.style.display = 'block';
        msgView.style.display = 'none';
        menuQuiz.classList.add('active');
        menuMsg.classList.remove('active');
    } else {
        quizView.style.display = 'none';
        msgView.style.display = 'block';
        menuQuiz.classList.remove('active');
        menuMsg.classList.add('active');
        window.fetchActiveChats(); // Mesajlar sekmesine geçince listeyi yenile
    }
};

window.fetchActiveChats = async () => {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (!currentUser) return;
    try {
        const res = await fetch(`http://localhost:8000/api/messages/active-chats/${currentUser.id}`);
        const chats = await res.json();
        const listId = currentUser.role === 'hr' ? 'recentChatsList' : 'devChatsList';
        const list = document.getElementById(listId);
        
        if (chats.length === 0) {
            list.innerHTML = '<p style="text-align: center; padding: 40px; color: var(--text-muted); background: rgba(255,255,255,0.02); border-radius: 20px;">Henüz aktif bir sohbetiniz bulunmuyor.</p>';
            return;
        }
        
        // FIX: MongoDB string ID için '${user.id}' şeklinde tırnak eklendi.
        list.innerHTML = chats.map(user => `
            <div class="candidate-card" style="display: flex; justify-content: space-between; align-items: center; cursor: pointer; margin-bottom: 12px; padding: 16px 24px;" onclick="openDirectChat('${user.id}', '${user.full_name}')">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div class="user-avatar" style="background: var(--primary); color: #fff;">${user.full_name[0]}</div>
                    <div>
                        <h4 style="margin: 0; color: #fff;">${user.full_name}</h4>
                        <small style="color: var(--text-muted);">${user.role === 'hr' ? 'İK Uzmanı' : 'Aday'}</small>
                    </div>
                </div>
                <div style="color: var(--primary); font-size: 1.2rem;">💬</div>
            </div>
        `).join('');
    } catch (e) { console.error("Sohbetler yüklenemedi", e); }
};

window.logout = () => {
    localStorage.removeItem('currentUser');
    location.reload();
};

document.addEventListener('DOMContentLoaded', () => {
    const apiBase = 'http://localhost:8000/api';
    window.authMode = 'login';
    let currentUser = JSON.parse(localStorage.getItem('currentUser')) || null;
    let currentAICandidateId = null;
    let currentChatPartnerId = null;

    // --- DASHBOARD DISPLAY ---
    function showDashboard(user) {
        document.getElementById('loginScreen').style.display = 'none';
        document.getElementById('globalNavbar').style.display = 'flex';
        document.getElementById('navUserName').textContent = user.full_name;
        document.getElementById('navRoleBadge').textContent = user.role === 'hr' ? 'İK Paneli' : 'Aday Paneli';

        if (user.role === 'candidate') {
            document.getElementById('developerDashboard').style.display = 'block';
            document.getElementById('hrDashboard').style.display = 'none';
            document.getElementById('devWelcomeName').textContent = user.full_name;
            fetchMyQuizzes(user.id);
        } else {
            document.getElementById('hrDashboard').style.display = 'flex';
            document.getElementById('developerDashboard').style.display = 'none';
            fetchCandidates();
        }
    }

    async function fetchMyQuizzes(userId) {
        try {
            const res = await fetch(`${apiBase}/candidates/my-quizzes/${userId}`);
            const list = await res.json();
            const historyList = document.getElementById('myQuizHistory');
            if (list.length === 0) {
                historyList.innerHTML = '<p style="color: var(--text-muted);">Henüz bir sınavınız bulunmuyor.</p>';
                return;
            }
            historyList.innerHTML = list.map(q => `
                <div class="candidate-card" style="display: flex; justify-content: space-between; align-items: center; padding: 15px 25px;">
                    <div>
                        <h4 style="margin: 0; color: #fff;">${q.name}</h4>
                        <small style="color: var(--text-muted);">Skor: %${q.quiz_score || 0}</small>
                    </div>
                    <div class="nav-role-badge" style="background: rgba(20, 184, 166, 0.1); color: var(--accent); border-color: rgba(20, 184, 166, 0.2);">TAMAMLANDI</div>
                </div>
            `).join('');
        } catch (e) { console.error("Sınav geçmişi yüklenemedi", e); }
    }

    if (currentUser) showDashboard(currentUser);

    // --- AUTH SUBMIT ---
    document.getElementById('authSubmitBtn').addEventListener('click', async () => {
        const email = document.getElementById('emailInput').value.trim();
        const password = document.getElementById('passwordInput').value.trim();
        if (!email || !password) return alert("Lütfen alanları doldurun.");

        try {
            if (window.authMode === 'register') {
                const fullName = document.getElementById('fullNameInput').value.trim();
                const role = document.querySelector('input[name="authRole"]:checked').value;
                const res = await fetch(`${apiBase}/auth/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password, full_name: fullName, role })
                });
                if (!res.ok) throw new Error("Kayıt başarısız.");
                alert("Kayıt başarılı! Giriş yapabilirsiniz.");
                window.toggleAuth('login');
            } else {
                const res = await fetch(`${apiBase}/auth/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                if (!res.ok) throw new Error("Giriş bilgileri hatalı.");
                const user = await res.json();
                localStorage.setItem('currentUser', JSON.stringify(user));
                location.reload();
            }
        } catch (e) { alert(e.message); }
    });

    // --- HR ACTIONS ---
    async function fetchCandidates() {
        try {
            const res = await fetch(`${apiBase}/candidates/`);
            const list = await res.json();
            const grid = document.getElementById('candidatesGrid');
            grid.innerHTML = list.map(cand => {
                const hasScore = cand.quiz_score && cand.quiz_score > 0;
                const trustScore = cand.trust_score || 0;
                const scoreLabel = hasScore ? `%${cand.quiz_score} Skor` : 'Sınava Girmedi';
                const badgeStyle = hasScore 
                    ? 'style="background: rgba(249,109,0,0.15); color: #f96d00; border-color: rgba(249,109,0,0.3);"'
                    : 'style="background: rgba(245,158,11,0.1); color: #f59e0b; border-color: rgba(245,158,11,0.2);"';
                const trustBadge = trustScore > 0
                    ? `<span style="margin-left:8px; font-size:0.75rem; background:rgba(34,197,94,0.1); color:#22c55e; border:1px solid rgba(34,197,94,0.2); border-radius:20px; padding:3px 10px;">🛡️ Güven: ${trustScore}</span>`
                    : '';

                return `
                    <div class="candidate-card">
                        <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
                            <div class="card-badge" ${badgeStyle}>${scoreLabel}</div>
                            ${trustBadge}
                        </div>
                        <h3>${cand.name}</h3>
                        <p>${cand.experience_years} Yıl Deneyim</p>
                        <div style="margin-top: 15px; display: flex; gap: 10px;">
                            <button class="btn btn-primary btn-sm" onclick="openAIChat('${cand.id}', '${cand.name}')">AI Mülakat</button>
                            <button class="btn btn-outline btn-sm" onclick="openDirectChat('${cand.user_id || cand.id}', '${cand.name}')">Mesaj</button>
                        </div>
                    </div>
                `;
            }).join('');
        } catch (e) { console.error("Adaylar yüklenemedi", e); }
    }

    window.openAIChat = (id, name) => {
        currentAICandidateId = id;
        document.getElementById('chatCandidateName').textContent = name;
        document.getElementById('chatMessages').innerHTML = `
            <div class="msg-wrapper received">
                <div class="msg msg-ai">Merhaba! <strong>${name}</strong> hakkında ne bilmek istersiniz?</div>
            </div>`;
        document.getElementById('chatModal').classList.add('active');
    };

    window.openDirectChat = (id, name) => {
        currentChatPartnerId = id;
        document.getElementById('msgCandidateName').textContent = name;
        document.getElementById('messageModal').classList.add('active');
        loadMessages();
        if (window.chatInterval) clearInterval(window.chatInterval);
        window.chatInterval = setInterval(loadMessages, 3000);
    };

    async function loadMessages() {
        if (!currentChatPartnerId || !currentUser) return;
        try {
            const res = await fetch(`${apiBase}/messages/history/${currentUser.id}/${currentChatPartnerId}`);
            if (!res.ok) return;
            const messages = await res.json();
            const list = document.getElementById('directMessages');
            // FIX: String() ile karşılaştır — MongoDB ObjectId her zaman string
            list.innerHTML = messages.map(m => {
                const isMine = String(m.sender_id) === String(currentUser.id);
                const wrapperClass = isMine ? 'sent' : 'received';
                const msgClass = isMine ? 'msg-user' : 'msg-ai';
                return `
                    <div class="msg-wrapper ${wrapperClass}">
                        <div class="msg ${msgClass}">${m.content}</div>
                    </div>`;
            }).join('');
            list.scrollTop = list.scrollHeight;
        } catch(e) { console.error('Mesajlar yüklenemedi', e); }
    }

    // --- SEND BUTTONS ---
    document.getElementById('sendMsgBtn').onclick = async () => {
        const input = document.getElementById('chatInput');
        const text = input.value.trim();
        if (!text || !currentAICandidateId) return;
        appendMsg('chatMessages', 'user', text);
        input.value = '';
        const res = await fetch(`${apiBase}/chat/${currentAICandidateId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        const data = await res.json();
        appendMsg('chatMessages', 'ai', data.response);
    };

    document.getElementById('sendDirectMsgBtn').onclick = async () => {
        const input = document.getElementById('directMsgInput');
        const text = input.value.trim();
        if (!text || !currentChatPartnerId) return;
        await fetch(`${apiBase}/messages/send`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sender_id: currentUser.id, receiver_id: currentChatPartnerId, content: text })
        });
        input.value = '';
        loadMessages();
    };

    function appendMsg(id, type, text) {
        const list = document.getElementById(id);
        const div = document.createElement('div');
        const isMine = (type === 'user');
        div.className = `msg-wrapper ${isMine ? 'sent' : 'received'}`;
        div.innerHTML = `<div class="msg ${isMine ? 'msg-user' : 'msg-ai'}">${text}</div>`;
        list.appendChild(div);
        list.scrollTop = list.scrollHeight;
    }

    // --- UPLOAD LOGIC ---
    const uploadBtn = document.getElementById('uploadBtn');
    const fileInput = document.createElement('input');
    fileInput.type = 'file';

    if (uploadBtn) {
        uploadBtn.addEventListener('click', (e) => {
            console.log("Upload tıklandı");
            fileInput.click();
        });
    }

    fileInput.onchange = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        document.getElementById('loadingOverlay').style.display = 'flex';
        const formData = new FormData();
        formData.append('file', file);

        try {
            const res = await fetch(`${apiBase}/upload/`, {
                method: 'POST',
                body: formData,
                headers: { 'user-id': currentUser.id }
            });
            const data = await res.json();
            document.getElementById('loadingOverlay').style.display = 'none';
            if (data.quiz) {
                renderQuiz(data.quiz, data.candidate_id);
                document.getElementById('quizModal').classList.add('active');
            }
        } catch (err) {
            document.getElementById('loadingOverlay').style.display = 'none';
            alert("Hata oluştu.");
        }
    };

    function renderQuiz(quiz, candId) {
        // FIX: Quiz format kontrolü — API'den gelen yanıt geçerli mi?
        if (!quiz || !quiz.questions || quiz.questions.length === 0) {
            alert('Sınav oluşturulamadı. Lütfen tekrar deneyin.');
            document.getElementById('loadingOverlay').style.display = 'none';
            return;
        }
        const body = document.getElementById('quizBody');
        body.innerHTML = quiz.questions.map((q, i) => `
            <div class="question-item">
                <p style="font-weight:600; margin-bottom:12px;">${i + 1}. ${q.question_text || q.question || 'Soru yüklenemedi'}</p>
                ${(q.options || []).map((opt, oi) => `<label class="option-label"><input type="radio" name="q${i}" value="${oi}"> <span>${opt}</span></label>`).join('')}
            </div>
        `).join('');
        document.getElementById('quizFooter').style.display = 'block';
        document.getElementById('submitQuizBtn').onclick = async () => {
            const answers = quiz.questions.map((_, i) => {
                const sel = document.querySelector(`input[name="q${i}"]:checked`);
                return sel ? parseInt(sel.value) : -1;
            });
            const res = await fetch(`${apiBase}/candidates/${candId}/quiz/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ candidate_id: candId, answers })
            });
            const result = await res.json();
            closeAllModals();
            alert(`✅ Sınav Tamamlandı!\nSkor: %${result.quiz_score}\n🛡️ AI Güven Skoru: ${result.trust_score}`);
            location.reload();
        };
    }
});
