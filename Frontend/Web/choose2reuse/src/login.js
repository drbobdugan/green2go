import './App.css';
import React,{Component, useState} from 'react';
import axios from 'axios';
import { useHistory } from "react-router-dom";
import logo from './logo.jpg';

function Login (props) {
    const history = useHistory();

    function routeChange(token) { 
    let path = `/table`; 
    //passes email and authToken values to props param in table.js
    history.push(path,{email:email,authToken:token});
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
        try{
        var response = await axios.post('198.199.77.174:5002/login', obj)
        var user_response = await axios.get('http://198.199.77.174:5002/getUser?email='+ email + '&auth_token=' + response.data.data.auth_token)
            if(response.data.success && user_response.data.data.role === 'Admin'){
                setAuthToken(response.data.data.auth_token)
                routeChange(response.data.data.auth_token)
            }else{
                alert(response.data.message)
            }
        }
        catch(error){
            alert("You do not have login privileges")
        }
       
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
            <div>
                <img src={logo} width="25%" height="100%"/>
            </div>
            <h1>Login</h1>
            <form id="form">
                <p>Email:  <input placeholder="Email" type="text" name="email" value={email} onChange={(event) => {setEmail(event.target.value)} } /> </p>
                <p>Password:  <input placeholder="Password" type="password" name="password" value={password} onChange={(event) => {setPassword(event.target.value)} } /> </p>
                <input type="button" name="submit" value="submit" onClick={() => { loginToEmail() } }/>
            </form>
            {authToken
            ? authTokenResponse()
            : null
            }
        </div>
        );
}

export default Login
