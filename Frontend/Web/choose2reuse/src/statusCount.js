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
        const [description, setDescription] = useState()
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
            getContainers(email,authToken)
        }

        async function removeLocation(qr_code){
            const obj = {email: email, qrcode: qr_code, auth_token: authToken};
            var response = await axios.delete('http://198.199.77.174:5000/deleteLocation', obj)
            getContainers(email,authToken)
        }

        async function addLocation(description,location_qrcode){
            const obj = {location_qrcode: location_qrcode, email: email, auth_token: authToken, description: description};
            var response = await axios.post('http://198.199.77.174:5000/addLocation', obj)
            console.log(response)
            getContainers(email,authToken)
        }

        async function updateLocation(qr_code){
            const obj = {email: email, qrcode: qr_code, auth_token: authToken};
            var response = await axios.patch('http://198.199.77.174:5000/updateLocation', obj)
            console.log(response)
            getContainers(email,authToken)
        }

        function select(container){
          setSelected(container)
         }
        
        
        async function getLocationInfo(email, authToken){
            var response2 = await axios.get('http://198.199.77.174:5000/locationList?email='+email+'&auth_token='+authToken)
            //console.log(response2)
            if(locInfo.length == 0)
            {
               setNumLocations(response2.data.data)
               var l = numLocations
               for(const j of l)
               {
                   locationQRCode.push(j.location_qrcode)
                   locationDescription.push(j.description)
                   lastPickup.push(j.lastPickip)
                   count.push(j.count)
                   locInfo.push([j.location_qrcode,j.description,j.lastPickip,j.count])
               }
            }   
        }
        
        
         
        async function getContainers(email, authToken){
         var response = await axios.get('http://198.199.77.174:5000/getCounts?email='+email+'&auth_token='+authToken)
         console.log(response.data)
            setRetrieved(true)
            setCheckedOut(response.data.data["Checked Out"].length)
            //getting undefined error from setCheckedOut() line
            setInStock(response.data.data["In Stock"].length)
            setPendingReturn(response.data.data["Pending Returns"].length)
            //getLocationInfo(email,authToken)
        }

        if(locationQRCode.length == 0 && !retrieved && props.location && props.location.state){
            getContainers(props.location.state.email,props.location.state.authToken)
        }else if(!props.location || !props.location.state){
            history.push("/login");
        }

        function newLoc_qr(){
            if(locInfo.length < 9){
                setNewLoc_QR('L00' + (locInfo.length+1))
            }else if(locInfo.length > 8){
                setNewLoc_QR('L0' + (locInfo.length+1))
            }
        }

//NEED TO MAP ARRAYS TO LOCATION TABLE
        function displayLocationCounts(){
            return(
                <div className = "locationtable">
                <table className="locationcounts">
                    <thead>
                    <tr>
                      <th>Location</th>
                      <th>Number of Containers</th>
                      <th>Clear Containers</th>
                      <th>Last Cleared</th>
                      <th>Remove Location</th>
                    </tr>
                    </thead>
                <tbody>
                    {locInfo.map((elem)=>(
                    <tr>
                        <td>{elem[1]}</td> 
                        <td>{elem[3]}</td>
                        <td><input type='button' value='Clear' /*onClick ={() => {clearLocation(elem[0])}}*//></td>
                        <td>{elem[2]}</td>
                        <td><input type='button' value='Remove' /*onClick ={() => {removeLocation(elem[0])}}*//></td>
                    </tr>
                    ))}
                </tbody>
             </table>
             <table className="addLocation">
                    <thead>
                    <tr>
                      <th>Location Name</th>
                      <th>Add Location</th>
                    </tr>
                    </thead>
                <tbody>
                    <tr>
                        <td><input type='text' onChange= {description => setDescription(description)}/></td> 
                        <td><input type='button' value='Add' onClick ={newLoc_qr(), () => {updateLocation(description, newLoc_QR)}}/></td>
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
            <h1>Container Status Counts</h1>
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
             <h1>Location Status Counts</h1>
            {displayLocationCounts()}
           </div>    
        )
}

export default StatusCount