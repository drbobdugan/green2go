import './App.css';
import React,{Component, useState} from 'react';
import axios from 'axios';
import './table.css';
import { useHistory } from "react-router-dom";


function Table (props) {
        const [containers, setContainers] = useState([])
        const [filteredContainers, setFilteredContainers] = useState([])
        const [selected, setSelected] = useState()
        const [limit, setLimit] = useState(20)
        const history = useHistory();

        function routeChangeLocationCount() { 
        let path = `/locationCount`; 
        history.push(path);
        }
        function routeChangeStatusCount() { 
          let path = `/statusCount`; 
          history.push(path);
          }

        function select(container){
          console.log(container)
          setSelected(container)
         }
        
        async function getContainers(email, authToken){
         var response = await axios.get('http://198.199.77.174:5000/getallContainers?email='+email+'&auth_token='+authToken)
         setContainers(response.data.data)
         setFilteredContainers(response.data.data.slice(0,limit))
        }
        
        function filterByStatus(e) {
          var filter = e.target.value        
          if(filter !== 'All') 
          {
            if(filter == 'Checked Out')
            {
              setFilteredContainers(containers.filter(container => container.status == 'Checked Out'))
            }
            if(filter == 'Pending Return')
            {
              setFilteredContainers(containers.filter(container => container.status == 'Pending Return'))
            }
            if(filter == 'Verified Return')
            {
              setFilteredContainers(containers.filter(container => container.status == 'Verified Return'))
            }
            if(filter == 'Damaged Lost')
            {
              setFilteredContainers(containers.filter(container => container.status == 'Damaged Lost'))
            }
          }
          else
          {
            setFilteredContainers(containers)
          }
        }

        function toggleLimit(){
          if(limit == 20){
            setLimit(containers.length)
            setFilteredContainers(containers)
          }else{
            setLimit(20)
            setFilteredContainers(containers.slice(0,20))
          }
        }

        function filterBySearch(e) {
          var filter = e.target.value
          console.log(filter) 
          if(filter === ""){
            setFilteredContainers(containers.slice(0,limit))
          }else{    
          setFilteredContainers(containers.filter(container => {
            if(container.location_qrcode != null && container.description != null){
            return(
              container.email.includes(filter) || 
              container.qrcode.includes(filter) ||
              container.status.includes(filter) ||
              container.statusUpdateTime.includes(filter) ||
              container.location_qrcode.includes(filter) ||
              container.active.includes(filter) ||
              container.description.includes(filter)
            )
            }
            else if(container.location_qrcode == null && container.description != null){
              return(
                container.email.includes(filter) || 
                container.qrcode.includes(filter) ||
                container.status.includes(filter) ||
                container.statusUpdateTime.includes(filter) ||
                container.active.includes(filter) ||
                container.description.includes(filter)
              )
              }
              else if(container.location_qrcode != null && container.description == null){
                return(
                  container.email.includes(filter) || 
                  container.qrcode.includes(filter) ||
                  container.status.includes(filter) ||
                  container.statusUpdateTime.includes(filter) ||
                  container.active.includes(filter) ||
                  container.location_qrcode.includes(filter) 
                )
                }
                else if(container.location_qrcode == null && container.description == null){
                  return(
                    container.email.includes(filter) || 
                    container.qrcode.includes(filter) ||
                    container.status.includes(filter) ||
                    container.statusUpdateTime.includes(filter) ||
                    container.active.includes(filter)  
                  )
                  }
          }))
        }
        }

        if(containers.length === 0 && props.location && props.location.state){
        getContainers(props.location.state.email,props.location.state.authToken)
        }else if(!props.location || !props.location.state){
          history.push("/login");
        }
        return (
            <div className="App">
            <h1>All Container Transactions</h1>
            <div className="row">
              <div className="column"><button type="button" onClick={() => { routeChangeLocationCount() } }>Location Container Counts</button></div>
              <div className="column"><table className="tableTotals" className="center">
              <thead>
                <tr>
                <th colSpan="3">Totals</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th>Checked Out</th>
                  <th>Pending Return</th>
                  <th>Verified Return</th>
                </tr>
                <tr>
                <th>0</th>
                <th>0</th>
                <th>0</th>
                </tr>
              </tbody>
            </table></div>
              
              <div className="column"><button type="button" onClick={() => { routeChangeStatusCount() } }>Container Status Counts</button></div>
           </div>
            
            <br></br>
            <br></br>
            <input type="text" placeholder="Search for anything.." onChange={filterBySearch}></input>
            <input type="button" value="Toggle Limit" onClick={() => {toggleLimit()}}></input> 
            <br></br>
            <br></br>
            <br></br>
            <div className = "containertable">
            <table className="centerone">
            <thead>
             <tr>
               <th>Email</th>
               <th>QR Code</th>
               <th>Status
                <select name="status" id="status" onChange={filterByStatus}>
                  <option value="All">All</option>
                  <option value="Checked Out">Checked Out</option>
                  <option value="Pending Return">Pending Return</option>
                  <option value="Verified Return">Verified Return</option>
                  <option value="Damaged Lost">Damaged Lost</option>
                </select>
               </th>
               <th>Status Update Time</th>
               <th>Location QR Code</th>
               <th>Active</th>
               <th>Description</th>
               
             </tr>
             </thead>
             <tbody>
               {filteredContainers.map((elem)=>(
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
           </div>    
        )
}

export default Table
