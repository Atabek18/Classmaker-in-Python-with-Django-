import React, { useState } from 'react';
import axios from 'axios';
import { useDispatch, useSelector } from "react-redux";
import { register } from '../redux/action/quizAction';
const UserInfoForm = ({ }) => {
  const dispatch = useDispatch();
  const handleQuizRegister = () => {
    dispatch(register());
  };
  const [formData, setFormData] = useState({
    name: '',
    surname: '',
    email: '',
    phone_number: '',
    season_number: '',
    season_type: '',
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    handleQuizRegister();
    try {
      const response = await axios.post(`http://127.0.0.1:8000/api/user-register?quiz_id=6D6f4E73ACE2A6C951D2`, formData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const register_responseData = response.data;
      const jwtToken = register_responseData.token;
      const expirationDate = new Date();
      expirationDate.setTime(expirationDate.getTime() + 60 * 60 * 1000);
      document.cookie = `jwtToken=${jwtToken}; expires=${expirationDate.toUTCString()}; path=/;`;

      console.log('Registration successful:', register_responseData);
    } catch (error) {
      console.error('Error registering user:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="form-horizontal">
      <input type="text" name="name" value={formData.name} onChange={handleInputChange} placeholder="Name" />
      <input type="text" name="surname" value={formData.surname} onChange={handleInputChange} placeholder="Surname" />
      <input type="email" name="email" value={formData.email} onChange={handleInputChange} placeholder="Email" />
      <input type="text" name="phone_number" value={formData.phone_number} onChange={handleInputChange} placeholder="Phone Number" />
      <input type="text" name="season_number" value={formData.season_number} onChange={handleInputChange} placeholder="Season Number" />
      <input type="text" name="season_type" value={formData.season_type} onChange={handleInputChange} placeholder="Season Type" />
      <button type="submit" >Submit</button>
    </form>
  );
};

export default UserInfoForm;
