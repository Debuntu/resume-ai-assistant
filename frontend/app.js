const API_URL =
    "https://4c5lt6d6hb.execute-api.us-east-1.amazonaws.com/analyze";


/* =========================================
   DOM Elements
========================================= */

const taskSelect =
    document.getElementById("task");

const taskDescription =
    document.getElementById("taskDescription");

const resumeInput =
    document.getElementById("resume");

const jobDescriptionInput =
    document.getElementById("jobDescription");

const analyzeButton =
    document.getElementById("analyzeBtn");

const loading =
    document.getElementById("loading");

const result =
    document.getElementById("result");

const resultContent =
    document.getElementById("resultContent");


/* =========================================
   Task Configuration
========================================= */

const taskConfig = {

    resume_analysis: {

        description:
            "Compare your resume against the job description and identify your strengths, missing skills, and areas for improvement.",

        button:
            "Analyze Resume",

        resumePlaceholder:
            "Paste your complete resume here...",

        jobPlaceholder:
            "Paste the complete job description here..."
    },


    cover_letter: {

        description:
            "Generate a customized professional cover letter based on your resume and the target job.",

        button:
            "Generate Cover Letter",

        resumePlaceholder:
            "Paste your complete resume here...",

        jobPlaceholder:
            "Paste the complete job description here..."
    },


    interview_questions: {

        description:
            "Generate technical and behavioral interview questions based on your resume and the target job.",

        button:
            "Generate Interview Questions",

        resumePlaceholder:
            "Paste your complete resume here...",

        jobPlaceholder:
            "Paste the complete job description here..."
    },


    ats_optimizer: {

        description:
            "Analyze your resume for ATS compatibility and identify keywords and improvements.",

        button:
            "Optimize Resume",

        resumePlaceholder:
            "Paste the resume you want to optimize here...",

        jobPlaceholder:
            "Paste the complete job description here..."
    }
};


/* =========================================
   Initialize UI
========================================= */

updateTaskUI();


/* =========================================
   Handle Task Selection
========================================= */

taskSelect.addEventListener(
    "change",
    updateTaskUI
);


function updateTaskUI() {

    const task =
        taskSelect.value;

    const config =
        taskConfig[task];


    taskDescription.textContent =
        config.description;


    analyzeButton.textContent =
        config.button;


    resumeInput.placeholder =
        config.resumePlaceholder;


    jobDescriptionInput.placeholder =
        config.jobPlaceholder;
}


/* =========================================
   Analyze / Generate Button
========================================= */

analyzeButton.addEventListener(
    "click",
    analyzeResume
);


async function analyzeResume() {

    const task =
        taskSelect.value;

    const resume =
        resumeInput.value.trim();

    const jobDescription =
        jobDescriptionInput.value.trim();


    if (!resume) {

        alert(
            "Please enter your resume."
        );

        return;
    }


    if (!jobDescription) {

        alert(
            "Please enter the job description."
        );

        return;
    }


    loading.classList.remove(
        "hidden"
    );

    result.classList.add(
        "hidden"
    );

    analyzeButton.disabled = true;


    try {

        console.log(
            "Sending request for task:",
            task
        );


        const response =
            await fetch(
                API_URL,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        task: task,

                        resume: resume,

                        jobDescription:
                            jobDescription

                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.message ||
                "API request failed"
            );
        }


        displayResult(
            task,
            data.result
        );


    } catch (error) {

        console.error(
            "API Error:",
            error
        );


        alert(
            "Something went wrong: " +
            error.message
        );


    } finally {

        loading.classList.add(
            "hidden"
        );

        analyzeButton.disabled =
            false;
    }
}


/* =========================================
   Display Result
========================================= */

function displayResult(
    task,
    resultData
) {

    switch (task) {

        case "resume_analysis":

            displayResumeAnalysis(
                resultData
            );

            break;


        case "cover_letter":

            displayCoverLetter(
                resultData
            );

            break;


        case "interview_questions":

            displayInterviewQuestions(
                resultData
            );

            break;


        case "ats_optimizer":

            displayATSOptimizer(
                resultData
            );

            break;


        default:

            resultContent.innerHTML =
                "<p>Unsupported task.</p>";
    }


    result.classList.remove(
        "hidden"
    );
}


/* =========================================
   Resume Analysis
========================================= */

function displayResumeAnalysis(data) {

    resultContent.innerHTML = `

        <div class="result-section">

            <h3>Match Score</h3>

            <div class="score">
                ${data.match_score}%
            </div>

        </div>


        <div class="result-section">

            <h3>Strengths</h3>

            ${createList(data.strengths)}

        </div>


        <div class="result-section">

            <h3>Missing Skills</h3>

            ${createList(data.missing_skills)}

        </div>


        <div class="result-section">

            <h3>Professional Summary</h3>

            <p>
                ${data.professional_summary}
            </p>

        </div>


        <div class="result-section">

            <h3>Recommendations</h3>

            ${createList(data.recommendations)}

        </div>
    `;
}


/* =========================================
   Cover Letter
========================================= */

function displayCoverLetter(data) {

    resultContent.innerHTML = `

        <div class="result-section">

            <h3>Generated Cover Letter</h3>

            <p>
                ${formatText(data.cover_letter)}
            </p>

        </div>


        <div class="result-section">

            <h3>Key Matches</h3>

            ${createList(data.key_matches)}

        </div>


        <div class="result-section">

            <h3>Customization Notes</h3>

            ${createList(
                data.customization_notes
            )}

        </div>
    `;
}


/* =========================================
   Interview Questions
========================================= */

function displayInterviewQuestions(data) {

    let questionsHTML = "";


    data.questions.forEach(
        (item, index) => {

            questionsHTML += `

                <div class="result-section">

                    <h3>
                        ${index + 1}.
                        ${item.question}
                    </h3>

                    <p>
                        <strong>
                            Category:
                        </strong>

                        ${item.category}
                    </p>

                    <p>
                        <strong>
                            Difficulty:
                        </strong>

                        ${item.difficulty}
                    </p>

                    <p>
                        <strong>
                            Why this question:
                        </strong>

                        ${item.reason}
                    </p>

                </div>
            `;
        }
    );


    resultContent.innerHTML =
        questionsHTML;
}


/* =========================================
   ATS Optimizer
========================================= */

function displayATSOptimizer(data) {

    resultContent.innerHTML = `

        <div class="result-section">

            <h3>ATS Score</h3>

            <div class="score">
                ${data.ats_score}%
            </div>

        </div>


        <div class="result-section">

            <h3>Keywords to Add</h3>

            ${createList(
                data.keywords_to_add
            )}

        </div>


        <div class="result-section">

            <h3>Keywords to Remove</h3>

            ${createList(
                data.keywords_to_remove
            )}

        </div>


        <div class="result-section">

            <h3>Resume Improvements</h3>

            ${createList(
                data.resume_improvements
            )}

        </div>


        <div class="result-section">

            <h3>Optimized Summary</h3>

            <p>
                ${data.optimized_summary}
            </p>

        </div>
    `;
}


/* =========================================
   Helper Functions
========================================= */

function createList(items) {

    if (
        !items ||
        items.length === 0
    ) {

        return "<p>None identified.</p>";
    }


    return `

        <ul>

            ${items
                .map(
                    item =>
                        `<li>${item}</li>`
                )
                .join("")}

        </ul>
    `;
}


function formatText(text) {

    if (!text) {
        return "";
    }


    return text.replace(
        /\n/g,
        "<br>"
    );
}