import './App.css';
import React,{Component, useState} from 'react';
import axios from 'axios';
import './table.css';
import { useHistory } from "react-router-dom";
import ExportCSV from './ExportCSV';

function Table (props) {
        const [containers, setContainers] = useState([])
        const [filteredContainers, setFilteredContainers] = useState([])
        const [selected, setSelected] = useState()
        const [limit, setLimit] = useState(20)
        const history = useHistory();
        const fileName = 'Container Transactions';

        function routeChangeContainerTable() { 
        let path = `/containerTable`; 
        history.push(path,{email:props.location.state.email,authToken:props.location.state.authToken});
        }
        function routeChangeStatusCount() { 
          let path = `/statusCount`; 
          history.push(path,{email:props.location.state.email,authToken:props.location.state.authToken});
        }
        function routeChangeEmailUsers() { 
          let path = `/emailUsers`; 
          history.push(path,{email:props.location.state.email,authToken:props.location.state.authToken});
        }

        function select(container){
          console.log(container)
          setSelected(container)
         }
        
        async function getContainers(email, authToken){
         var response = await axios.get('http://198.199.77.174:5000/getallContainers?email='+email+'&auth_token='+authToken)
         setContainers(response.data.data)
         console.log(response)
         try{
          setFilteredContainers(response.data.data.slice(0,limit))
         }
         catch (error) {
          history.push('/login')
        }
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
              container.description.includes(filter)
            )
            }
            else if(container.location_qrcode == null && container.description != null){
              return(
                container.email.includes(filter) || 
                container.qrcode.includes(filter) ||
                container.status.includes(filter) ||
                container.statusUpdateTime.includes(filter) ||
                container.description.includes(filter)
              )
              }
              else if(container.location_qrcode != null && container.description == null){
                return(
                  container.email.includes(filter) || 
                  container.qrcode.includes(filter) ||
                  container.status.includes(filter) ||
                  container.statusUpdateTime.includes(filter) ||
                  container.location_qrcode.includes(filter) 
                )
                }
                else if(container.location_qrcode == null && container.description == null){
                  return(
                    container.email.includes(filter) || 
                    container.qrcode.includes(filter) ||
                    container.status.includes(filter) ||
                    container.statusUpdateTime.includes(filter)
                  )
                  }
          }))
        }
        }
        
        try{
          if(containers.length === 0 && props.location && props.location.state){
          getContainers(props.location.state.email,props.location.state.authToken)
          }else if(!props.location || !props.location.state){
            history.push("/login");
          }
        }
        catch(error) {
          history.push('/login')
        }
        return (
            <div className="App">
              <div className="nav">
                <button className="navButton2" type="button" onClick={() => { routeChangeStatusCount() } }>All Locations</button>
                <button className="navButton3" type="button" onClick={() => { routeChangeEmailUsers() } }>Email Users</button>
                <button className="navButton1" type="button" onClick={() => { routeChangeContainerTable() } }>All Containers</button>
              </div>
            <br></br>
            <div className="title">
            <h1>All Container Transactions</h1>
            </div>
            <br></br>
            <br></br>
            <input type="text" placeholder="Search for anything.." onChange={filterBySearch}></input>
            <input type="button" value="Toggle Limit" onClick={() => {toggleLimit()}}></input>
            <div>
              <ExportCSV csvData={filteredContainers} fileName={fileName} />
            </div>
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
