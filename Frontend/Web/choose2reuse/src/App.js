import './App.css';
import { BrowserRouter as Router, Switch, Route, Redirect} from 'react-router-dom';
import Login from './login';
import Table from './table';
import StatusCount from './statusCount';
import ContainerTable from './containerTable';
import React,{Component} from 'react';

export default class App extends Component {
  render(){
    return (
    <div className="App">
      <Router basename={process.env.PUBLIC_URL}>
        <Switch>
          <Route exact path= "/" render = {() => (
            <Redirect to = "/login"/>
          )}/>
          <Route exact path= "/login" component={Login} />
          <Route exact path= "/table" component={Table} />
          <Route exact path= "/statusCount" component={StatusCount} />
          <Route exact path= "/containerTable" component={ContainerTable} />
        </Switch>
      </Router>
    </div>
  );
  }
}
