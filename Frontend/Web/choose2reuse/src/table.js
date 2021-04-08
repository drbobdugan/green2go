import './App.css';
import React,{Component, useState} from 'react';
import axios from 'axios';


function Table (props) {
        
        return (
            <div className="App">
            <table className="table table-hover table-dark">
            <hi>hasContainer Table</hi>
             <tr>
               <th>Email</th>
               <th>QR Code</th>
               <th>Status</th>
               <th>Status</th>
               <th>Status Update Time</th>
               <th>Location QR Code</th>
               <th>Active</th>
               <th>Description</th>
               
             </tr>
               <tr>
                 <td>x</td>
                 <td>y</td>
                 <td>z</td>
                 <td>a</td>
                 <td>c</td>
                 <td>d</td>
                 <td>e</td>
                 <td>f</td>
                </tr>
               
             </table>
           </div>    
        )
}

export default Table
