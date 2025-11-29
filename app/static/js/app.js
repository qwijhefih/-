// static/app.js
// ───────────────────────────────────────────────
// [최종본] 실기 퀴즈 클라이언트 (주관식, AI우측, Textarea)
// ───────────────────────────────────────────────

const esc = (s) =>
  String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");

// 타이머 관련 전역 변수
let timerInterval = null;
let timerSeconds = 0;
let timerMode = false;

function renderQuestionText(qText){
  const isCode = qText.startsWith("[코드]");
  if(!isCode) return `<p class="whitespace-pre-wrap">${esc(qText)}</p>`;
  const parts = qText.split(/\n\n/);
  const title = parts[0], code = parts.slice(1).join("\n\n");
  return `
    <div class="mb-2 font-medium">${esc(title)}</div>
    <pre><code class="language-python">${esc(code)}</code></pre>
  `;
}

/**
 * [수정] 주관식 입력창을 <textarea> (자동 높이 조절)로 변경
 */
function renderQuestionCard(q, index){
  
  // textarea 높이를 자동으로 조절하는 스크립트
  const autoResize = `
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
  `;

  return `
    <div class="bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 shadow-sm p-4">
      <div class="flex items-center justify-between mb-2">
        <div class="text-sm text-neutral-500 dark:text-neutral-400">문제 ${index+1}</div>
        <button onclick="toggleBookmark('${esc(q.q)}', '${esc(q.answer)}', '${esc(q.explain || '')}')" class="text-sm text-neutral-500 dark:text-neutral-400 hover:text-yellow-500">
          <span id="bookmark-icon-${index}">⭐</span>
        </button>
      </div>
      <div class="mb-3">${renderQuestionText(q.q)}</div>
      
      <div class="mt-4">
        <textarea
          id="q${index}" 
          name="q${index}" 
          class="w-full px-3 py-2 text-sm border border-neutral-300 dark:border-neutral-600 bg-white dark:bg-neutral-700 rounded-lg focus:outline-none focus:ring-1 focus:ring-neutral-900 dark:focus:ring-neutral-400 resize-none overflow-hidden" 
          placeholder="정답을 입력하세요..."
          autocomplete="off"
          rows="1" 
          oninput="${autoResize}"
        ></textarea>
      </div>
    </div>
  `;
}

function renderQuiz(items){
  const wrap = document.getElementById("quiz");
  wrap.innerHTML = items.map((q,i)=>renderQuestionCard(q,i)).join("");
  
  if(window.hlRefresh) window.hlRefresh();
  
  document.getElementById("submit-wrap").classList.remove("hidden");
  document.getElementById("result").innerHTML = "";

  wrap.addEventListener('input', checkQuizProgress);
  
  updateProgress(0); // 처음엔 0%로 초기화
}

function updateProgress(p){
  document.getElementById("top-progress-bar").style.width = `${p}%`;
}

/**
 * [수정] 실시간 진행률 (텍스트 입력창 기준)
 */
function checkQuizProgress() {
  const total = window.quizItems?.length || 0;
  if (total === 0) {
    updateProgress(0);
    return;
  }

  let answered = 0;
  for (let i = 0; i < total; i++) {
    const inputEl = document.getElementById(`q${i}`);
    if (inputEl && inputEl.value.trim() !== '') {
      answered++;
    }
  }

  const percent = (answered / total) * 100;
  updateProgress(percent);
}


async function loadQuiz(mode="new"){
  const url = mode==="review" ? "/api/review" : "/api/quiz";
  const res = await fetch(url);
  const data = await res.json();
  window.quizItems = data.items;
  window.currentQuizMode = mode; // 현재 퀴즈 모드 저장
  renderQuiz(data.items);
  toast(mode==="review" ? "오답 복습 시작!" : "새 시험 시작!");
  
  // 타이머 시작 (타이머 모드가 활성화된 경우)
  if (timerMode) {
    startTimer();
  } else {
    stopTimer();
  }
  
  // 새 퀴즈 시작 시, AI 튜터의 기억(대화 기록) 초기화
  chatHistory = [];
  const chatMessages = document.getElementById('chat-messages');
  chatMessages.innerHTML = `
    <div class="p-2 bg-neutral-100 dark:bg-neutral-700 rounded-lg text-sm">
      안녕하세요! 정처산기 공부하다 궁금한 걸 물어보세요.
    </div>
  `;
}

