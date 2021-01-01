import { useEffect, useState, useRef } from "react";
import { Button, Col, Container, Row } from "react-bootstrap";
import {useParams, useHistory} from "react-router-dom";
import io from 'socket.io-client';

function Game(props){
    let {id} = useParams();
    //const [socket, setSocket] = useState();
    const history = useHistory()
    const [cards, setCards] = useState([])
    const [name, setName] = useState("")
    const [players, setPlayers] = useState([])
    const [status, setStatus] = useState("Loading")
    const [turn, setTurn] = useState("")
    const socketContainer = useRef(null)

    useEffect(() => {
        fetch("/api/game/" + id).then(res => res.json()).then(data => {
            if (data.valid === false){
                history.push('/');
            } else {
                setCards(data.cards)
                setStatus("Loaded")
            }
        })
    }, [])

    function joinGamePlayer() {
        socketContainer.current = io() //creates the socket
        if(name === ""){
            setName("Mr. potato head")  //TODO: create a random name generator
        }

        //once the socket is connected
        socketContainer.current.on('connect', () => {
            socketContainer.current.emit('join', {game: id, player: true, name: name}); //say that they are connected and pass the name
            setUpListeners(); //call a functino to set up the rest of the sockets
            setStatus("Player") //say connected
        })        
    }

    function joinGameSpectator()  {
        socketContainer.current = io() //create the socket
        
        socketContainer.current.on('connect', () => {
            socketContainer.current.emit('join', {game: id, player: false}) 
            setUpListeners(); //set up all teh same listeners for chagnes
            setStatus("Spectator");
        })    
    }

    function setUpListeners() {
        socketContainer.current.on('playerUpdate', (data) => { //listener for when a player joins to update the list of players
            setPlayers(data['players'])
        })

        socketContainer.current.on('gameStart', (data) => {
            setStatus('Playing')
            setTurn(data['turn'])
        })

        socketContainer.current.on('handUpdate', (data) => {
            setCards(data['hand'])
            //TODO: Acutally get the hand to show, and add more cards
        })
    }

    function startGame() {
        socketContainer.current.emit('startGame', {game: id})
    }

    

    //I should see if I can make the input field work with React Bootstrap


    //issue, the functions button calls are within a lower scope, so the global socket here is never set
    //arrow functions are not the most optimized but we go with it
    return (
        <div>
            <p>{status}</p>
            {status === "Player" && 
                <div>
                    <h1>Start Game</h1>
                    <Button onClick={startGame}>Start Game</Button>
                </div>
            }
            {status === "Loaded" && 
                <div id="join-game">
                    <h1>Join a game</h1>
                    <div className="container d-flex">
                        <input id="name" type="text" className="input-group-text flex-nowrap" placeholder="name" onChange={e => setName(e.target.value)}>{}</input>
                        <Button onClick={joinGamePlayer} className="btn btn-primary">Join as Player</Button>
                        <Button onClick={joinGameSpectator} className="btn btn-secondary">Join as spectator</Button>
                    </div>
                </div>
            }
            <ul>
            {
                players.map(player => 
                    {return player === turn ? 
                        <li style={{color: "green"}} key={player}>{player} (Current Turn)</li>  
                        :
                        <li key={player}>{player}</li>
                    }
                    
                )
            }
            </ul>
            
           {status === "Playing" && <Hand cards={cards}/>}
        </div>
    )
}

function Hand(props){
    var isArray = Array.isArray(props.cards)

    return (
         
        <div>          
            {isArray && 
            <div>
                <h3>Your Cards</h3> 
                <Container fluid justify-content-center="true">
                    <Row>
                        {props.cards.map(cardId => 
                            <Col style={{textAlign: 'center'}} key={cardId}>{cardId}</Col>
                        )}
                    </Row>
                </Container> 
            </div>
            }
            
        </div>
    
        
    )
}

export default Game;