import './App.css';
import React,{Component, useState} from 'react';
import axios from 'axios';
import './table.css';
import { useHistory } from "react-router-dom";

function EmailUsers (props) {
        const [locations, setLocations] = useState([])
        const history = useHistory();
        const [email,setEmail] = useState()
        const [authToken,setAuthToken] = useState()

        function backPage(){
            history.goBack()
        }

        if(props.location && props.location.state && !email){
            setEmail(props.location.state.email);
            setAuthToken(props.location.state.authToken);
        }

        if(locations.length == 0 && props.location && props.location.state){
        }else if(!props.location || !props.location.state){
            history.push("/login");
        }

        return (
            <div className="App">
            <div className ="back">
                <input type='button' value='Back' onClick={() => {backPage()}}/>
            </div>
             <h1>Email Users</h1>
           </div>    
        )
}

export default EmailUsers