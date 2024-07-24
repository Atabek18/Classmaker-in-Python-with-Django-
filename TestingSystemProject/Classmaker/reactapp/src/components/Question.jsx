import React, { useState, useEffect, useRef } from "react";
import { useSelector, useDispatch } from "react-redux";
import axios from 'axios';
import {
  nextQuiz,
  prevQuiz,
  submitQuiz,
  timeOut,
} from "../redux/action/quizAction";
import quizData from "../data/quiz.json";

// const useFetchCsrfToken = () => {
//   const [csrfToken, setCsrfToken] = useState('');

//   useEffect(() => {
//     const fetchCsrfToken = async () => {
//       try {
//         const response = await fetch('http://127.0.0.1:8000/api/get-csrf-token/');
//         const data = await response.json();
//         setCsrfToken(data.csrftoken);
//       } catch (error) {
//         console.error('Error fetching CSRF token:', error);
//       }
//     };

//     fetchCsrfToken();
//   }, []);

//   return csrfToken;
// };

// const useFetchQuizData = (csrfToken) => {
//   const [quizData, setQuizData] = useState(null);
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     const fetchData = async () => {
//       if (!csrfToken) return;
//       const payload = { csrfmiddlewaretoken: csrfToken }
//       try {
//         const response = await axios.post(
//           'http://127.0.0.1:8000/api/init_test/',
//           payload,
//           {
//             params: { quiz_id: '6D6f4E73ACE2A6C951D2' },
//             headers: {
//               'Content-Type': 'application/json',
//               'X-CSRFToken': csrfToken,
//             },
//           }
//         );

//         setQuizData(response.data);
//         setLoading(false);
//       } catch (error) {
//         console.error('Error fetching quiz data:', error);
//         setLoading(false);
//       }
//     };

//     fetchData();
//   }, [csrfToken]);

//   return { quizData, loading };
// };

// const Question = () => {
//   const csrfToken = useFetchCsrfToken();
//   const { quizData, loading } = useFetchQuizData(csrfToken);

//   return (
//     <div>
//       <h2>Quiz Results</h2>
//       {loading ? (
//         <p>Loading quiz data...</p>
//       ) : quizData ? (
//         <>
//           <p>Score: {quizData.score}</p>
//           <p>Feedback: {quizData.feedback}</p>
//         </>
//       ) : (
//         <p>Failed to load quiz data.</p>
//       )}
//     </div>
//   );
// };

// export default Question;






const Question = () => {
  const dispatch = useDispatch();
  const { activePage, answers, time } = useSelector(
    (state) => state?.quizReducer
  );
  const [data, setData] = useState(quizData?.data?.pages[activePage].contents[0]);
  const [error, setError] = useState("");
  const [selected, setSelected] = useState("");
  const [timer, setTimer] = useState(time);

  useEffect(() => {
    if (timer > 0) {
      setTimeout(() => setTimer(timer - 1), 1000);
    } else {
      dispatch(timeOut());
    }
  }, [timer]);
  const radiosWrapper = useRef();
  useEffect(() => {
    setData(quizData?.data?.pages[activePage].contents[0]);
    if (answers[activePage] != undefined) {
      setSelected(answers[activePage].a);
      console.log("Run once");
    }
  }, [data, activePage]);
  const changeHandler = (e) => {
    setSelected(e.target.value);
    if (error) {
      setError("");
    }
  };
  const handlePrev = () => {
    setError("");
    dispatch(prevQuiz());
  };
  const handleNext = (e) => {
    if (selected === "") {
      return setError("Please select one option!");
    }
    let ans = [...answers];
    ans[activePage] = {
      q: data.question,
      a: selected,
    };
    console.log(ans);
    dispatch(
      nextQuiz({
        answers: ans,
      })
    );
    setSelected("");
    const findCheckedInput =
      radiosWrapper.current.querySelector("input:checked");
    if (findCheckedInput) {
      findCheckedInput.checked = false;
    }
  };
  const handleSubmit = () => {
    if (selected === "") {
      return setError("Please select one option!");
    }
    dispatch(
      submitQuiz({
        answers: [
          ...answers,
          (answers[activePage] = {
            q: data.question,
            a: selected,
          }),
        ],
        time: time - timer,
      })
    );
  };

  return (
    <div className="questionBox">
      <section className="questionHead">
        <h3>
          Question {activePage + 1}/{quizData?.data.length}
        </h3>
        <h5>{timer}</h5>
      </section>
      <section className="middleBox">
        <div className="question">
          <p>{data?.question}</p>
          {error && <div>{error}</div>}
        </div>
        <div className="option" ref={radiosWrapper}>
          {data?.choices.map((choice, i) => (
            <label
              className={`${choice === selected ? `selected` : `text`}`}
              key={i}
            >
              <input
                type="radio"
                name="answer"
                value={choice}
                onChange={changeHandler}
                checked={choice === selected}
              />
              {choice}
            </label>
          ))}
        </div>
      </section>
      <section className="questionBottom">
        {activePage <= 0 ? null : (
          <button className="button" onClick={handlePrev}>
            Prev
          </button>
        )}

        {activePage + 1 >= quizData?.data?.pages.length ? (
          <button className="button nextBtn" onClick={handleSubmit}>
            Submit
          </button>
        ) : (
          <button className="button nextBtn" onClick={handleNext}>
            Next
          </button>
        )}
      </section>
    </div>
  );
};

export default Question;
