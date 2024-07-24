import {QUIZ_START , QUIZ_RESET , QUIZ_NEXT,QUIZ_SUBMIT, QUIZ_PREV , QUIZ_TIMEOUT, QUIZ_REGISTER} from '../constant/quizConstant'

const initialState = {
    step : 1,
    activePage: 0,
    answers: [],
    time: 60
}

const quizReducer = (state = initialState , action) =>{
    const {type , payload} = action
    switch (type) {
        case QUIZ_REGISTER:
            return {
                ...state, step:2
            }
        case QUIZ_START:
            return {
                ...state,step:3
            }
        case QUIZ_NEXT:
            return{
                ...state,answers: [...payload],activePage: state?.activePage+1
            }
        case QUIZ_SUBMIT:
            return{
                ...state,step:4,answers:[...payload?.answers] , time: payload?.time
            }
        case QUIZ_RESET:
            return{
                ...state,step:1,activePage:0,answers:[], time: 60
            }
        case QUIZ_PREV:
            return{
                ...state,activePage:state?.activePage-1
            }
        case QUIZ_TIMEOUT:
            return{
                ...state, time: 0,step:4
            }
        default:
            return state;
    }
}

export default quizReducer;