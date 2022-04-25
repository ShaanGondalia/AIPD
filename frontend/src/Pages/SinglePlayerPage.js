import React from 'react';
import RewardTableComponent from '../Components/RewardComponent';
import GameTableComponent from '../Components/GameTableComponent';
import { Grid, Button } from 'semantic-ui-react';
import axios from 'axios';

const SinglePlayerPage = () => {

    const [userHistory, setUserHistory] = React.useState([])
    const [opponentHistory, setOpponentHistory] = React.useState([])

    const onButtonClick = async (event) => {
        console.log("Hello World")
        const data = {
            'user_moves' : userHistory,
            'agent_moves' : opponentHistory
        }
        const res = await axios.post("/play", data)
        if (res.status === 200) {
            var newUserHistory = [...userHistory]
            if (event.target.name === "coop") {
                newUserHistory.push(0)
            } else {
                newUserHistory.push(1)
            }
            var newOpponentHistory = [...opponentHistory]
            newOpponentHistory.push(res.data.agent_decision)
            setUserHistory(newUserHistory)
            setOpponentHistory(newOpponentHistory)
        }
    }

    return <Grid>
        <Grid.Row centered>
            <Grid.Column mobile={12} tablet={12} computer={9}>
                <RewardTableComponent/>
            </Grid.Column>
        </Grid.Row>
        <Grid.Row centered>
            <Button name="coop" color="blue" onClick={onButtonClick}>Cooperate</Button>
            <Button name="defect" color="red" onClick={onButtonClick}>Defect</Button>
        </Grid.Row>
        <Grid.Row centered>
            <Grid.Column mobile={12} tablet={12} computer={12}>
                {<GameTableComponent userHistory={userHistory} opponentHistory={opponentHistory}/>}
            </Grid.Column>
        </Grid.Row>
    </Grid>
}

export default SinglePlayerPage;