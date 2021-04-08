import './App.css';
import React,{Component, useState} from 'react';
import axios from 'axios';
import './table.css';


function Table (props) {
        const [containers, setContainers] = useState([])
        const [selected, setSelected] = useState()

        function select(container){
         console.log(container)
         setSelected(container)
        }
        
        async function getContainers(email, authToken){
         var response = await axios.get('http://198.199.77.174:5000/getallContainers?email='+email+'&auth_token='+authToken)
         setContainers(response.data.data)
        }

        if(containers.length == 0 && props.location && props.location.state)
        getContainers(props.location.state.email,props.location.state.authToken)

        return (
            <div className="App">
            <hi>hasContainer Table</hi>
            <table className="table table-hover table-dark">
            <thead>
             <tr>
               <th>Email</th>
               <th>QR Code</th>
               <th>Status</th>
               <th>Status Update Time</th>
               <th>Location QR Code</th>
               <th>Active</th>
               <th>Description</th>
               
             </tr>
             </thead>
             <tbody>
               {containers.map((elem)=>(
                <tr onClick={()=>{select(elem)}}>
                 <td>{elem.email}</td>
                 <td>{elem.qrcode}</td>
                 <td>{elem.status}</td>
                 <td>{elem.statusUpdateTime}</td>
                 <td>{elem.location_qrcode}</td>
                 <td>{elem.active}</td>
                 <td>{elem.description}</td>
                </tr>
               ))}
                </tbody>
             </table>
           </div>    
        )
}

export default Table
