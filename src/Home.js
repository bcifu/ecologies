import React, {useEffect, useState} from "react"
import { Button, ListGroup, ListGroupItem } from "react-bootstrap";
import { useHistory } from "react-router-dom";


function Home(props) {

    const [games, setGames] = useState([])
    const history = useHistory()

    function newGame() {
        fetch('/api/newGame/').then(res => res.json()).then(data => {history.push("/game/" + data.gameId)})
    }
    //make sure that this won't block
    useEffect(() => {fetch('/api/games/').then(res => res.json()).then(data => setGames(data.games))}, [])
    
//for the creating a new game, I can't just go because the game has to be set up then redirected, so what I should do is run an action then have a confirmation callback which the flask can call and that triggers the redirect
    return (
            <div className="Home">
                <Button onClick={newGame}>Create Game</Button>
                <h1>Games</h1>
                <ListGroup>
                {games.map((gameId => 
                    <ListGroupItem key={gameId} action href={"/game/" + gameId}>{gameId}</ListGroupItem>
                    ))} 
                </ListGroup>
            </div>
    )
    
}

export default Home;