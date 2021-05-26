import './App.css';
import React,{Component, useState} from 'react';
import axios from 'axios';
import './table.css';
import { useHistory } from "react-router-dom";

function StatusCount (props) {
        const [locations, setLocations] = useState([])
        const [retrieved, setRetrieved] = useState(false)
        const [selected, setSelected] = useState()
        const history = useHistory();
        const [description, setDescription] = useState('')
        const [loc_qr, setLoc_qr] = useState('')
        const [newLoc_QR, setNewLoc_QR] = useState()
        const [checkedOut, setCheckedOut] = useState()
        const [inStock, setInStock] = useState()
        const [pendingReturn, setPendingReturn] = useState()
        const [email,setEmail] = useState()
        const [authToken,setAuthToken] = useState()
        const [locationQRCode,setLocationQRCode] = useState([])
        const [locationDescription,setLocationDescription] = useState([])
        const [lastPickup,setLastPickup] = useState([])
        const [count,setCount] = useState([])
        const [numLocations,setNumLocations] = useState([])
        const [locInfo,setLocInfo] = useState([])

        if(props.location && props.location.state && !email){
            setEmail(props.location.state.email);
            setAuthToken(props.location.state.authToken);
        }

        async function clearLocation(qr_code){
            const obj = {email: email, qrcode: qr_code, auth_token: authToken};
            var response = await axios.patch('http://198.199.77.174:5000/clearLocation', obj)
            getLocationInfo(email,authToken)
        }

        async function removeLocation(qr_code){
            
            const obj = {email: email, qrcode: qr_code, auth_token: authToken};
            console.log(obj)
            var response = await axios.post('http://198.199.77.174:5000/deleteLocation', obj)
            console.log(response)
            getLocationInfo(email,authToken)
        }

        async function addLocation(description,location_qrcode){
            const obj = {location_qrcode: location_qrcode, email: email, auth_token: authToken, description: description};
            var response = await axios.post('http://198.199.77.174:5000/addLocation', obj)
            console.log(response)
            await getLocationInfo(email,authToken)
            setLoc_qr('')
            setDescription('')
        }

        async function updateLocation(qr_code){
            const obj = {email: email, qrcode: qr_code, auth_token: authToken};
            //var response = await axios.patch('http://198.199.77.174:5000/updateLocation', obj)
            //console.log(response)
            getLocationInfo(email,authToken)
        }

        function select(container){
          setSelected(container)
         }
        
        
        async function getLocationInfo(email, authToken){
            var response = await axios.get('http://198.199.77.174:5000/locationList?email='+email+'&auth_token='+authToken)
            console.log(response.data.data)
            if(response && response.data && response.data.data)
            {
                setLocations(response.data.data)
            }
        }
        
        if(locations.length == 0 && props.location && props.location.state){
            getLocationInfo(props.location.state.email,props.location.state.authToken)
        }else if(!props.location || !props.location.state){
            history.push("/login");
        }

//NEED TO MAP ARRAYS TO LOCATION TABLE
        function displayLocationCounts(){
            return(
                <div className = "locationtable">
                <table className="locationcounts">
                    <thead>
                    <tr>
                      <th>Location QR Code</th>
                      <th>Location</th>
                      <th>Number of Containers</th>
                      <th>Clear Containers</th>
                      <th>Last Cleared</th>
                      <th>Remove Location</th>
                    </tr>
                    </thead>
                <tbody>
                    {locations.map((elem)=>(
                        <tr onClick={()=>{select(elem)}}>
                        <td>{elem.location_qrcode}</td>
                        <td>{elem.description}</td>
                        <td>{elem.count}</td>
                        <td><input type='button' value='Clear' onClick ={() => {clearLocation(elem.location_qrcode)}}/></td>
                        <td>{elem.lastPickip}</td>
                        <td><input type="button" value="Remove" onClick ={() => { if (window.confirm('Are you sure you wish to remove this location?'))  removeLocation(elem.location_qrcode)} }/></td>

                        </tr>
                    ))}
                    <tr>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td><input type='button' value='Clear All' onClick ={() => {locations.map((elem)=>{clearLocation(elem.location_qrcode)})}}/></td>
                    <td></td>
                    <td></td>
                    </tr>
                </tbody>
             </table>
             <table className="addLocation">
                    <thead>
                    <tr>
                      <th>Location QR Code</th>
                      <th>Location Name</th>
                      <th>Add Location</th>
                    </tr>
                    </thead>
                <tbody>
                    <tr>
                        <td><input type='text' value={loc_qr} placeholder="qr_code" onChange={event => setLoc_qr(event.target.value)}/></td> 
                        <td><input type='text' value={description} placeholder="description" onChange={event => setDescription(event.target.value)}/></td> 
                        <td><input type='button' value='Add' onClick ={() => {addLocation(description, loc_qr)}}/></td>
                    </tr>
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
            <div className ="back">
                <input type='button' value='Back' onClick={() => {backPage()}}/>
            </div>
             <h1>All Locations</h1>
            {displayLocationCounts()}
           </div>    
        )
}

export default StatusCount