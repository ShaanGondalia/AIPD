import React from 'react';
import { Table } from 'semantic-ui-react';

const RewardTableComponent = () => {
    return <Table definition>
        <Table.Header>
            <Table.Row>
                <Table.HeaderCell />
                <Table.HeaderCell>Opponent Cooperates</Table.HeaderCell>
                <Table.HeaderCell>Opponent Defects</Table.HeaderCell>
            </Table.Row>
        </Table.Header>
        <Table.Body>
            <Table.Row>
                <Table.Cell>You Cooperate</Table.Cell>
                <Table.Cell>
                    <div>Your Reward: 2</div>
                    <div>Opponent Reward: 2</div>   
                </Table.Cell>
                <Table.Cell>
                    <div>Your Reward: 0</div>
                    <div>Opponent Reward: 3</div>
                </Table.Cell>
            </Table.Row>
            <Table.Row>
                <Table.Cell>You Defect</Table.Cell>
                <Table.Cell>
                    <div>Your Reward: 3</div>
                    <div>Opponent Reward: 0</div>
                </Table.Cell>
                <Table.Cell>
                    <div>Your Reward: 1</div>
                    <div>Opponent Reward: 0</div>     
                </Table.Cell>
            </Table.Row>
        </Table.Body>
    </Table>
}

export default RewardTableComponent;