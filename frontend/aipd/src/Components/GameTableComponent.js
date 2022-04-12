import React from 'react';
import { Table } from 'semantic-ui-react';


const GameTableComponent = ({userHistory, opponentHistory}) => {

    return <Table celled>
        <Table.Header>
            <Table.Row>
                <Table.HeaderCell>Your Moves</Table.HeaderCell>
                <Table.HeaderCell>Opponent Moves</Table.HeaderCell>
                <Table.HeaderCell>Your Cumulative Reward</Table.HeaderCell>
                <Table.HeaderCell>Opponent Cumulative Reward</Table.HeaderCell>
            </Table.Row>
        </Table.Header>
        <Table.Body>
            {generateRows(userHistory, opponentHistory)}
        </Table.Body>
    </Table>
}

const generateRows = (userHistory, opponentHistory) => {

    if (userHistory.length < 0) {
        return null
    }
    const cumulativeRewards = computeCumulativeRewards(userHistory, opponentHistory)
    console.log(cumulativeRewards)
    const rows = userHistory.map((x, i) => {
        return <Table.Row>
            <Table.Cell>{x}</Table.Cell>
            <Table.Cell>{opponentHistory[i]}</Table.Cell>
            <Table.Cell>{cumulativeRewards.userCumulativeRewards[i]}</Table.Cell>
            <Table.Cell>{cumulativeRewards.opponentCumulativeRewards[i]}</Table.Cell>
        </Table.Row>
    })
    return rows
}

const REWARD = [[2, 2], 
                [0, 3],
                [3, 0],
                [1, 1]]

const computeReward = (userChoice, opponentChoice) => {

    var userReward = 0;
    var opponentReward = 0;

    if (userChoice === 0 && opponentChoice === 0) {
        userReward = REWARD[0][0]
        opponentReward = REWARD[0][1]
    } else if (userChoice === 0 && opponentChoice === 1) {
        userReward = REWARD[1][0]
        opponentReward = REWARD[1][1]
    } else if (userChoice === 1 && opponentChoice === 0) {
        userReward = REWARD[2][0]
        opponentReward = REWARD[2][1]
    } else {
        userReward = REWARD[3][0]
        opponentReward = REWARD[3][1]
    }

    return {
        userReward: userReward,
        opponentReward: opponentReward
    }
}

const computeCumulativeRewards = (userHistory, opponentHistory) => {

    var userCumulativeRewards = []
    var opponentCumulativeRewards = []

    const roundRewards = userHistory.map((x, i) => {
        return computeReward(x, opponentHistory[i])
    })

    const roundRewardsCopy = [...roundRewards]

    roundRewards.reduce((a, b, i) => {
        userCumulativeRewards[i] = a + b.userReward
        return userCumulativeRewards[i]
    }, 0)

    roundRewardsCopy.reduce((a, b, i) => {
        opponentCumulativeRewards[i] = a + b.opponentReward
        return opponentCumulativeRewards[i]
    }, 0) 

    return {
        userCumulativeRewards: userCumulativeRewards,
        opponentCumulativeRewards: opponentCumulativeRewards
    }

}

export default GameTableComponent;