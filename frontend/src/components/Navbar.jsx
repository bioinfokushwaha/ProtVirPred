import { Link } from "react-router-dom";

import paraVirPredLogo from "../assets/logos/paravirpred-logo.png";

function Navbar() {

  return (

    <nav className="navbar">

      <Link
        to="/"
        className="navbar-brand"
      >

        <img
          src={paraVirPredLogo}
          alt="ParaVirPred"
          className="navbar-logo-img"
        />

        <span className="navbar-logo-text">
          ParaVirPred
        </span>

      </Link>

      <div className="navbar-links">

        <Link to="/">
          Home
        </Link>

        <Link to="/about">
          About
        </Link>

        <Link to="/prediction">
          Prediction
        </Link>

        <Link to="/download">
          Download
        </Link>

        <Link to="/help">
          Help
        </Link>

        <Link to="/contact">
          Contact
        </Link>

      </div>

    </nav>

  );

}

export default Navbar;