/*
 -----------------------------------------------------------------
 ▼▼▼ AI 설명 기능 (submitQuiz, getAIExplanation) ▼▼▼
 -----------------------------------------------------------------
*/
async function getAIExplanation(question, explanation, index) {
  const button = document.getElementById(`ai-btn-${index}`);
  const resultDiv = document.getElementById(`ai-result-${index}`);
  if (!button || !resultDiv) return;
  button.disabled = true;
  resultDiv.style.display = 'block';
  resultDiv.innerHTML = 'AI가 설명 생성 중... 🤖';
  try {
      const res = await fetch("/api/ai/explain", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ q: question, explain: explanation })
      });
      if (!res.ok) throw new Error('AI 서버 응답 오류 (' + res.status + ')');
      const data = await res.json();
      if (data.error) {
          resultDiv.innerHTML = `<span class="text-red-600">${esc(data.error)}</span>`;
      } else {
          resultDiv.innerHTML = `<p class="whitespace-pre-wrap">${esc(data.explanation)}</p>`;
      }
  } catch (error) {
      console.error('AI 설명 요청 실패:', error);
      resultDiv.innerHTML = `<span class="text-red-600">AI 설명을 불러오는데 실패했습니다.</span>`;
  } finally {
      button.style.display = 'none';
  }
}

/**
 * 퀴즈 채점 (틀린 문제에 '내 답안' 표시)
 */
