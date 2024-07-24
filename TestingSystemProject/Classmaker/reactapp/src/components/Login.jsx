import React from "react";

const Login = () => {
  return (
    <div>
      <h1>Hellow going</h1>
    </div>
  );
};
const Rigester = () => {
  return (
    <div>
      <input type="text" placeholder="rigester" />
    </div>
  );
};

const Button = () => {
  return (
    <div>
      <button>Button</button>
    </div>
  );
};

function Login1() {
  return (
    <div className="term">
      <Login />
      <Rigester />
      <Button />
    </div>
  );
}

export default Login1;

