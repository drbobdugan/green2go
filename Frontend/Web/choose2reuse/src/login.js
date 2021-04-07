import './App.css';
import React,{Component} from 'react';

export default class Login extends Component {
    constructor(props){
        super(props);

        this.state = { userid: '', password: ''};
    }
    componentDidMount(){}

    onChangeUserid(e){
        const { value } = e.target;
        this.setState({ userid: value });
        console.log(this.state.userid);
    }

    onChangePassword(e){
        const { value } = e.target;
        this.setState({ password: value });
    }

    render(){
        return (
        <div className="App">
            <hi>Login</hi>
            <p>Login Attempts: </p>
            <form id="form" method="post" action='login'>
                <p>Userid:  <input type="text" name="userid" onChange={this.onChangeUserid} /> </p>
                <p>Password:  <input type="password" name="password" onChange={this.onChangePassword} /> </p>
                <input type="submit" name="submit" value="submit"/>
            </form>
        </div>
            );
    }
}