async function submitQuiz(){
    const items = window.quizItems.map((q,i)=>{
        const inputEl = document.getElementById(`q${i}`);
        const userValue = inputEl ? inputEl.value : "";
        return { ...q, user: userValue }; 
    });

    const submitButton = document.getElementById('btn-submit');
    submitButton.disabled = true;
    submitButton.textContent = '채점 중...';

    try {
      const res = await fetch("/api/submit", {
          method:"POST",
          headers:{ "Content-Type":"application/json" },
          body: JSON.stringify({ 
              items,
              quiz_type: window.currentQuizMode || "mixed"
          })
      });
      const data = await res.json();
      const { score, total, wrong, level_info } = data;
      const rate = Math.round((score/total)*100);

      const wrongAnswersHtml = wrong.map((item, index) => {
          const aiButtonId = `ai-btn-${index}`;
          const aiResultId = `ai-result-${index}`;
          return `
              <div class="mt-3 p-3 border-t border-neutral-200 dark:border-neutral-700">
                  <div class="text-sm font-medium text-red-700 dark:text-red-400">틀린 문제:</div>
                  <div class="text-sm whitespace-pre-wrap">${esc(item.q)}</div>
                  <div class="text-sm text-red-700 dark:text-red-400 mt-1"><b>내 답안:</b> <p class="whitespace-pre-wrap inline">${esc(item.user_answer || '(입력 안 함)')}</p></div>
                  <div class="text-sm text-blue-700 dark:text-blue-400 mt-1"><b>정답:</b> ${esc(item.answer)}</div>
                  <div class="text-sm text-neutral-500 dark:text-neutral-400 mt-1"><b>해설:</b> ${esc(item.explain)}</div>
                  <button id="${aiButtonId}" class="text-xs text-blue-600 dark:text-blue-400 hover:underline mt-2">[AI로 더 자세히 보기]</button>
                  <div id="${aiResultId}" class="text-sm mt-2 p-2 bg-neutral-100 dark:bg-neutral-700 rounded-lg" style="display:none;"></div>
              </div>
          `;
      }).join("");
      
      // 레벨 업 표시
      let levelUpHtml = '';
      if (level_info) {
          const levelColor = getLevelColor(level_info.color);
          levelUpHtml = `
              <div class="mt-3 p-3 bg-gradient-to-r ${levelColor} rounded-xl text-white">
                  <div class="flex items-center justify-between mb-2">
                      <div>
                          <div class="text-xs opacity-90">현재 레벨</div>
                          <div class="text-2xl font-bold">Lv.${level_info.level} ${level_info.name}</div>
                      </div>
                      <div class="text-right">
                          <div class="text-xs opacity-90">획득 XP</div>
                          <div class="text-xl font-bold">+${items.find(i => i.user)?.earned_xp || (score * 5)} XP</div>
                      </div>
                  </div>
                  ${!level_info.is_max_level ? `
                      <div class="mt-2">
                          <div class="flex justify-between text-xs mb-1">
                              <span>${level_info.xp} XP</span>
                              <span>${level_info.next_level}까지 ${level_info.xp_to_next} XP</span>
                          </div>
                          <div class="w-full bg-white/30 rounded-full h-2">
                              <div class="bg-white h-2 rounded-full transition-all" style="width: ${level_info.progress_percent}%"></div>
                          </div>
                      </div>
                  ` : '<div class="text-center text-sm mt-2">🏆 최고 레벨 달성! 🏆</div>'}
              </div>
          `;
      }

      document.getElementById("result").innerHTML = `
          <div class="bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 shadow-sm p-4 mt-4">
              <div class="font-semibold mb-2">결과</div>
              <div class="text-sm mb-2">점수: ${score} / ${total} (${rate}%)</div>
              ${levelUpHtml}
              ${wrong.length
                  ? `<div class="text-sm text-red-600 dark:text-red-400 mt-3">오답 ${wrong.length}문항이 기록되었습니다.</div> ${wrongAnswersHtml}`
                  : `<div class="text-sm text-green-600 dark:text-green-400 mt-3">완벽해! 🎉</div>`}
          </div>
      `;

      wrong.forEach((item, index) => {
          const button = document.getElementById(`ai-btn-${index}`);
          if (button) {
              button.onclick = () => getAIExplanation(item.q, item.explain, index);
          }
      });

      checkQuizProgress();
      toast("채점 완료!");

      // 채점 시 타이머 정지
      stopTimer();
      
      // 복습 모드에서 정답 처리 (재출제 일정 업데이트)
      if (window.currentQuizMode === 'review') {
          for (let item of items) {
              if (item.user && item.user.trim().toLowerCase() === item.answer.toString().toLowerCase()) {
                  await markCorrect(item.q);
              }
          }
      }

    } catch (error) {
      console.error('채점 실패:', error);
      toast("채점 중 오류가 발생했습니다.");
    } finally {
      submitButton.disabled = false;
      submitButton.textContent = '채점';
    }
}

/*
 -----------------------------------------------------------------
 ▼▼▼ 기본 이벤트 리스너 (수정 없음) ▼▼▼
 -----------------------------------------------------------------
*/
function toast(msg){
  const el = document.getElementById("toast");
  el.querySelector("div").textContent = msg;
  el.classList.remove("hidden");
  setTimeout(()=>el.classList.add("hidden"), 1800);
}

// 문제 정답 처리 (재출제 일정 업데이트)
async function markCorrect(question) {
    try {
        const res = await fetch('/api/mark_correct', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });
        const data = await res.json();
        if (data.ok && data.message.includes('마스터')) {
            toast(data.message);
        }
    } catch (error) {
        console.error('정답 처리 실패:', error);
    }
}

// 레벨 색상 매핑
function getLevelColor(color) {
    const colorMap = {
        'gray': 'from-gray-500 to-gray-700',
        'blue': 'from-blue-500 to-blue-700',
        'green': 'from-green-500 to-green-700',
        'yellow': 'from-yellow-500 to-yellow-700',
        'orange': 'from-orange-500 to-orange-700',
        'red': 'from-red-500 to-red-700',
        'purple': 'from-purple-500 to-purple-700'
    };
    return colorMap[color] || 'from-gray-500 to-gray-700';
}

