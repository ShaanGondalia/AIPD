import React from 'react';
import { Container, Header, Grid, Image } from 'semantic-ui-react';
import AgentCardComponent from '../Components/AgentCardComponent';
import Cooperate from '../Static/Cooperate.png';
import Defect from '../Static/Defect.png';
import Copy from '../Static/Copy.png';
import Grudge from '../Static/Grudge.png';
import Model from '../Static/Model.png';
import LSTM from '../Static/LSTM.jpg';
import QLearning from '../Static/QLearning.png';

const AboutPage = () => {
    return <Container>
        <Header as='h2'>Introduction to Prisoner's Dilemma</Header>
        <div>
            The prisoner's dilemma is a game commonly analyzed in game theory to show why individuals may not 
            cooperate despite it appearing to be in their best interest to do so.  In this game, two players 
            make a choice to cooperate or defect, and are rewarded based on their action and their opponent's 
            action. The rewards are constrained such that a reward is maximum when one individual defects and 
            the other does not. The next highest reward occurs when both individuals cooperate. Lastly, when both 
            both individuals defect, an individual's reward is minimized. The iterated  prisoner's  dilemma  (IPD)  
            repeats  this process multiple times, creating a greater incentive to cooperate, motivating coordination 
            from both agents. The goal for this project was to use a combination of deep learning and reinforcement 
            learning to create an agent that could play prisoner's dilemma to a reasonable level of proficiency.
        </div>
        <Header as='h2'>Agents for Training</Header>
        <div style = {{marginBottom: '2em'}}>To train our model, we needed it to play against several well defined 
        strategies. Our strategies were based on the descriptions of action explained by Elinor Ostrom These agents are 
        defined below:
         </div>
        <Grid>
            <Grid.Row centered>
                <Grid.Column width={3}>
                    <AgentCardComponent
                        image= {Cooperate}
                        header="Cooperate Agent"
                        description="Agent that cooperates regardless of the opponent moves."
                    />
                </Grid.Column>
                <Grid.Column width={3}>
                    <AgentCardComponent
                        image= {Defect}
                        header="Defect Agent"
                        description="Agent that defects regardless of the opponent moves."
                    />
                </Grid.Column>
                <Grid.Column width={3}>
                    <AgentCardComponent
                        image= {Copy}
                        header="Copy Agent"
                        description="Agent that chooses the previous move of the opponent."
                    />
                </Grid.Column>
                <Grid.Column width={3}>
                    <AgentCardComponent
                        image= {Grudge}
                        header="Grudge Agent"
                        description="Agent that cooperates unless defect on, in which case it always defects."
                    />
                </Grid.Column>
            </Grid.Row>
        </Grid>
        <Header as='h2'>Custom AI Agent</Header>
        <div style = {{marginBottom: '2em'}}>
            Our custom model utilized deep learning in the form of a LSTM Neural Network to predict the idenity of 
            the agent it plays against. Then, from the identity of the agent, a custom Q-Table is used to infer the 
            optimal move given the previous history of the game. The input to this model is a set of past moves for
            both the player and the opponent. The LSTM Neural Network outputs a confidence value for each agent it is 
            trained on which it believes to be the probability that the input move set could be from each agent. The 
            Q-Table table uses the same set of past moves to predict the expected reward given a cooperate decision or 
            a defect decision. Since the LSTM outputs probabilities, one can choose stochastically or deterministically
            the idenity of the opponent agent, which would affect the choice of Q-Table and may effect the decision of
            the model. Weighing the optimal moves against the output probability of the LSTM can give a probability
            that for either choice being the optimal move.
        </div>
        <Grid>
            <Grid.Row centered>
                <Grid.Column width={12}>
                    <Image src={Model}/>
                </Grid.Column>
            </Grid.Row>
        </Grid>
        <Header as='h2'>LSTM for Prediction</Header>
        <div style = {{marginBottom: '2em'}}>
            An LSTM stands for Long Short-Term Memory Neural Network is known for being exceptional
            at learning sequences of data. In the context of prisoner's dilemma the sequence of data 
            that an LSTM is learning is the series of player moves. An LSTM cell is composed of an 
            input gate, an output gate, and a forget gate. Due to the recurrent nature of the LSTM, 
            at any cell, the inputs are the previous hidden state, the previous cell state, and the
            current data point. When data is passed in, the current data point and the previous hidden
            state reach the forget gate, which determines the proportion of data to forget in each cell 
            state. The current data point and previous hidden state reach the input gate, which computes
            which values in the cell state to update. Candidate values are computed. The output of the 
            forget gate, input gate, and the candidate values are used to compute the new cell state. When 
            the current data point and previous hidden state reach the ouput gate an output value is computed. 
            The output value and new cell state are used to compute the new hidden state. In this way, the LSTM
            outputs a new hidden state, a new cell state, and an output for prediction. The LSTM our model 
            utilizes was trained via Cross-Entropy Loss.
        </div>
        <Grid>
            <Grid.Row centered>
                <Grid.Column width={8}>
                    <Image src={LSTM}/>
                </Grid.Column>
            </Grid.Row>
        </Grid>
        <Header as='h2'>Q-Table for Action</Header>
        <div style = {{marginBottom: '2em'}}>
            A Q-Table is mapping of states and actions to a reward in a 2D matrix. The Q-Table 
            was adopted with the objective of maximizing the agent's own reward when 
            playing against an opponent of a known strategy. In order to compute the Q-Table, an 
            agent plays the IPD multiple times against a strategy, populating the rewards associated 
            with the result of performing each action at any state in the game. Since the Q-table is 
            trained to play against one strategy, for a game with N strategies, N Q-tables are trained. 
            The Q-Agent, which makes decisions based on a Q-Table, begins playing the IPD against 
            another agent with no information about them or the game, besides knowing the option for 
            cooperating or defecting. In this initial state, or in any state with symmetrical or unpopulated rewards, 
            the Q-Agent cooperates or defects at random. The opponent agent selects their action according to 
            their pre-defined strategy. Then, based on the action of these two players, the rewards from this single PD game 
            is added to each player's total IPD reward. The Q-Agent learns from this interaction by writing the reward into the 
            corresponding state of the game, based on the history of past moves, for the action it took. The exact forumula used 
            for training is displayed below.
        </div>
        <Grid>
            <Grid.Row centered>
                <Grid.Column width={12}>
                    <Image src={QLearning}/>
                </Grid.Column>
            </Grid.Row>
        </Grid>
    </Container>
}

export default AboutPage;