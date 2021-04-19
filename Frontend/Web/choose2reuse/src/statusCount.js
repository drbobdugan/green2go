import './App.css';
import React,{Component, useState} from 'react';
import axios from 'axios';
import './table.css';
import { useHistory } from "react-router-dom";


function StatusCount (props) {
        const [containers, setContainers] = useState({})
        const [filteredContainers, setFilteredContainers] = useState({})
        const [selected, setSelected] = useState()
        const [limit, setLimit] = useState(20)
        const history = useHistory();
        const [checkedOut, setCheckedOut] = useState()
        const [inStock, setInStock] = useState()
        const [pendingReturn, setPendingReturn] = useState()

        function select(container){
          console.log(container)
          setSelected(container)
         }
        
        async function getContainers(email, authToken){
         var response = await axios.get('http://198.199.77.174:5000/getCounts?email='+email+'&auth_token='+authToken)
         console.log(response.data.data)
         setCheckedOut(response.data.data["Checked Out"].length)
         setInStock(response.data.data["In Stock"].length)
         setPendingReturn(response.data.data["Pending Returns"].length)
        }

        if(Object.keys(containers).length == 0 && props.location && props.location.state){
            getContainers(props.location.state.email,props.location.state.authToken)
        }else if(!props.location || !props.location.state){
            history.push("/login");
        }

        return (
            <div className="App">
            <h1>Container Status Counts</h1>
            <div>
                <h2>Number of Containers Currently Checked Out</h2>
                <h1>{checkedOut}</h1>
            </div>
            <div>
                <h2>Number of Containers Currently Pending Return</h2>
                <h1>{pendingReturn}</h1>
            </div>
            <div>
                <h2>Number of Containers Currently In Stock</h2>
                <h1>{inStock}</h1>
            </div>
           </div>    
        )
}

export default StatusCount