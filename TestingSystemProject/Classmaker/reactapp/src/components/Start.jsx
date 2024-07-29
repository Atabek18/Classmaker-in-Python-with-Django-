// import React, { useState } from "react";
// import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { startQuiz } from "../redux/action/quizAction";
// const Start = () => {
//   const dispatch = useDispatch();
//   // const {time} = useSelector(state => state.quizReducer)
//   const [minute, setMinute] = useState(1);
//   const [second, setSecond] = useState(0);
//   const [time, setTime] = useState(60);
//   const handleQuizStart = () => {
//     dispatch(startQuiz(time));
//   };
//   useEffect(() => {
//     if (minute > 59) {
//       setMinute(1);
//     }
//     if (second > 59) {
//       setSecond(1);
//     }
//   }, [minute, second]);
//   useEffect(() => {
//     console.log(minute);
//     console.log(typeof minute);
//     if (minute !== NaN && second !== NaN) {
//       setTime(minute * 60 + second);
//     }
//   }, [minute, second]);
//   return (
//     <div className="startBox">
//       <div>
//         <div>
//           <h1>Start the Quiz</h1>
//           <p>Good luck!</p>
//           <p>Time:&nbsp;&nbsp;{time}sec</p>
//           <section>
//             <label htmlFor="">
//               <input
//                 type="number"
//                 className="timeInput"
//                 value={minute}
//                 onChange={(e) => setMinute(parseInt(e.target.value))}
//               />
//               min
//             </label>
//             <label htmlFor="">
//               <input
//                 type="number"
//                 className="timeInput"
//                 value={second}
//                 onChange={(e) => setSecond(parseInt(e.target.value))}
//               />
//               sec
//             </label>
//           </section>
//           <button className="startButton" onClick={handleQuizStart}>
//             START
//           </button>
//         </div>
//       </div>
//     </div>
//   );
// };

// export default Start;

import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Start = ({}) => {
  const dispatch = useDispatch();
  const handleQuizStart = () => {
    dispatch(startQuiz());
  };
  const [startResponseData, setStartResponseData] = useState(null);
  const handleStartButtonClick = async () => {
    try {
      let header = null;
      const storedToken = document.cookie.replace(/(?:(?:^|.*;\s*)jwtToken\s*=\s*([^;]*).*$)|^.*$/, '$1');
      if (storedToken !== '' & storedToken !== null & storedToken !== undefined) {
          header = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${storedToken}`,
          };
      }
      const response = await axios.post(
        'http://127.0.0.1:8000/api/start/',
        {},
        {
          headers: header != null ? header : {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${storedToken}`
          },
        }
      );

      if (response.status === 200) {
        const startResponseData = response.data;
        const currentPage = startResponseData.data.test.current_page;
        const totalPage = startResponseData.data.test.total_page;

        setStartResponseData(startResponseData);
        const limitTime = startResponseData.settings.test.time_limits;
        const timeoutTimestamp = startResponseData.settings.test.timeout_timestamp;
        const remainingTime = startResponseData.settings.test.remaining_time;
        handleQuizStart();
        console.log(limitTime, timeoutTimestamp, remainingTime);
      } else {
        console.error('Error:', response.status);
      }
    } catch (error) {
      console.error('Network error occurred:', error);
    }
  };

  useEffect(() => {
    // Run animation logic after startResponseData is updated
    if (startResponseData) {
      // const limitTime = startResponseData.settings.test.time_limits;
      // const timeoutTimestamp = startResponseData.settings.test.timeout_timestamp;
      // const remainingTime = startResponseData.settings.test.remaining_time;

      // Initialize animation using the retrieved data
      // const animation = new LineBarAnimation(timeoutTimestamp, limitTime, remainingTime);
      // animation.startAnimation();
    }
  }, [startResponseData]); // Trigger effect when startResponseData changes

  return (
    <div>
      {/* Your component JSX goes here */}
      <button onClick={handleStartButtonClick} id="start-button">Start</button>
    </div>
  );
};

export default Start;
