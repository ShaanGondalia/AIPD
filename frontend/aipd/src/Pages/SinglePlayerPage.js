import React from 'react';
import RewardTableComponent from '../Components/RewardComponent';
import GameTableComponent from '../Components/GameTableComponent';
import { Grid, Button } from 'semantic-ui-react';

const SinglePlayerPage = () => {

    const [userHistory, setUserHistory] = React.useState([])
    const [opponentHistory, setOpponentHistory] = React.useState([])

    const onButtonClick = (event) => {
        var newUserHistory = [...userHistory]
        if (event.target.name === "coop") {
            newUserHistory.push(0)
        } else {
            newUserHistory.push(1)
        }
        var newOpponentHistory = [...opponentHistory]
        newOpponentHistory.push(Math.round(Math.random()))
        setUserHistory(newUserHistory)
        setOpponentHistory(newOpponentHistory)
        console.log("Hello World")
    }

    return <Grid>
        <Grid.Row centered>
            <Grid.Column mobile={20} tablet={12} computer={9}>
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