// 타이머 기능
function startTimer() {
  stopTimer(); // 기존 타이머 정지
  timerSeconds = 20 * 60; // 20분 = 1200초
  updateTimerDisplay();
  
  timerInterval = setInterval(() => {
    timerSeconds--;
    updateTimerDisplay();
    
    if (timerSeconds <= 0) {
      stopTimer();
      alert('시험 시간이 종료되었습니다! 자동으로 채점됩니다.');
      submitQuiz();
    }
  }, 1000);
}

function stopTimer() {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
  timerSeconds = 0;
  updateTimerDisplay();
}

function updateTimerDisplay() {
  const minutes = Math.floor(timerSeconds / 60);
  const seconds = timerSeconds % 60;
  const display = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
  
  const timerEl = document.getElementById('timer-display');
  if (timerEl) {
    timerEl.textContent = display;
    
    // 5분 이하일 때 빨간색으로 표시
    if (timerSeconds <= 300 && timerSeconds > 0) {
      timerEl.classList.add('text-red-600');
    } else {
      timerEl.classList.remove('text-red-600');
    }
  }
}

// 타이머 토글
document.getElementById('btn-toggle-timer')?.addEventListener('click', () => {
  timerMode = !timerMode;
  const btn = document.getElementById('btn-toggle-timer');
  const icon = document.getElementById('timer-icon');
  
  if (timerMode) {
    btn.classList.remove('bg-neutral-100');
    btn.classList.add('bg-blue-100', 'text-blue-700');
    icon.textContent = '⏱️';
    toast('타이머 모드 ON (20분)');
  } else {
    btn.classList.remove('bg-blue-100', 'text-blue-700');
    btn.classList.add('bg-neutral-100');
    icon.textContent = '⏱';
    stopTimer();
    toast('타이머 모드 OFF');
  }
});

document.getElementById("btn-new").onclick = () => loadQuiz("new");
document.getElementById("btn-review").onclick = () => loadQuiz("review");
document.getElementById("nav-new").onclick = () => loadQuiz("new");
document.getElementById("nav-review").onclick = () => loadQuiz("review");
document.getElementById("nav-bookmarks")?.addEventListener('click', () => loadBookmarksQuiz());
document.getElementById("nav-mock-exam")?.addEventListener('click', () => startMockExam());
document.getElementById("btn-submit").onclick = submitQuiz;
document.getElementById("btn-clear").onclick = async () => {
  await fetch("/api/clear_wrong", { method:"POST" });
  toast("오답 초기화 완료");
};
document.getElementById("btn-export").onclick = () => toast("CSV 내보내기 추후 추가");

// 북마크 기능
async function toggleBookmark(question, answer, explain) {
  try {
    const res = await fetch('/api/bookmarks/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ q: question, answer: answer, explain: explain })
    });
    const data = await res.json();
    toast(data.message || '북마크 완료');
  } catch (error) {
    console.error('북마크 실패:', error);
    toast('북마크 실패');
  }
}

async function loadBookmarksQuiz() {
  const res = await fetch('/api/bookmarks/quiz');
  const data = await res.json();
  
  if (data.items.length === 0) {
    toast('북마크된 문제가 없습니다.');
    return;
  }
  
  window.quizItems = data.items;
  renderQuiz(data.items);
  toast('북마크 퀴즈 시작!');
  
  chatHistory = [];
  const chatMessages = document.getElementById('chat-messages');
  chatMessages.innerHTML = `
    <div class="p-2 bg-neutral-100 dark:bg-neutral-700 rounded-lg text-sm">
      안녕하세요! 정처산기 공부하다 궁금한 걸 물어보세요.
    </div>
  `;
}

