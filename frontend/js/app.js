document.addEventListener('DOMContentLoaded', () => {
    console.log("AI Profil Chatbot Frontend Mimarisi Başlatıldı.");

    const candidatesGrid = document.getElementById('candidatesGrid');
    const loadSampleBtn = document.getElementById('loadSampleBtn');
    const uploadBtn = document.getElementById('uploadBtn');

    // Başlangıçta sahte verilerle gridi dolduralım ki premium hava korunsun
    setTimeout(() => {
        renderMockCandidates();
    }, 1000);

    // Etkileşimler
    loadSampleBtn.addEventListener('click', () => {
        // Backend API çağrısı simulasyonu
        loadSampleBtn.classList.add('loading');
        loadSampleBtn.textContent = 'Yükleniyor...';
        
        setTimeout(() => {
            loadSampleBtn.classList.remove('loading');
            loadSampleBtn.textContent = 'Örnek Veri Yüklendi';
            loadSampleBtn.style.backgroundColor = 'var(--accent)';
            loadSampleBtn.style.color = '#fff';
            
            fetchCandidates();
        }, 1500);
    });

    uploadBtn.addEventListener('click', () => {
        alert("CV Yükleme Modülü (WP6) için altyapı hazır. Backend /api/upload endpointine bağlanacak.");
    });

    function renderMockCandidates() {
        const mockData = [
            { id: 1, name: "Enes Kaya", role: "AI Software Engineer", score: 92, skills: ["Python", "React", "LLM"] },
            { id: 2, name: "Ayşe Yılmaz", role: "Frontend Tech Lead", score: 88, skills: ["Vue", "TailwindCSS", "Node.js"] },
            { id: 3, name: "Mehmet Demir", role: "Cloud Architect", score: 95, skills: ["AWS", "Kubernetes", "Docker"] }
        ];

        candidatesGrid.innerHTML = '';
        mockData.forEach(cand => {
            candidatesGrid.innerHTML += createCandidateCardHTML(cand);
        });
    }

    async function fetchCandidates() {
        try {
            const apiBase = 'http://localhost:8000/api/candidates';
            const res = await fetch(apiBase);
            if(res.ok) {
                const data = await res.json();
                if(data.length > 0) {
                    candidatesGrid.innerHTML = '';
                    data.forEach(cand => {
                        candidatesGrid.innerHTML += createCandidateCardHTML({
                            id: cand.id,
                            name: cand.name,
                            role: "Software Developer",
                            score: cand.quiz_score || 0,
                            skills: cand.skills
                        });
                    });
                }
            }
        } catch (e) {
            console.warn("Backend kapalı olabilir, sahte veriler gösteriliyor.");
        }
    }

    function createCandidateCardHTML(candidate) {
        return `
            <div class="candidate-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px;">
                    <div>
                        <h3 style="font-size: 1.25rem; margin-bottom: 4px; color: #fff;">${candidate.name}</h3>
                        <p style="color: var(--text-muted); font-size: 0.875rem;">${candidate.role}</p>
                    </div>
                    <div style="background: rgba(20, 184, 166, 0.1); color: var(--accent); padding: 4px 10px; border-radius: 100px; font-weight: 600; font-size: 0.875rem;">
                        Quiz: ${candidate.score}%
                    </div>
                </div>
                
                <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 24px;">
                    ${candidate.skills.map(s => `<span style="background: rgba(255,255,255,0.05); padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; border: 1px solid rgba(255,255,255,0.1)">${s}</span>`).join('')}
                </div>

                <div style="display: flex; gap: 12px;">
                    <button class="btn btn-outline" style="flex: 1; padding: 8px; font-size: 0.875rem;" onclick="alert('Detay Sayfası')">Profili Gör</button>
                    <button class="btn btn-primary" style="flex: 1; padding: 8px; font-size: 0.875rem; background: var(--secondary);" onclick="alert('/api/chat/${candidate.id} ile AI Bot Başlatılıyor...')">💬 Sohbet Et</button>
                </div>
            </div>
        `;
    }
});
