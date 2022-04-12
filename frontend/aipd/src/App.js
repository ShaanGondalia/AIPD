import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";

import ResultsPage from "./Pages/ResultsPage";
import SinglePlayerPage from "./Pages/SinglePlayerPage";
import TournamentPage from "./Pages/TournamentPage";
import NavbarComponent from "./Components/NavbarComponent";
import AboutPage from "./Pages/AboutPage";

function App() {
  return (
    <div>
      <Router>
        <NavbarComponent/>
        <Routes>
          <Route path = "/" element={<SinglePlayerPage/>}/>
        </Routes>
        <Routes>
          <Route path = "/about" element={<AboutPage/>}/>
        </Routes>
        <Routes>
          <Route path = "/results" element={<ResultsPage/>}/>
        </Routes>
        <Routes>
          <Route path = "/tournament" element={<TournamentPage/>}/>
        </Routes>
      </Router>
    </div>

  );
}

export default App;