// 실전 모의고사 모드
async function startMockExam() {
  if (!confirm('🎯 실전 모의고사 모드\n\n• 40문제 (이론 30 + 코드 10)\n• 제한시간 40분\n• 중간 저장 불가\n• 시간 종료 시 자동 채점\n\n시작하시겠습니까?')) {
    return;
  }
  
  const res = await fetch('/api/quiz?n=40');
  const data = await res.json();
  window.quizItems = data.items;
  renderQuiz(data.items);
  
  // 강제로 타이머 시작 (40분)
  timerMode = true;
  timerSeconds = 40 * 60;
  updateTimerDisplay();
  
  timerInterval = setInterval(() => {
    timerSeconds--;
    updateTimerDisplay();
    
    if (timerSeconds <= 0) {
      stopTimer();
      alert('⏰ 시험 시간이 종료되었습니다! 자동으로 채점됩니다.');
      submitQuiz();
    }
  }, 1000);
  
  toast('🎯 실전 모의고사 시작! (40분)');
  
  chatHistory = [];
  const chatMessages = document.getElementById('chat-messages');
  chatMessages.innerHTML = `
    <div class="p-2 bg-neutral-100 dark:bg-neutral-700 rounded-lg text-sm">
      실전 모의고사 진행 중입니다. 집중하세요! 💪
    </div>
  `;
}

// 초기 로드
loadQuiz("new");

// 다크모드 토글
document.getElementById('btn-dark-mode')?.addEventListener('click', () => {
  const isDark = document.documentElement.classList.toggle('dark');
  localStorage.setItem('darkMode', isDark);
  const icon = document.getElementById('dark-mode-icon');
  if (icon) {
    icon.textContent = isDark ? '☀️' : '🌙';
  }
  toast(isDark ? '다크모드 ON' : '라이트모드 ON');
  
  // 코드 하이라이팅 다시 적용
  if (window.hlRefresh) window.hlRefresh();
});

// 초기 다크모드 아이콘 설정
const isDarkMode = document.documentElement.classList.contains('dark');
const darkIcon = document.getElementById('dark-mode-icon');
if (darkIcon) {
  darkIcon.textContent = isDarkMode ? '☀️' : '🌙';
}


/*
 -----------------------------------------------------------------
 ▼▼▼ AI 문제 자동 생성 기능 ▼▼▼
 -----------------------------------------------------------------
*/
document.getElementById('btn-generate-theory')?.addEventListener('click', async () => {
  const category = prompt('문제 카테고리를 입력하세요:', '데이터베이스');
  if (!category) return;
  
  const count = prompt('생성할 문제 개수를 입력하세요:', '5');
  if (!count) return;
  
  const btn = document.getElementById('btn-generate-theory');
  btn.disabled = true;
  btn.textContent = '생성 중...';
  
  try {
    const res = await fetch('/api/generate/theory', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ category, count: parseInt(count) })
    });
    
    const data = await res.json();
    if (data.ok) {
      alert(data.message + '\n\n서버를 재시작해야 새 문제가 반영됩니다.');
    } else {
      alert('생성 실패: ' + data.message);
    }
  } catch (error) {
    console.error('문제 생성 실패:', error);
    alert('문제 생성에 실패했습니다.');
  } finally {
    btn.disabled = false;
    btn.textContent = '🤖 이론 문제 생성';
  }
});

document.getElementById('btn-generate-code')?.addEventListener('click', async () => {
  const language = prompt('프로그래밍 언어를 입력하세요:', 'Python');
  if (!language) return;
  
  const count = prompt('생성할 문제 개수를 입력하세요:', '5');
  if (!count) return;
  
  const btn = document.getElementById('btn-generate-code');
  btn.disabled = true;
  btn.textContent = '생성 중...';
  
  try {
    const res = await fetch('/api/generate/code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ language, count: parseInt(count) })
    });
    
    const data = await res.json();
    if (data.ok) {
      alert(data.message + '\n\n서버를 재시작해야 새 문제가 반영됩니다.');
    } else {
      alert('생성 실패: ' + data.message);
    }
  } catch (error) {
    console.error('코드 문제 생성 실패:', error);
    alert('코드 문제 생성에 실패했습니다.');
  } finally {
    btn.disabled = false;
    btn.textContent = '💻 코드 문제 생성';
  }
});

