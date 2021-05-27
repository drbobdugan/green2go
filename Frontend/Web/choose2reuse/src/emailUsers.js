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
            console.log(response)
            try{
             setFilteredUsers(response.data.data.slice(0,limit))
            }
            catch (error) {
             history.push('/login')
           }
           }

        if(props.location && props.location.state && !email){
            setEmail(props.location.state.email);
            setAuthToken(props.location.state.authToken);
        }

        try{
            if(users.length === 0 && props.location && props.location.state){
            getUsers(props.location.state.email,props.location.state.authToken)
            }else if(!props.location || !props.location.state){
              history.push("/login");
            }
        }
        catch(error) {
            history.push('/login')
        }
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