import './App.css';
import React,{Component, useState} from 'react';
import axios from 'axios';
import { useHistory } from "react-router-dom";

function Login (props) {
    const history = useHistory();

    const routeChange = () =>{ 
    let path = `/table`; 
    history.push(path);
    }
    // creates getter and setter methods
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [authToken, setAuthToken] = useState()

    async function loginToEmail () {
        const obj = {
            'email' : email,
            'password' : password
        }
        var response = await axios.post('http://198.199.77.174:5000/login', obj)
        setAuthToken(response.data.data.auth_token)
    }

    // you can return other html components encapsulated in a function
    function authTokenResponse() {
        return (
            <div>
                <strong>{authToken}</strong>
            </div>
        )
    }

    return (
        <div className="App">
            <hi>Login</hi>
            <form id="form">
                <p>Email:  <input placeholder="Email" type="text" name="email" value={email} onChange={(event) => {setEmail(event.target.value)} } /> </p>
                <p>Password:  <input placeholder="Password" type="password" name="password" value={password} onChange={(event) => {setPassword(event.target.value)} } /> </p>
                <input type="button" name="submit" value="submit" onClick={() => { loginToEmail() } } onClick={() => { routeChange() }}/>
            </form>
            {authToken
            ? authTokenResponse()
            : null
            }
        </div>
        );
}

export default Login