document.getElementById('btn-generate-batch')?.addEventListener('click', async () => {
  if (!confirm('운영체제, 데이터베이스, 네트워크 각 3문제씩 생성하시겠습니까?\n(총 9문제, 약 1-2분 소요)')) {
    return;
  }
  
  const btn = document.getElementById('btn-generate-batch');
  btn.disabled = true;
  btn.textContent = '생성 중...';
  
  try {
    const res = await fetch('/api/generate/batch', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        categories: ['운영체제', '데이터베이스', '네트워크'],
        count_per_category: 3
      })
    });
    
    const data = await res.json();
    if (data.ok) {
      alert(data.message + '\n\n서버를 재시작해야 새 문제가 반영됩니다.');
    } else {
      alert('생성 실패: ' + data.message);
    }
  } catch (error) {
    console.error('일괄 생성 실패:', error);
    alert('일괄 생성에 실패했습니다.');
  } finally {
    btn.disabled = false;
    btn.textContent = '⚡ 일괄 생성 (3개씩)';
  }
});


/*
 -----------------------------------------------------------------
 ▼▼▼ [ ✅ 수정 ] AI 챗봇 UI (Shift+Enter 기능 추가) ▼▼▼
 -----------------------------------------------------------------
*/
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const chatSendBtn = document.getElementById('chat-send-btn');
const chatMessages = document.getElementById('chat-messages');

let chatHistory = []; // 대화 기록을 저장할 전역 변수

// [수정] 폼 제출(전송 버튼 클릭) 이벤트
chatForm.addEventListener('submit', (e) => {
    e.preventDefault(); // 폼 기본 동작(새로고침) 방지
    sendChatMessage();
});

// [신규] Textarea에서 Enter/Shift+Enter 키 감지
chatInput.addEventListener('keydown', (e) => {
    // Enter 키만 눌렀을 때 (Shift 키 X)
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault(); // Textarea의 기본 Enter 동작(줄바꿈)을 막음
        sendChatMessage(); // 메시지 전송
    }
    // Shift + Enter 키를 눌렀을 때는 (e.shiftKey가 true)
    // e.preventDefault()를 호출하지 않아, textarea의 기본 동작(줄바꿈)이 실행되도록 둠.
});


/**
 * 챗봇 메시지를 API로 전송하는 함수 (수정 없음)
 */
async function sendChatMessage() {
    const query = chatInput.value.trim();
    if (!query) return;
    
    addMessageToChat('user', query);
    chatInput.value = ''; // 입력창 비우기
    // [수정] 입력창 높이 원래대로 복구
    chatInput.style.height = 'auto';

    chatSendBtn.disabled = true;
    const loadingEl = addMessageToChat('ai', 'AI 튜터가 생각 중... 🤖');

    try {
        const res = await fetch('/api/ai/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                query: query,
                history: chatHistory 
            })
        });

        if (!res.ok) throw new Error('AI 서버 응답 오류');

        const data = await res.json();
        let aiAnswer = ""; // AI 답변을 저장할 변수

        if (data.answer) {
            aiAnswer = data.answer;
            loadingEl.innerHTML = `<p class="whitespace-pre-wrap">${esc(aiAnswer)}</p>`;
        } else {
            aiAnswer = data.error || '답변을 가져오지 못했습니다.';
            loadingEl.innerHTML = `<span class="text-red-600">${esc(aiAnswer)}</span>`;
        }

        // 대화 기록(History)에 내 질문과 AI 답변을 추가
        chatHistory.push({ "role": "user", "text": query });
        chatHistory.push({ "role": "model", "text": aiAnswer });

    } catch (error) {
        console.error('AI 챗봇 요청 실패:', error);
        loadingEl.innerHTML = `<span class="text-red-600">AI 챗봇 연결에 실패했습니다.</span>`;
    } finally {
        chatSendBtn.disabled = false;
        scrollToChatBottom();
    }
}

/**
 * 채팅창에 메시지를 추가하는 헬퍼 함수 (수정 없음)
 */
