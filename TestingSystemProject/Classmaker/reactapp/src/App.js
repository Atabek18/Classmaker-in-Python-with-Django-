import React, { useState, useEffect } from "react";
import "./App.css";
import { useSelector, useDispatch } from "react-redux";

import End from "./components/End";
import Question from "./components/Question";
import Start from "./components/Start";
import UserInfoForm from "./components/UserRegister"
import quizData from "./data/quiz.json";
import { Router } from "react-router-dom";
import Login from './components/Login';

let interval;

const App = () => {
  const dispatch = useDispatch();
  const { step, answers } = useSelector((state) => state?.quizReducer);
  const [showModal, setShowModal] = useState(false);
  const [time, setTime] = useState(0);
  useEffect(() => {
    if (step === 4) {
      clearInterval(interval);
    }
  }, [step]);

  return (
    <div className="App">
      {step === 1 && <UserInfoForm />}
      {step === 2 && <Start />}
      {step === 3 && <Question />}
      {step === 4 && (
        <End
          data={quizData.data}
          time={time}
          onAnswersCheck={() => setShowModal(true)}
        />
      )}
    </div>
  );
};

export default App;


