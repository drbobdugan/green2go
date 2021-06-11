import './App.css';
import React,{Component, useState} from 'react';
import axios from 'axios';
import './table.css';
import { useHistory } from "react-router-dom";
import logo from './logo.jpg';

function EmailUsers (props) {
        const [locations, setLocations] = useState([])
        const history = useHistory();
        const [email,setEmail] = useState()
        const [authToken,setAuthToken] = useState()
        const [users, setUsers] = useState([])
        const [filteredUsers, setFilteredUsers] = useState([])
        const [selected, setSelected] = useState()
        const [limit, setLimit] = useState(20)

        function backPage(){
            history.goBack()
        }

        function select(user){
            console.log(user)
            setSelected(user)
        }

        async function getUsers(email, authToken){
            //need to add get users route
            var response = await axios.get('http://198.199.77.174:5000/getAllUsers?email='+email+'&auth_token='+authToken)
            console.log(response)
            setUsers(response.data.data)
            setLimit(users.length)
            console.log(response)
            try{
             setFilteredUsers(response.data.data.slice(0,limit))
            }
            catch (error) {
             history.push('/login')
           }
        }

        function toggleLimit(){
            if(limit == 20){
              setLimit(users.length)
              setFilteredUsers(users)
            }else{
              setLimit(20)
              setFilteredUsers(users.slice(0,20))
            }
          }
  
          function filterBySearch(e) {
            var filter = e.target.value
            console.log(filter) 
            if(filter === ""){
              setFilteredUsers(users.slice(0,limit))
            }else{    
            setFilteredUsers(users.filter(user => {
              if(user.email != null){
              return(
                user.email.includes(filter)
              )
              }
            }))
          }
        }

        
        async function copyToClipboard(e) {
            console.log("copying all users to clipboard")

            var response = await axios.get('http://198.199.77.174:5000/getAllUsers?email='+email+'&auth_token='+authToken)
            //format all users into a string that can be inputted into an email
            var usersFormattedEmail="";
            var i;
            for(i=0; i<response.data.data.length; i++){
                usersFormattedEmail+=response.data.data[i].email+",";
            }
            if(usersFormattedEmail.length!=0){
                usersFormattedEmail=usersFormattedEmail.slice(0,-1);
            }
            console.log(usersFormattedEmail);

            window.alert("Copy the following text:"+"\n"+usersFormattedEmail)
        }     

        if(props.location && props.location.state && !email){
            setEmail(props.location.state.email);
            setAuthToken(props.location.state.authToken);
        }

        try{
            if(users.length === 0 && props.location && props.location.state){
                getUsers(props.location.state.email,props.location.state.authToken)
            }
            else if(!props.location || !props.location.state){
                history.push("/login");
            }
        }
        catch(error) {
            history.push('/login')
        }
        return (
            <div className="App">
            <div>
                <img src={logo} width="25%" height="100%"/>
            </div>
                <div className ="back">
                    <input type='button' value='Back' onClick={() => {backPage()}}/>
                </div>
                <br></br>
                <br></br>
                <div className="title">
                    <h1>Email Users</h1>
                </div>
                <br></br>
                <br></br>
                <input type="text" placeholder="Search for anything.." onChange={filterBySearch}></input>
                <input type="button" value="Toggle Limit" onClick={() => {toggleLimit()}}></input>
                <br></br>
                <br></br>
                <input type="button" value="Copy all users to clipboard" onClick={() => copyToClipboard()}></input>
                <br></br>
                <br></br>
                <br></br>
                <div className = "containertable">
                <table className="centerone">
                    <thead>
                        <tr>
                            <th>Email</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredUsers.map((elem)=>(
                            <tr onClick={()=>{select(elem)}}>
                            <td>{elem.email}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                </div>
           </div>    
        )
}

export default EmailUsers