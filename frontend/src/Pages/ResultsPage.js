import React from 'react';
import { Container, Header, Grid, Image } from 'semantic-ui-react';
import AgentCardComponent from '../Components/AgentCardComponent';
import LSTMAcc from '../Static/LSTM Accuracy.png'
import CooperateConfidence from '../Static/CooperateConfidence.png'
import DefectConfidence from '../Static/DefectConfidence.png'
import CopyConfidence from '../Static/CopyConfidence.png'
import GrudgeConfidence from '../Static/GrudgeConfidence.png'
import Cooperate from '../Static/Cooperate.gif'
import Defect from '../Static/Defect.gif'
import Copy from '../Static/Copy.gif'
import Grudge from '../Static/Grudge.gif'


const ResultPage = () => {
    const [visualQState, setVisualQState] = React.useState('coop')

    const handleQClick = (event, {name}) => {
        setVisualQState(name)
    }


    return <Container>
        <Header as='h2'>Results of LSTM Training</Header>
        <Image src = {LSTMAcc} className= "ui centered medium image"/>
        <div style={{margin: '2em'}}>
            The above graphic displays the accuracy of our LSTM model as the number of rounds it plays increases. 
            When the model starts out playing just 1 round, it can only identify the opponent with around 20% 
            accuracy meaning it is randomly guessing the identity of the opponent. However, as the number of rounds
            increases, the model becomes more and more accurate at identifying its opponent, reaching a plateau at 
            80% accuracy with 10 rounds.
        </div>
        <Grid>
            <Grid.Row centered>
                <Grid.Column width={4}>
                    <Image src = {CooperateConfidence} className='ui centered medium image'/>
                </Grid.Column>
                <Grid.Column width={4}>
                    <Image src = {DefectConfidence} className='ui centered medium image'/>
                </Grid.Column>
                <Grid.Column width={4}>
                    <Image src = {CopyConfidence} className='ui centered medium image'/>
                </Grid.Column>
                <Grid.Column width={4}>
                    <Image src = {GrudgeConfidence} className='ui centered medium image'/>
                </Grid.Column>
            </Grid.Row>
        </Grid>
        <div style={{margin: '2em'}}>
            The above 4 graphics display the confidence of our LSTM model as the number of rounds it plays increases.
            The LSTM model is able to quickly and confidently identify the Cooperate Agent and the Grudge Agent. However, 
            it consistently mistakes the Defect Agent with the Grudge Agent until over 20 rounds are played. This 
            shouldn't greatly affect performance  as a Defect Agent and a Grudge Agent that has been cheated on have the same actions,
            so the optimal moves should be the same via Q-Table. Lastly, with the Copy Agent, the model is able to identify it 
            confidently so long as the number of rounds played remain below 30, after which it confuses it with the Cooperate Agent. 
            This can lead to undesirable behavior as over the long run, it is best to cheat against a Cooperate Agent and cooperate against
            a Copy Agent, leading to unoptimal behavior from the AI.

        </div>
        <Header as='h2'>Results of Q-Table Training</Header>  
        <Grid>
            <Grid.Row centered>
                <Grid.Column width={3}>
                    <AgentCardComponent
                        image= {Cooperate}
                        header="Cooperate"
                        description="Q-Table weights trained to play optimally against a Cooperate Agent"
                    />
                </Grid.Column>
                <Grid.Column width={3}>
                    <AgentCardComponent
                        image= {Defect}
                        header="Defect"
                        description="Q-Table weights trained to play optimally against a Defect Agent"
                    />
                </Grid.Column>
                <Grid.Column width={3}>
                    <AgentCardComponent
                        image= {Copy}
                        header="Copy"
                        description="Q-Table weights trained to play optimally against a Copy Agent"
                    />
                </Grid.Column>
                <Grid.Column width={3}>
                    <AgentCardComponent
                        image= {Grudge}
                        header="Grudge"
                        description="Q-Table weights trained to play optimally against a Grudge Agent"
                    />
                </Grid.Column>
            </Grid.Row>
        </Grid>
        <div style={{margin: '2em'}}>
            The above graphics show the optimal move at each state in the Q-Table. Red indicates defect while blue
            indicates cooperate. The intenisty of the color displays the magnitude of the expected reward. As the 
            rounds are played out, we see that against a Cooperate Agent, the Q-Table slowly learns to consistently 
            cheat. Against a Defect Agent, the Q-Table quickly learns to cheat. Against a Copy Agent, the Q-Table finds
            that cheating and cooperating give very close rewards. Finally, against the Grudge Agent, the Q-Table discovers
            that it is best to cooperate if and only if it has not cheated before. 
        </div>
        <div style={{padding:'1em'}}/>
    </Container>
}

export default ResultPage;