function addMessageToChat(sender, text) {
    const div = document.createElement('div');
    div.classList.add('text-sm', 'p-2', 'rounded-lg');
    if (sender === 'user') {
        div.classList.add('bg-blue-100', 'dark:bg-blue-900', 'text-blue-900', 'dark:text-blue-100', 'self-end');
    } else {
        div.classList.add('bg-neutral-100', 'dark:bg-neutral-700');
    }
    div.innerHTML = `<p class="whitespace-pre-wrap">${esc(text)}</p>`;
    chatMessages.appendChild(div);
    scrollToChatBottom();
    return div;
}

/**
 * 채팅창 스크롤을 맨 아래로 내리는 함수 (수정 없음)
 */
function scrollToChatBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// ───────────────────────────────────────────────
// 학습 메모 기능
// ───────────────────────────────────────────────

let currentEditNoteId = null; // 현재 수정 중인 메모 ID

// 메모 목록 로드
async function loadNotes(category = '') {
    try {
        const url = category ? `/api/notes?category=${encodeURIComponent(category)}` : '/api/notes';
        const res = await fetch(url);
        const data = await res.json();
        
        if (data.ok) {
            renderNotesList(data.notes);
        }
    } catch (error) {
        console.error('메모 로드 실패:', error);
    }
}

// 메모 목록 렌더링
function renderNotesList(notes) {
    const notesList = document.getElementById('notes-list');
    if (!notes || notes.length === 0) {
        notesList.innerHTML = '<p class="text-sm text-neutral-500 dark:text-neutral-400">메모가 없습니다.</p>';
        return;
    }
    
    notesList.innerHTML = notes.map(note => `
        <div class="p-3 bg-neutral-100 dark:bg-neutral-700 rounded-lg cursor-pointer hover:bg-neutral-200 dark:hover:bg-neutral-600" data-note-id="${note.id}">
            <div class="flex items-start justify-between mb-1">
                <div class="font-semibold text-sm">${esc(note.title)}</div>
                <button class="delete-note text-red-600 hover:text-red-800" data-note-id="${note.id}" onclick="event.stopPropagation();">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                </button>
            </div>
            <div class="text-xs text-neutral-500 dark:text-neutral-400 mb-2">${note.category} • ${new Date(note.created_at).toLocaleDateString()}</div>
            <div class="text-sm text-neutral-700 dark:text-neutral-300 line-clamp-2">${esc(note.content)}</div>
        </div>
    `).join('');
    
    // 메모 클릭 시 수정 모드
    notesList.querySelectorAll('[data-note-id]').forEach(el => {
        el.addEventListener('click', () => {
            if (el.classList.contains('delete-note')) return;
            const noteId = parseInt(el.dataset.noteId);
            const note = notes.find(n => n.id === noteId);
            if (note) editNote(note);
        });
    });
    
    // 삭제 버튼
    notesList.querySelectorAll('.delete-note').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.stopPropagation();
            const noteId = parseInt(btn.dataset.noteId);
            if (confirm('이 메모를 삭제하시겠습니까?')) {
                await deleteNote(noteId);
            }
        });
    });
}

// 메모 추가
async function addNote() {
    const title = document.getElementById('note-title').value.trim() || '무제';
    const content = document.getElementById('note-content').value.trim();
    const category = document.getElementById('note-category').value;
    
    if (!content) {
        alert('메모 내용을 입력해주세요.');
        return;
    }
    
    try {
        const res = await fetch('/api/notes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, content, category })
        });
        
        const data = await res.json();
        if (data.ok) {
            showToast('메모가 저장되었습니다.');
            clearNoteForm();
            loadNotes();
        }
    } catch (error) {
        console.error('메모 저장 실패:', error);
    }
}

// 메모 수정
function editNote(note) {
    currentEditNoteId = note.id;
    document.getElementById('note-title').value = note.title;
    document.getElementById('note-content').value = note.content;
    document.getElementById('note-category').value = note.category;
    document.getElementById('btn-save-note').textContent = '수정 완료';
}

