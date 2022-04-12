import React from 'react';
import { Menu, Segment } from 'semantic-ui-react';
import { Link } from 'react-router-dom';

const NavbarComponent = () => {

    return <Menu widths={4} inverted>
        <Menu.Item>
            <Link to="/">Home</Link>
        </Menu.Item>
        <Menu.Item>
            <Link to="/about">About</Link>
        </Menu.Item>
        <Menu.Item>
            <Link to="/results">Results</Link>
        </Menu.Item>
        <Menu.Item>
            <Link to="/tournament">Tournament</Link>
        </Menu.Item>
    </Menu>
}

export default NavbarComponent;