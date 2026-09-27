const form = document.getElementById("ideaForm");
const gradeInput = document.getElementById("grade");
const interestInput = document.getElementById("interest");
const topicInput = document.getElementById("topic");

const resultText = document.getElementById("resultText");
const generateButton = document.getElementById("generateButton");


form.addEventListener("submit", async function (event) {

    // 폼의 기본 새로고침 동작 방지
    event.preventDefault();

    const grade = gradeInput.value.trim();
    const interest = interestInput.value.trim();
    const topic = topicInput.value.trim();


    // 1. 빈 입력 검사
    if (!grade || !interest || !topic) {
        resultText.textContent =
            "⚠️ 학년, 관심사, 주제를 모두 입력해주세요.";
        return;
    }


    // 2. 로딩 상태 표시
    generateButton.disabled = true;
    generateButton.textContent = "아이디어 생성 중...";

    resultText.textContent =
        "✨ SparkIdea AI가 너에게 맞는 아이디어를 생각하고 있어요...";


    try {

        // 3. Python 백엔드에 요청
        const response = await fetch("/api/generate", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                grade: grade,
                interest: interest,
                topic: topic
            })
        });


        // 4. 서버 응답을 JSON으로 변환
        const data = await response.json();


        // 5. API 오류 처리
        if (!response.ok) {
            throw new Error(
                data.error || "아이디어 생성에 실패했습니다."
            );
        }


        // 6. AI 결과 화면 출력
        resultText.textContent = data.result;


    } catch (error) {

        console.error("SparkIdea AI Error:", error);

        resultText.textContent =
            "⚠️ 아이디어를 생성하지 못했습니다. 잠시 후 다시 시도해주세요.";

    } finally {

        // 7. 버튼 원래 상태로 복구
        generateButton.disabled = false;
        generateButton.textContent = "✨ 아이디어 생성하기";

    }

});