import { Routes, Route } from "react-router-dom";

import Home from "../pages/Home";

import Prediction from "../pages/Prediction";

import About from "../pages/About";

import Help from "../pages/Help";

import Download from "../pages/Download";

import Contact from "../pages/Contact";

function AppRoutes() {

  return (

    <Routes>

      <Route
        path="/"
        element={<Home />}
      />

      <Route
        path="/prediction"
        element={<Prediction />}
      />

      <Route
        path="/about"
        element={<About />}
      />

      <Route
        path="/help"
        element={<Help />}
      />

      <Route
        path="/download"
        element={<Download />}
      />

      <Route
        path="/contact"
        element={<Contact />}
      />

    </Routes>

  );

}

export default AppRoutes;