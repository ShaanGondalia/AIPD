import React from 'react';
import { Card, Image, Icon, Button } from 'semantic-ui-react';

const AgentCardComponent = ({image, header, description}) => {
    return <Card>
        <Image src={image}/>
        <Card.Content textAlign="center">
            <Card.Header>{header}</Card.Header>
            <Card.Description>{description}</Card.Description>
        </Card.Content>
    </Card>
}

export default AgentCardComponent;