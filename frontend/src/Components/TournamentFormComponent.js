import React from 'react';
import { Form, Select } from 'semantic-ui-react';
import axios from 'axios';

const selectOptions = [
    { key: '1', text: '1', value: 1 },
    { key: '2', text: '2', value: 2 },
    { key: '3', text: '3', value: 3 },
    { key: '4', text: '4', value: 4 },
    { key: '5', text: '5', value: 5 },
    { key: '6', text: '6', value: 6 },
    { key: '7', text: '7', value: 7 },
    { key: '8', text: '8', value: 8 },
    { key: '9', text: '9', value: 9 },
    { key: '10', text: '10', value: 10 },
    { key: '11', text: '11', value: 11 },
    { key: '12', text: '12', value: 12 },
    { key: '13', text: '13', value: 13 },
    { key: '14', text: '14', value: 14 },
    { key: '15', text: '15', value: 15 },
    { key: '16', text: '16', value: 16 },
    { key: '17', text: '17', value: 17 },
    { key: '18', text: '18', value: 18 },
    { key: '19', text: '19', value: 19 },
    { key: '20', text: '20', value: 20 },
    { key: '21', text: '21', value: 21 },
    { key: '22', text: '22', value: 22 },
    { key: '23', text: '23', value: 23 },
    { key: '24', text: '24', value: 24 },    
    { key: '25', text: '25', value: 25 },
    { key: '26', text: '26', value: 26 },
    { key: '27', text: '27', value: 27 },
    { key: '28', text: '28', value: 28 },
    { key: '29', text: '29', value: 29 },
    { key: '30', text: '30', value: 30 }
  ]

const TournamentFormComponent = ({setGif}) => {

    const [percentCoop, setPercentCoop] = React.useState(0)
    const [percentDefect, setPercentDefect] = React.useState(0)
    const [percentCopy, setPercentCopy] = React.useState(0)
    const [percentGrudge, setPercentGrudge] = React.useState(0)
    const [percentAI, setPercentAI] = React.useState(0)

    const [generations, setGenerations] = React.useState(0)
    const [interactions, setInteractions] = React.useState(0)
    const [rounds, setRounds] = React.useState(0)
    const [reproduction, setReproduction] = React.useState(0)

    const onChange = (event) => {
        switch(event.target.id) {
            case 'coop':
                setPercentCoop(event.target.value)
                break
            case 'defect':
                setPercentDefect(event.target.value)
                break
            case 'copy':
                setPercentCopy(event.target.value)
                break
            case 'grudge':
                setPercentGrudge(event.target.value)
                break
            case 'ai':
                setPercentAI(event.target.value)
                break
            case 'reproduction':
                setReproduction(event.target.value)
                break
        }
    }

    const onSelectChange = (event, result) => {
        switch(result.id) {
            case 'generations':
                setGenerations(result.value)
                break
            case 'interactions':
                setInteractions(result.value)
                break
            case 'rounds':
                setRounds(result.value)
                break
        }
    }

    const onSubmit = async () => {
        const config = makeConfig()
        const data = {
            generations : generations,
            interactions: interactions,
            rounds: rounds,
            reproduction_rate: reproduction / 100,
            config: config
        }
        const res = await axios.post("/tournament", data)
        if (res.status === 200) {
            setGif(res.data.gif)
        }
    }

    const makeConfig = () => {
        const total = Number(percentCoop) + Number(percentDefect) + Number(percentCopy) + Number(percentGrudge) + Number(percentAI)
        var coop = 20
        var defect = 20 
        var copy = 20
        var grudge = 20
        var ai = 20
        if (total !== 0) {
            coop = Math.round(100 * percentCoop / total)
            defect = Math.round(100 * percentDefect / total)
            copy = Math.round(100 * percentCopy / total)
            grudge = Math.round(100 * percentGrudge / total)
            ai = Math.round(100 * percentAI / total)
        }
        const coopConfig = {
            name : "Cooperate",
            id : 0,
            count : coop,
            type : 'memory',
            n : 1,
            strategy: [0,0,0,0]

        }
        const defectConfig = {
            name : "Defect",
            id : 1,
            count : defect,
            type : 'memory',
            n : 1,
            strategy: [1,1,1,1]
        }
        const copyConfig = {
            name: "Copy", 
            id: 2,
            count: copy,
            type: "memory", 
            n: 1,
            strategy: [0,1,0,1]
        }
        const grudgeConfig = {
            name: "Grudge",
            id: 3,
            count: grudge,
            type: "memory", 
            n: 1,
            strategy: [0,1,1,1]
        }
        const aiConfig = {
            name: "AI",
            id: 4,
            count: ai, 
            type: "ai", 
        }
        const config = {
            agents : [coopConfig, defectConfig, copyConfig, grudgeConfig, aiConfig]
        }
        return config
    }

    return <Form onSubmit = {onSubmit}>
        <Form.Group widths='equal'>
            <Form.Field required
                label = 'Percent Cooperate Agent (0)'
                id = 'coop'
                control = 'input'
                type = 'number'
                max = {100}
                min  = {0}
                onChange = {onChange}
            />
            <Form.Field required
                label = 'Percent Defect Agent (1)'
                id = 'defect'
                control = 'input'
                type = 'number'
                max = {100}
                min  = {0}
                onChange = {onChange}
            />            
            <Form.Field required
                label = 'Percent Copy Agent (2)'
                id = 'copy'
                control = 'input'
                type = 'number'
                max = {100}
                min  = {0}
                onChange = {onChange}
            />
            <Form.Field required
                label = 'Percent Grudge Agent (3)'
                id ='grudge'
                control = 'input'
                type = 'number'
                max = {100}
                min  = {0}
                onChange = {onChange}
            />
            <Form.Field required
                label = 'Percent AI Agent (4)'
                id = 'ai'
                control = 'input'
                type = 'number'
                max = {100}
                min  = {0}
                onChange = {onChange}
            />
        </Form.Group>
        <Form.Group>
            <Form.Field required
                label = 'Generations'
                id = 'generations'
                type = 'number'
                placeholder = '1'
                onChange = {onSelectChange}
                control = {Select}
                options = {selectOptions}
            />
            <Form.Field required
                label = 'Interactions'
                id = 'interactions'
                type = 'number'
                placeholder = '1'
                onChange = {onSelectChange}
                control = {Select}
                options = {selectOptions.slice(0, 6)}
            />
            <Form.Field required
                label = 'Rounds'
                id = 'rounds'
                type = 'number'
                placeholder = '1'
                onChange = {onSelectChange}
                control = {Select}
                options = {selectOptions.slice(0, 21)}
            />
            <Form.Field required
                label = 'Reproduction Rate'
                id = 'reproduction'
                type = 'number'
                onChange = {onChange}
                control = 'input'
                min = {0}
                max = {100}
            />
        </Form.Group>
        <Form.Button type='submit'>Load Tournament Visual</Form.Button>
    </Form>

}

export default TournamentFormComponent;
