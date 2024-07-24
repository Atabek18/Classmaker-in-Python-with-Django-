document.addEventListener('DOMContentLoaded', function() {
  const addQuestionButton = document.getElementById('add-question');
  const questionForm = document.getElementById('question-form');
  const questionsContainer = document.getElementById('questions-container');

  addQuestionButton.addEventListener('click', function() {
    const questionText = document.getElementById('question-text').value;
    const optionA = document.getElementById('id_text-A').value;
    const optionB = document.getElementById('id_text-A').value;
    const optionC = document.getElementById('option-c').value;
    const optionD = document.getElementById('option-d').value;

    const questionHTML = `
      <div class="question">
        <h3>${questionText}</h3>
        <ul>
          <li>${optionA}</li>
          <li>${optionB}</li>
          <li>${optionC}</li>
          <li>${optionD}</li>
        </ul>
      </div>
    `;

    questionsContainer.innerHTML += questionHTML;

    // Clear input fields
    questionForm.reset();
  });
});
