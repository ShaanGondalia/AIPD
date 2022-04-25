import React from 'react';
import { Grid, Container, Image } from 'semantic-ui-react';
import TournamentFormComponent from '../Components/TournamentFormComponent';

const TournamentPage = () => {

    const [gif, setGif] = React.useState("")

    return <Grid>
        <Grid.Row centered>
            <Grid.Column mobile={12} tablet={12} computer={12}>
                <TournamentFormComponent setGif = {setGif}/>
            </Grid.Column>
        </Grid.Row>
        <Grid.Row centered>
            <Grid.Column>
                <Container>
                    {gif !== "" ?  <Image className= "ui centered medium image" src={`data:image/png;base64,${gif}`}/> : null}
                </Container>
            </Grid.Column>
        </Grid.Row>
    </Grid>
}

export default TournamentPage;