// 메모 업데이트
async function updateNote() {
    if (!currentEditNoteId) {
        await addNote();
        return;
    }
    
    const title = document.getElementById('note-title').value.trim() || '무제';
    const content = document.getElementById('note-content').value.trim();
    const category = document.getElementById('note-category').value;
    
    try {
        const res = await fetch(`/api/notes/${currentEditNoteId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, content, category })
        });
        
        const data = await res.json();
        if (data.ok) {
            showToast('메모가 수정되었습니다.');
            clearNoteForm();
            loadNotes();
        }
    } catch (error) {
        console.error('메모 수정 실패:', error);
    }
}

// 메모 삭제
async function deleteNote(noteId) {
    try {
        const res = await fetch(`/api/notes/${noteId}`, { method: 'DELETE' });
        const data = await res.json();
        
        if (data.ok) {
            showToast('메모가 삭제되었습니다.');
            loadNotes();
        }
    } catch (error) {
        console.error('메모 삭제 실패:', error);
    }
}

// 메모 폼 초기화
function clearNoteForm() {
    currentEditNoteId = null;
    document.getElementById('note-title').value = '';
    document.getElementById('note-content').value = '';
    document.getElementById('note-category').value = '일반';
    document.getElementById('btn-save-note').textContent = '저장';
}

// 메모 모달 열기/닫기
function openNotesModal() {
    document.getElementById('notes-modal').classList.remove('hidden');
    document.getElementById('notes-modal').classList.add('flex');
    loadNotes();
}

function closeNotesModal() {
    document.getElementById('notes-modal').classList.add('hidden');
    document.getElementById('notes-modal').classList.remove('flex');
    clearNoteForm();
}

// 이벤트 리스너
document.addEventListener('DOMContentLoaded', () => {
    const navNotes = document.getElementById('nav-notes');
    const btnViewNotes = document.getElementById('btn-view-notes');
    const closeModal = document.getElementById('close-notes-modal');
    const btnAddNote = document.getElementById('btn-add-note');
    const btnSaveNote = document.getElementById('btn-save-note');
    const btnCancelNote = document.getElementById('btn-cancel-note');
    const categoryFilters = document.querySelectorAll('.note-category-filter');
    
    if (navNotes) navNotes.addEventListener('click', openNotesModal);
    if (btnViewNotes) btnViewNotes.addEventListener('click', openNotesModal);
    if (closeModal) closeModal.addEventListener('click', closeNotesModal);
    if (btnAddNote) btnAddNote.addEventListener('click', clearNoteForm);
    if (btnSaveNote) btnSaveNote.addEventListener('click', updateNote);
    if (btnCancelNote) btnCancelNote.addEventListener('click', clearNoteForm);
    
    categoryFilters.forEach(btn => {
        btn.addEventListener('click', () => {
            const category = btn.dataset.category;
            loadNotes(category);
            
            // 활성 카테고리 표시
            categoryFilters.forEach(b => b.classList.remove('bg-blue-500', 'text-white'));
            btn.classList.add('bg-blue-500', 'text-white');
        });
    });
    
    // 페이지 로드 시 레벨 정보 표시
    loadLevelBadge();
});

// 레벨 배지 업데이트
async function loadLevelBadge() {
    try {
        const res = await fetch('/api/stats');
        const data = await res.json();
        
        if (data.level_info) {
            const badge = document.getElementById('level-badge');
            if (badge) {
                badge.classList.remove('hidden');
                badge.textContent = `Lv.${data.level_info.level} ${data.level_info.name}`;
                
                // 레벨에 따른 색상 변경
                const colorMap = {
                    'gray': 'bg-gray-100 dark:bg-gray-900 text-gray-700 dark:text-gray-300',
                    'blue': 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300',
                    'green': 'bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300',
                    'yellow': 'bg-yellow-100 dark:bg-yellow-900 text-yellow-700 dark:text-yellow-300',
                    'orange': 'bg-orange-100 dark:bg-orange-900 text-orange-700 dark:text-orange-300',
                    'red': 'bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300',
                    'purple': 'bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300'
                };
                
                badge.className = `flex items-center gap-1 px-2 py-1 rounded-lg text-xs font-semibold ${colorMap[data.level_info.color]}`;
            }
        }
    } catch (error) {
        console.error('레벨 정보 로드 실패:', error);
    }
}