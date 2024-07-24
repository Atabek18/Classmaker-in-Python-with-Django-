import React, { useState } from 'react';
import axios from 'axios';

const YourComponent = ({ testId, linkId, startResponseData, initResponseData, extractQuestionsFromPage, showQuestion, displaySetups }) => {
  const [currentPage, setCurrentPage] = useState(null);
  const [totalPages, setTotalPages] = useState(null);

  const getQuestionsAnswer = () => {
    const pageShown = document.querySelector('.page_shown');
    const currentId = pageShown?.id;
    const questionContainer = pageShown?.querySelector('#question-container');

    if (!currentId || !questionContainer) {
      return false;
    }

    const questions = questionContainer.querySelectorAll('.question');
    const question = questions[0]; // Assuming there's only one question per page

    if (!question) {
      return false;
    }

    const extractClass = question.className.split(' ');
    const questionType = extractClass[extractClass.length - 1];
    const extractId = question.id.match(/\d+/)[0];
    const selectedValue = question.querySelector(`input[name="question_${extractId}_${questionType}"]:checked`)?.value;

    if (!selectedValue) {
      return false;
    }

    const data = {
      csrfmiddlewaretoken: '{{ csrf_token }}', // Use your CSRF token here
      next_page: true, // Example value, modify as needed
      page: parseInt(currentId, 10),
      status: 'continue', // Example status, modify as needed
      answers: [
        {
          question_id: extractId,
          type: questionType,
          answer: selectedValue || '',
        }
      ]
    };

    return data;
  };

  const handleNextButtonClick = async () => {
    const data = getQuestionsAnswer();

    if (!data) {
      return;
    }

    try {
      const storedToken = document.cookie.replace(/(?:(?:^|.*;\s*)jwtToken\s*=\s*([^;]*).*$)|^.*$/, '$1');
      const response = await axios.post(
        `/api/continue/?test_id=${testId}&link_id=${linkId}`,
        data,
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${storedToken}`,
          },
        }
      );

      const continueResponseData = response.data;
      const testData = startResponseData || initResponseData;
      const currentPage = continueResponseData.data.test.current_page;
      const questionData = extractQuestionsFromPage(testData.data, currentPage);

      setCurrentPage(currentPage);
      setTotalPages(continueResponseData.data.test.total_pages);

      showQuestion(questionData, currentPage);
      displaySetups(currentPage, continueResponseData.data.test.total_pages, testData);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      {/* Your component JSX goes here */}
      <button onClick={handleNextButtonClick} id="next-button">Next</button>
    </div>
  );
};

export default YourComponent;
