import './App.css';
import React,{Component, useState} from 'react';
import axios from 'axios';
import './table.css';
import { useHistory } from "react-router-dom";


function StatusCount (props) {
        const [locations, setLocations] = useState([])
        const [selected, setSelected] = useState()
        const history = useHistory();
        const [checkedOut, setCheckedOut] = useState()
        const [inStock, setInStock] = useState()
        const [pendingReturn, setPendingReturn] = useState()

        function select(container){
          setSelected(container)
         }
        
        async function getContainers(email, authToken){
         var response = await axios.get('http://198.199.77.174:5000/getCounts?email='+email+'&auth_token='+authToken)
         if(Object.keys(locations).length == 0)
         {
            var l = response.data.data["In Bin"]
            var temp_dict = {}
            for(const i of l)
            {
                if(i['location_qrcode'] in temp_dict)
                {
                    temp_dict[i['location_qrcode']] +=1
                }
                else{
                    temp_dict[i['location_qrcode']] = 1
                }
            }
            var to_arr = []
            for(const key in temp_dict)
            {
                to_arr.push([key, temp_dict[key]])
            }
            setLocations(to_arr)
            setCheckedOut(response.data.data["Checked Out"].length)
            setInStock(response.data.data["In Stock"].length)
            setPendingReturn(response.data.data["Pending Returns"].length)
         }
        }

        if(locations.length == 0 && props.location && props.location.state){
            getContainers(props.location.state.email,props.location.state.authToken)
        }else if(!props.location || !props.location.state){
            history.push("/login");
        }

        function displayLocationCounts(){
            return(
                <div className = "locationtable">
                <table className="locationcounts">
                    <thead>
                    <tr>
                      <th>Location</th>
                      <th>Number of Containers</th>
                      <th>Clear Containers</th>
                    </tr>
                    </thead>
                <tbody>
                    {locations.map((elem)=>(
                    <tr>
                        <td>{elem[0]}</td> 
                        <td>{elem[1]}</td>
                        <td><input type='button' value='Clear'/></td>
                    </tr>))}
                </tbody>
             </table>
             </div>   
            )
        }

        function backPage(){
            history.goBack()
        }
        

        return (
            <div className="App">
            <h1>Container Status and Location Counts</h1>
            <div className ="back">
                <input type='button' value='Back' onClick={() => {backPage()}}/>
            </div>
            <div className = "statustable">
                <table className="statuscounts">
                    <thead>
                    <tr>
                      <th>Status</th>
                      <th>Quantity</th>
                    </tr>
                    </thead>
                <tbody>
                    <tr>
                        <td>Checked Out</td> 
                        <td>{checkedOut}</td>
                    </tr>
                    <tr>
                        <td>Pending Return</td> 
                        <td>{pendingReturn}</td>
                    </tr>
                    <tr>
                        <td>In Stock</td> 
                        <td>{inStock}</td>
                    </tr>
                </tbody>
             </table>
             </div> 
            {displayLocationCounts()}
           </div>    
        )
}

export default StatusCount