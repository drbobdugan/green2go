import './App.css';
import React,{Component, useState} from 'react';
import axios from 'axios';
import './table.css';
import { useHistory } from "react-router-dom";
import ExportCSV from './ExportCSV';

function ContainerTable (props) {
        const [containers, setContainers] = useState([])
        const [filteredContainers, setFilteredContainers] = useState([])
        const [retrieved, setRetrieved] = useState(false)
        const [selected, setSelected] = useState()
        const [limit, setLimit] = useState(20)
        const history = useHistory();
        const [email,setEmail] = useState()
        const [authToken,setAuthToken] = useState()
        const [checkedOut, setCheckedOut] = useState()
        const [inStock, setInStock] = useState()
        const [pendingReturn, setPendingReturn] = useState()
        const [damagedLost, setDamagedLost] = useState()
        const fileName = 'Container Status Counts';
        const [cont_qr, setCont_qr] = useState('')


        async function markDamagedLost(qr_code) { 
          const obj = {email: email, qrcode: qr_code,status: 'Damaged Lost', auth_token: authToken, description: 'Damaged Lost'};
          console.log(obj)
          var response = await axios.post('http://198.199.77.174:5000/reportContainer', obj)
          getContainers(email,authToken)
        }

        async function revertDamagedLost(qr_code) { 
          const obj = {email: email, qrcode: qr_code, auth_token: authToken};
          var response = await axios.post('http://198.199.77.174:5000/undoReportContainer', obj)
          getContainers(email,authToken)
        }

        async function addContainer(qrcode){
          const obj = {qrcode: qrcode, email: email, auth_token: authToken};
          var response = await axios.post('http://198.199.77.174:5000/addContainer', obj)
          console.log(response)
          await getContainerInfo(email,authToken)
          setCont_qr('')
      }

      async function getContainerInfo(email, authToken){
        var response = await axios.get('http://198.199.77.174:5000/containerList?email='+email+'&auth_token='+authToken)
        console.log(response.data.data)
        if(response && response.data && response.data.data)
        {
            console.log("Setting containers")
            setContainers(response.data.data)
            setFilteredContainers(response.data.data)
        }
      }

        function select(container){
          console.log(container)
          setSelected(container)
         }
        
        async function getContainers(email, authToken){
          try{
            var response = await axios.get('http://198.199.77.174:5000/getCurrent?email='+email+'&auth_token='+authToken)
            if(response && response.data && response.data.data && response.data.data.length){
              setContainers(response.data.data)
              setFilteredContainers(response.data.data)
            }
            setEmail(email);
            setAuthToken(authToken);
          }
        catch(e){
          console.log(e)
        }
        }

        async function removeContainer(qr_code){
          const obj = {qrcode: qr_code, auth_token: authToken, email: email};
          console.log(obj)
<<<<<<< HEAD
          var response = await axios.delete('http://198.199.77.174:5000/deleteContainer', { data: obj })
=======
          //var response = await axios.delete('http://198.199.77.174:5000/removeContainer', obj)
          var response = axios.delete('http://198.199.77.174:5000/deleteContainer', { data: obj })
>>>>>>> 8fe1b533ceba878f97c586d4d1c09c78934639e2
          console.log(response)
          await getContainerInfo(email,authToken)
      }

        async function getCounts(email, authToken){
          try{
            var response = await axios.get('http://198.199.77.174:5000/getCounts?email='+email+'&auth_token='+authToken)
            console.log(response.data.data)
            setRetrieved(true)
            setCheckedOut(response.data.data["Checked Out"].length)
            setInStock(response.data.data["In Stock"].length)
            setPendingReturn(response.data.data["In Bin"].length)
            setDamagedLost(response.data.data["Damaged Lost"].length)
          }
          catch(e){
            console.log(e)
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

        function filterBySearch(e) {
          var filter = e.target.value
          console.log(filter) 
          if(filter === ""){
            setFilteredContainers(containers.slice(0,limit))
          }else{    
          setFilteredContainers(containers.filter(container => {
            if(container.status == null){
              return(
                container.qrcode.includes(filter)
              )
            }
            else if(container.status != null && container.qrcode != null){
              return( 
                container.qrcode.includes(filter) ||
                container.status.includes(filter)
              )
            }
          }))
        }
        }

        function backPage(){
          history.goBack()
      }

        if(containers.length === 0 && props.location && props.location.state){
          getContainers(props.location.state.email,props.location.state.authToken)
        }else if(!props.location || !props.location.state){
          history.push("/login");
        }

        if(containers.length != 0 && props.location && props.location.state){
          getCounts(props.location.state.email,props.location.state.authToken)
        }else if(!props.location || !props.location.state){
          history.push("/login");
        }

        return (
            <div className="App">
              <div className ="back">
                <input type='button' value='Back' onClick={() => {backPage()}}/>
              </div>
            <br></br>
            <br></br>
            <div className="title">
            <h1>All Containers</h1>
            </div>
            <h2>Container Status Counts</h2>
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
                    <tr>
                        <td>Damaged Lost</td> 
                        <td>{damagedLost}</td>
                    </tr>
                </tbody>
             </table>
             </div>
            <br></br>
            <input type="text" placeholder="Search for anything.." onChange={filterBySearch}></input>
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
               <th>Mark Damaged Lost</th>
               <th>Revert Damaged Lost</th>
               <th>Remove Container</th>
             </tr>
             </thead>
             <tbody>
               {filteredContainers.map((elem)=>(
                <tr onClick={()=>{select(elem)}}>
                 <td>{elem.qrcode}</td>
                 <td>{elem.status}</td>
                 <td><input type="button" value="Damaged Lost" onClick ={() => {markDamagedLost(elem.qrcode)}}/></td>
                 <td><input type="button" value="Revert" onClick ={() => {revertDamagedLost(elem.qrcode)}}/></td>
                 <td><input type="button" value="Remove" onClick ={() => { if (window.confirm('Are you sure you wish to remove this container?')) removeContainer(elem.qrcode) } }/></td>
                </tr>
               ))}
                </tbody>
             </table>
             <table className="addLocation">
                <thead>
                    <tr>
                      <th>Container QR Code</th>
                      <th>Add Container</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><input type='text' value={cont_qr} placeholder="qr_code" onChange={event => setCont_qr(event.target.value)}/></td> 
                        <td><input type='button' value='Add' onClick ={() => {addContainer(cont_qr)}}/></td>
                    </tr>
                </tbody>
             </table>
             </div>
           </div>    
        )
}

export default ContainerTable