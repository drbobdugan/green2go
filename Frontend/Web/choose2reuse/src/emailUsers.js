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
        const [users, setUsers] = useState([])
        const [filteredUsers, setFilteredUsers] = useState([])
        const [selected, setSelected] = useState()
        const [limit, setLimit] = useState(20)
        const [checked, setChecked] = React.useState(true);

        var dict = {};

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

        function onChangeChecked(email){
            console.log(dict.email)
            if(dict.email == true){
                console.log("Changed from true to false")
                dict.email = false;
            }
            else if(dict.email==false){
                console.log("Changed to true from false")
                dict.email = true;
            }
            console.log(dict.email)
        }

        function copyToClipboard(e) {
            navigator.clipboard.writeText(getSelectedUsers())
        }

        function getSelectedUsers(){
            //iterate through dict, if something is true then add it to a string, return the string
            const copied = "";
            for (var key in dict) {
                if (dict.key==true){
                    console.log(key)
                    copied.append(key+",")
                }
            }
        }

        if(props.location && props.location.state && !email){
            setEmail(props.location.state.email);
            setAuthToken(props.location.state.authToken);
        }

        try{
            if(users.length === 0 && props.location && props.location.state){
                getUsers(props.location.state.email,props.location.state.authToken).then( _ => {
                    //initialize users selected checkboxes to all false
                    {users.map((elem)=>(
                        console.log(dict.elem.email)
                    ))}
                })
            }
            else if(!props.location || !props.location.state){
            history.push("/login");
            }
        }
        catch(error) {
            history.push('/login')
        }

        //initialize users selected checkboxes to all false
        //{filteredUsers.map((elem)=>(
        //    dict.elem.email=false
        //))}
        return (
            <div className="App">
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
                <input type="button" value="Copy to Clipboard" onClick={() => copyToClipboard()}></input>
                <br></br>
                <br></br>
                <br></br>
                <div className = "containertable">
                <table className="centerone">
                    <thead>
                        <tr>
                            <th>Select</th>
                            <th>Email</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredUsers.map((elem)=>(
                            <tr onClick={()=>{select(elem)}}>
                            <td><input type="checkbox" checked="false" onChange={() => onChangeChecked(elem.email)} /></td>
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